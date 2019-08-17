from django import forms
from mxv.models import EmailSettings
from members.models import Member

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

    # returns a field created from the profile field
    def CreateFieldFromProfileField(self, profile_field):
        # create the field
        field_class = getattr(forms, '%sField' % profile_field.field_type)
        field = field_class()
        
        # set the field parameters
        field.label = profile_field.display_text
        field.initial = field.to_python(profile_field.value_string)
        field.required = profile_field.required
        
        return(field)
    
    # turns a dotted field path into a valid field name
    def field_path_to_name(self, field_path):
        return field_path.replace('.', '__')

    # turns a field name into a dotted field path
    def name_to_field_path(self, name):
        return name.replace('__', '.')

    # adds the profile fields to the form in display order
    def __init__(self, *args, **kwargs):
        profile_fields = kwargs.pop('profile_fields')
        super(MemberProfileForm, self).__init__(*args, **kwargs)
        profile_fields.sort(key = lambda field: field.display_order)
        for profile_field in profile_fields:
            self.fields[self.field_path_to_name(profile_field.field_path)] = self.CreateFieldFromProfileField(profile_field)
    
    # returns the name/value tuples of the profile fields        
    def extra_field_values(self):
        values = {}
        for name, value in self.cleaned_data.items():
            values[self.name_to_field_path(name)] = value
        return values
                
                