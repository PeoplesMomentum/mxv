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

    class Meta:
        model = Member
        fields = ['name']
        
    def FieldFromType(self, field_type):
        field_class = getattr(forms, '%sField' % field_type)
        return(field_class())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields')
        super(MemberProfileForm, self).__init__(*args, **kwargs)

        for extra_field in extra_fields:
            field = self.FieldFromType(extra_field.field_type)
            field.label = extra_field.display_text
            field.initial = field.to_python(extra_field.value_string)
            field.required = extra_field.required
            self.fields['custom_%s' % extra_field.field_path] = field