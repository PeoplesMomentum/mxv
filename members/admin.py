from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from members.models import Member, ProfileField, UpdateDetailsCampaign, CampaignField, UrlParameter, CampaignTagGroup, CampaignTag
from solo.admin import SingletonModelAdmin
from django.contrib.auth.models import Group
from mxv.models import EmailSettings
from mxv.nation_builder import NationBuilder
from django.db import models
from django.forms.widgets import Textarea, TextInput
from nested_admin import nested
from django.utils.safestring import mark_safe

# form for creating a new member
class MemberCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ('email', 'name', 'activation_key')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        member = super(MemberCreationForm, self).save(commit=False)
        member.set_password(self.cleaned_data["password1"])
        if commit:
            member.save()
        return member

# form for editing a member
class MemberChangeForm(forms.ModelForm):
    # change inherited fields
    def __init__(self, *args, **kwargs):
        super(MemberChangeForm, self).__init__(*args, **kwargs)
        self.fields['is_superuser'].label = 'Momentum staff'
        self.fields['is_superuser'].help_text = 'Staff can access this admin interface and do pretty much anything'

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this member's password, but you can change the password "
                    "using <a href=\'../password/\'>this form</a>."))

    class Meta:
        model = Member
        fields = ('email', 'password', 'name', 'activation_key', 'is_active', 'last_emailed', 'is_superuser', 'is_ncg', 'is_members_council')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# member admin setup
class MemberAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = MemberChangeForm
    add_form = MemberCreationForm

    # The fields to be used in displaying the member model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'activation_key', 'is_active', 'last_emailed', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'activation_key', 'is_active', 'last_emailed')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_ncg', 'is_members_council')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('GDPR', {'fields': ('is_anonymised',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'activation_key', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('activation_key', 'last_login', 'last_emailed','is_anonymised' )
    actions = ['make_anonymised']

    # sends the activation email to the member
    def response_change(self, request, obj):
        member = obj
        settings = EmailSettings.get_solo()
        sent = 0
        
        # if a post requesting the activation email to be sent...
        if request.method == 'POST' and 'send_activation_email' in request.POST:
            
            # and there is an activation email...
            activation_email = settings.activation_email
            if activation_email:
                try:
                    
                    # send the activation email
                    sent += activation_email.send_to(request, [member.email])
                except Exception as e:
                    messages.error(request, repr(e))

            messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
        
        # if a post requesting the member be anonymised...
        if request.method == 'POST' and 'anonymise_member' in request.POST:
            member.anonymise_user()
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)


# Momentum group admin
class MemberInline(admin.TabularInline):
    model = Member
    fields = ('email','name', )
    readonly_fields = ('email','name', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
# activation email admin setup
class MemberActivationEmailModelAdmin(SingletonModelAdmin):
    # hide from the app list as it's linked separately
    def get_model_perms(self, request):
        return {}
    
# profile field admin
class ProfileFieldAdminForm(forms.ModelForm):
    field_path = forms.ChoiceField()
    
    # gets the nation builder id for the current user if required
    def __init__(self, *args, **kwargs):
        super(ProfileFieldAdminForm, self).__init__(*args, **kwargs)
        nb = NationBuilder()
        if not self.current_user.nation_builder_person.nation_builder_id:
            self.current_user.nation_builder_person.nation_builder_id = nb.GetIdFromEmail(self.current_user.email)
            self.current_user.save()
        self.fields['field_path'].choices = [(field[0], field[2]) for field in nb.PersonFieldsAndValues(self.current_user.nation_builder_person.nation_builder_id)]
        self.fields['field_path'].help_text = 'Example field values are from your NationBuilder record (id = %d)' % self.current_user.nation_builder_person.nation_builder_id
    
class ProfileFieldAdmin(admin.ModelAdmin):
    form = ProfileFieldAdminForm
    
    # stores the current user
    def get_form(self, request, *args, **kwargs):
        form = super(ProfileFieldAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form
        
    list_display = ('display_order', 'display_text', 'field_path', 'field_type', 'required', 'admin_only', 'is_phone_number', 'negate_value')
    ordering = ('display_order', )

# campaign tag admin
class CampaignTagInline(nested.NestedTabularInline):
    model = CampaignTag
    ordering = ['display_order']
    extra = 0
 
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
 
# campaign tag group admin
class CampaignTagGroupInline(nested.NestedTabularInline):
    model = CampaignTagGroup
    ordering = ['display_order']
    extra = 0
    inlines = [ CampaignTagInline ]
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }

# campaign field admin
class CampaignFieldInline(nested.NestedTabularInline):
    model = CampaignField
    ordering = ['display_order']
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 75 })}, 
    }
    
    # populates the field path choices from the current user's nation builder record
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'field_path':
            nb = NationBuilder()
            if not request.user.nation_builder_person.nation_builder_id:
                request.user.nation_builder_person.nation_builder_id = nb.GetIdFromEmail(request.user.email)
                request.user.save()
            db_field.choices = [(field[0], field[2]) for field in nb.PersonFieldsAndValues(request.user.nation_builder_person.nation_builder_id)]
            db_field.help_text = 'Example field values are from your NationBuilder record (id = %d)' % request.user.nation_builder_person.nation_builder_id
        return super(CampaignFieldInline, self).formfield_for_dbfield(db_field, request, **kwargs)

# URL parameter admin
class UrlParameterInline(nested.NestedTabularInline):
    model = UrlParameter
    ordering = ['name']
    extra = 0
    formfield_overrides = { 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 50 })}, 
    }
    
# update details campaign
class UpdateDetailsCampaignAdmin(nested.NestedModelAdmin, SingletonModelAdmin):
    formfield_overrides = { 
        models.TextField: { 'widget': Textarea(attrs = { 'rows': 5, 'cols': 200 })}, 
        models.CharField: { 'widget': TextInput(attrs = { 'size': 200 })}, 
    }
    inlines = [CampaignTagGroupInline, CampaignFieldInline, UrlParameterInline ]
    model = UpdateDetailsCampaign
    fields = (
        ('fields_page_header', 'fields_page_footer', ),
        ('redirect_url'),
        ('nation_builder_url'))
    readonly_fields = ('nation_builder_url',)

    # URL for use in NationBuilder
    def nation_builder_url(self, campaign):
        parameters = []
        for param in campaign.url_parameters.all().order_by('name'):
            parameters.append((param.name, param.nation_builder_value if param.nation_builder_value else ''))
        url = '<p>https://my.peoplesmomentum.com/members/update_details/1?%s</p>' % '&'.join('='.join(param) for param in parameters)
        return mark_safe(url)

# not using builtin permissions
admin.site.unregister(Group)

# register admins
admin.site.register(Member, MemberAdmin)
admin.site.register(ProfileField, ProfileFieldAdmin)
admin.site.register(UpdateDetailsCampaign, UpdateDetailsCampaignAdmin)

