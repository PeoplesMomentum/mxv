from django import forms
from mxv.models import EmailSettings
from members.models import Member, ProfileFieldType
from django.contrib.auth.hashers import check_password
from django.utils.safestring import mark_safe
from django.core.validators import RegexValidator

# form for sending member activation email
class SendMemberActivationEmailsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['test_email_address', 'send_count', 'is_active', 'activation_email']
        widgets = {
            'test_email_address': forms.TextInput(attrs={'size':65})}

# member profile form
class MemberProfileForm(forms.ModelForm):

    # a model form needs a model with at least one field but we don't want to show any of the member fields directly, just via NationBuildeer
    # so we include a read-only and hidden name field 
    class Meta:
        model = Member
        fields = ['name', ]
    name = forms.CharField(label = '', widget = forms.TextInput(attrs = { 'readonly': True, 'hidden': True, 'height': 1 }))

    # tracks which fields are negated
    negated_field_paths = []

    # adds the profile fields to the form in display order
    def __init__(self, *args, **kwargs):
        profile_fields = None
        if 'profile_fields' in kwargs:
            profile_fields = kwargs.pop('profile_fields')
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        if profile_fields:
            profile_fields.sort(key = lambda field: field.display_order)
            for profile_field in profile_fields:
                self.fields[self.field_path_to_name(profile_field.field_path)] = self.CreateFieldFromProfileField(profile_field)
    
    # returns a field created from the profile field
    def CreateFieldFromProfileField(self, profile_field):
        # create the field
        field_class = getattr(forms, '%sField' % profile_field.field_type)
        field = field_class()
        
        # set the field parameters
        field.label = mark_safe(profile_field.display_text)
        field.initial = field.to_python(profile_field.value_string)
        field.required = profile_field.required
        
        # validate phone number fields
        if profile_field.is_phone_number:   # from http://regexlib.com/REDetails.aspx?regexp_id=589
            field.validators = [RegexValidator(r'^((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$', 'Please enter a valid phone number')]
        
        # negate checkbox fields
        if profile_field.field_type == 'Boolean' and profile_field.negate_value:
            self.negated_field_paths.append(profile_field.field_path)
            field.initial = True if field.initial == False else False
        
        return(field)
    
    # turns a dotted field path into a valid field name
    def field_path_to_name(self, field_path):
        return field_path.replace('.', '__')

    # turns a field name into a dotted field path
    def name_to_field_path(self, name):
        return name.replace('__', '.')

    # returns a dictionary of the profile fields' names and values
    def profile_field_values(self):
        values = {}
        for name, value in self.cleaned_data.items():
            values[self.name_to_field_path(name)] = value

        # negate values for negated checkboxes
        for field_path in values.keys():
            if field_path in self.negated_field_paths:
                values[field_path] = True if values[field_path] == False else False
        
        return values

# user details form
class UserDetailsForm(forms.Form):
    
    # tracks which fields are negated
    negated_field_paths = []

    # adds the tags and profile fields to the form in display order
    def __init__(self, *args, **kwargs):
        profile_fields = None
        if 'profile_fields' in kwargs:
            profile_fields = kwargs.pop('profile_fields')
        tags = None
        if 'tags' in kwargs:
            tags = kwargs.pop('tags')
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        if profile_fields:
            profile_fields.sort(key = lambda field: field.display_order)
            for profile_field in profile_fields:
                self.fields[self.field_path_to_name(profile_field.field_path)] = self.CreateFieldFromProfileField(profile_field)
        if tags:
            tags.sort(key = lambda tag: tag.display_order)
            for tag in tags:
                self.fields[tag.tag] = self.CreateFieldFromTag(tag)
        
    # returns a field created from the profile field
    def CreateFieldFromProfileField(self, profile_field):
        # create the field
        field_class = getattr(forms, '%sField' % profile_field.field_type)
        field = field_class()
        
        # set the field parameters
        field.label = mark_safe(profile_field.display_text)
        field.initial = field.to_python(profile_field.value_string)
        field.required = profile_field.required
        
        # validate phone number fields
        if profile_field.is_phone_number:   # from http://regexlib.com/REDetails.aspx?regexp_id=589
            field.validators = [RegexValidator(r'^((\(?0\d{4}\)?\s?\d{3}\s?\d{3})|(\(?0\d{3}\)?\s?\d{3}\s?\d{4})|(\(?0\d{2}\)?\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$', 'Please enter a valid phone number')]
        
        # negate checkbox fields
        if profile_field.field_type == 'Boolean' and profile_field.negate_value:
            self.negated_field_paths.append(profile_field.field_path)
            field.initial = True if field.initial == False else False
        
        return(field)
    
    # turns a dotted field path into a valid field name
    def field_path_to_name(self, field_path):
        return field_path.replace('.', '__')

    # turns a field name into a dotted field path
    def name_to_field_path(self, name):
        return name.replace('__', '.')

    # returns a dictionary of the profile fields' names and values
    def profile_field_values(self):
        values = {}
        for name, value in self.cleaned_data.items():
            values[self.name_to_field_path(name)] = value
        
        # negate values for negated checkboxes
        for field_path in values.keys():
            if field_path in self.negated_field_paths:
                values[field_path] = True if values[field_path] == False else False
        
        return values
    
    # returns a field created from the tag
    def CreateFieldFromTag(self, tag):
        # create the field
        field = forms.BooleanField()
        
        # set the field parameters
        field.label = mark_safe(tag.display_text)
        field.initial = field.to_python(tag.value_string)
        field.required = False
        
        return field

    # returns a dictionary of the tag' names and values
    def tag_values(self):
        values = {}
        for name, value in self.cleaned_data.items():
            values[name] = value
        return values
    
# verify login email form
class VerifyEmailForm(forms.Form):
    email = forms.EmailField(label = 'New login email', widget = forms.EmailInput(attrs = { 'readonly': True }))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput())
    
    # stores the request
    def __init__(self, *args, **kwargs):
        self.password_digest = kwargs.pop('password_digest')
        super(VerifyEmailForm, self).__init__(*args, **kwargs)
        
    # checks the entered password against the member's password
    def clean(self):
        form_data = self.cleaned_data
        if not check_password(form_data['password'], self.password_digest):
            self._errors["password"] = ["Password is incorrect"]
            del form_data['password']
        return form_data
    

    
                