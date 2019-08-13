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
    # so we include a readonly and hidden name field
    class Meta:
        model = Member
        fields = ['name']
    name = forms.CharField(label = '', widget = forms.TextInput(attrs = { 'readonly': True, 'hidden': True }))
         
    # returns the class of a field (assumes that field_type+'Field' is a valid field class)
    def FieldFromType(self, field_type):
        field_class = getattr(forms, '%sField' % field_type)
        return(field_class())

    # adds the extra fields to the form
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        super(MemberProfileForm, self).__init__(*args, **kwargs)

        for extra_field in extra_fields:
            field = self.FieldFromType(extra_field.field_type)
            field.label = extra_field.display_text
            field.initial = field.to_python(extra_field.value_string)
            field.required = extra_field.required
            self.fields['custom_%s' % extra_field.field_path] = field
    
    # returns the name/value tuples of the extra fields        
    def extra_field_values(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (name[7:], value)