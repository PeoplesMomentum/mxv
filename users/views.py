from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from users.models import User, MemberActivationEmail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin import site
from .forms import EditMemberActivationEmailForm, SendMemberActivationEmailsForm, ImportMemberNamesAndEmailAddressesForm
from django.contrib import messages
from django.db import IntegrityError

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
    
    # track users
    users_created = 0
    users_already_existing = 0

    # include the django admin context for the user links
    context = site.each_context(request)

    # logs the users created and already existing
    def log_users():
        messages.info(request, "%d users created (%d already existed)" % (users_created, users_already_existing))
    
    # create am empty form in case this is a GET
    form = ImportMemberNamesAndEmailAddressesForm()
    
    # if a POST and import was clicked...
    if request.method == 'POST' and 'import' in request.POST:
        
        try:
            # get the uploaded file
            csv = request.FILES['csv']
            
            # reject multi-chunk files
            if csv.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv.size / (1000000)))
            else:                    
                # for each line in the file...                    
                lines = csv.read().decode("utf-8").split("\n")
                for line in lines: 
                    
                    # create a user from the name and email address                       
                    fields = line.split(",")                    
                    try:
                        name = fields[0].replace('"', '')
                        email = fields[1].replace('"', '')
                        User.objects.create_user(name = name, email = email)
                        users_created += 1
                    except (IntegrityError):
                        users_already_existing += 1
            
                # log number of users created and existing
                log_users()
            
                # redirect
                return HttpResponseRedirect('/admin/import_member_names_and_email_addresses')
        
        # add exceptions to errors and log number of users created and existing
        except Exception as e:
            messages.error(request, repr(e))
            log_users()
                        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'users/import_member_names_and_email_addresses.html', context)

