from django.contrib import admin
from mxv.models import Email, EmailSettings, DefaultUrlParameter
from members.models import Member
from django.contrib import messages
from solo.admin import SingletonModelAdmin

# admin site title
admin.site.site_header = 'My Momentum - Administration'

# emails
class EmailAdmin(admin.ModelAdmin):
    search_fields = ('name', 'subject', 'html_content', 'text_content')
    list_display = ('name', 'subject')
    fields = (
        'name',
        'subject', 
        'html_content', 
        'text_content'
    )
    
    # sends the email to (in)active members (last_emailed needs to be manually set to null for the target members first)
    def response_change(self, request, obj):
        email = obj
        settings = EmailSettings.get_solo()
        members = []
        sent = 0
        
        if request.method == 'POST' and ('send_to_all_active_members' in request.POST or 'send_to_all_inactive_members' in request.POST or 'send_to_test_address' in request.POST):
            
            # get the members to send to
            if 'send_to_all_active_members' in request.POST:
                members = Member.objects.filter(is_active = True, last_emailed = None)
            if 'send_to_all_inactive_members' in request.POST:
                members = Member.objects.filter(is_active = False, last_emailed = None)
            if 'send_to_test_address' in request.POST:
                members = Member.objects.filter(email = settings.test_email_address)
            
            # only send to a few to avoid timeouts
            members_to_send = members[:settings.send_count]
            
            # send the email
            try:
                sent = email.send_to(request, { member.email for member in members_to_send })
                messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
            except Exception as e:
                messages.error(request, repr(e))                
                            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)

# default URL parameter admin
class DefaultUrlParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'pass_on_name', 'nation_builder_value')
    fields = ('name', 'pass_on_name', 'nation_builder_value')
    ordering = ['name']

admin.site.register(DefaultUrlParameter, DefaultUrlParameterAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(EmailSettings, SingletonModelAdmin)
