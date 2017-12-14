from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from members.models import Member, MemberActivationEmail
from solo.admin import SingletonModelAdmin
from django.contrib.auth.models import Group

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
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this member's password, but you can change the password "
                    "using <a href=\'../password/\'>this form</a>."))

    class Meta:
        model = Member
        fields = ('email', 'password', 'name', 'activation_key', 'is_active', 'is_superuser')

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
    list_display = ('email', 'name', 'activation_key', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'activation_key', 'is_active')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'activation_key', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('activation_key',)

# activation email admin setup
class MemberActivationEmailModelAdmin(SingletonModelAdmin):
    # hide from the app list as it's linked separately
    def get_model_perms(self, request):
        return {}

# register the new admin classes
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberActivationEmail, MemberActivationEmailModelAdmin)

# not using builtin permissions
admin.site.unregister(Group)
