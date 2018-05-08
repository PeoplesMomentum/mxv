from django.contrib import admin
from mxv.models import Email

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

# register the admin classes
admin.site.register(Email, EmailAdmin)