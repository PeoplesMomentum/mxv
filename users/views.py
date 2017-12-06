from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from users.models import User, MemberActivationEmail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin import site
from .forms import EditMemberActivationEmailForm, SendMemberActivationEmailsForm, ImportMemberNamesAndEmailAddressesForm

# creates an inactive user for the email and name
@csrf_exempt
def create_inactive_user(request):
    try:
        
        # if it's a post and the secret is correct...
        if request.method == 'POST' and request.POST['secret'] == settings.CREATE_INACTIVE_USER_SECRET:
            
            # create the user
            User.objects.create_user(email = request.POST['email'], name = request.POST['name'])
            return HttpResponse(content = 'Created inactive user for ' + request.POST['email'])
        else:
            return HttpResponseForbidden()
    except (KeyError):
        return HttpResponseForbidden()

# returns the member activation email view
@staff_member_required
def edit_member_activation_email(request):
    
    # include the django admin context for the user links
    context = site.each_context(request)

    # populate the form with the singleton activation email in case this is a GET
    member_activation_email = MemberActivationEmail.get_solo()
    form = EditMemberActivationEmailForm(instance = member_activation_email)
    
    # if a POST and save was clicked...
    if request.method == 'POST' and 'save' in request.POST:
        
        # .. and the posted form is valid...
        form = EditMemberActivationEmailForm(request.POST)
        if form.is_valid():
            
            # update the member email
            member_activation_email.subject = form.cleaned_data['subject']
            member_activation_email.content = form.cleaned_data['content']
            member_activation_email.save()
            
            # redirect
            return HttpResponseRedirect('/admin/edit_member_activation_email')      
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'users/edit_member_activation_email.html', context)

# returns the member activation email view
@staff_member_required
def send_member_activation_emails(request):
    
    # include the django admin context for the user links
    context = site.each_context(request)

    # populate the form with the singleton activation email in case this is a GET
    member_activation_email = MemberActivationEmail.get_solo()
    form = SendMemberActivationEmailsForm(instance = member_activation_email)
    
    # if a POST and send test was clicked...
    if request.method == 'POST' and 'send_test' in request.POST:
        
        # .. and the posted form is valid...
        form = SendMemberActivationEmailsForm(request.POST)
        if form.is_valid():
            
            # update the member email
            member_activation_email.test_email_address = form.cleaned_data['test_email_address']
            member_activation_email.save()
            
            # redirect
            return HttpResponseRedirect('/admin/send_member_activation_emails')      
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'users/send_member_activation_emails.html', context)

# returns the member activation email view
@staff_member_required
def import_member_names_and_email_addresses(request):
    
    # include the django admin context for the user links
    context = site.each_context(request)

    # create am empty form in case this is a GET
    form = ImportMemberNamesAndEmailAddressesForm()
    
    # if a POST and import was clicked...
    if request.method == 'POST' and 'import' in request.POST:
        
        # .. and the posted form is valid...
        form = ImportMemberNamesAndEmailAddressesForm(request.POST)
        if form.is_valid():
            
            # import the member names and email addresses
            
            # redirect
            return HttpResponseRedirect('/admin/import_member_names_and_email_addresses')      
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'users/import_member_names_and_email_addresses.html', context)

