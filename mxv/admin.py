from django.contrib import admin
from mxv.models import Email, EmailSettings
from members.models import Member
from django.contrib import messages

# admin site title
admin.site.site_header = 'My Momentum - Administration'

# emails
class EmailAdmin(admin.ModelAdmin):
    search_fields = ('subject', 'html_content', 'text_content')
    list_display = ('subject',)
    fields = (
        'subject', 
        'html_content', 
        'text_content'
    )
    
    # sends the email to (in)active members
    def response_change(self, request, obj):
        email = obj
        settings = EmailSettings.get_solo()
        members = []
        sent = 0
        
        if request.method == 'POST' and ('send_to_all_active_members' in request.POST or 'send_to_all_inactive_members' in request.POST):
            
            # get the members to send to
            if 'send_to_all_active_members' in request.POST:
                members = Member.objects.filter(is_active = True)
            if 'send_to_all_inactive_members' in request.POST:
                members = Member.objects.filter(is_active = False)
            
            # while there are members to send the email to...
            while (len(members) > 0):
            
                # get the next group to send
                members_to_send = members[:settings.send_count]
                members = [member for member in members if not member in members_to_send]
                
                # send the email
                try:
                    sent += email.send_to(request, { member.email for member in members_to_send })
                except Exception as e:
                    messages.error(request, repr(e))                
                
            messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)


# register the admin classes
admin.site.register(Email, EmailAdmin)