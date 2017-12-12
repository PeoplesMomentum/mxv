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
from django.urls import reverse

# creates an inactive user for the email and name (POST with email, name and secret)
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

# edits the member activation email
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
            member_activation_email.html_content = form.cleaned_data['html_content']
            member_activation_email.text_content = form.cleaned_data['text_content']
            member_activation_email.save()
            
            # redirect
            return HttpResponseRedirect(reverse('usersadmin:edit_member_activation_email'))
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/edit_member_activation_email.html', context)

# sends the member activation email
@staff_member_required
def send_member_activation_emails(request):
    
    # include the django admin context for the user links
    context = site.each_context(request)

    # populate the form with the singleton activation email in case this is a GET
    member_activation_email = MemberActivationEmail.get_solo()
    form = SendMemberActivationEmailsForm(instance = member_activation_email)
    
    # if sending a test email...
    if request.method == 'POST' and 'send_test' in request.POST:
        
        # .. and the posted form is valid...
        form = SendMemberActivationEmailsForm(request.POST)
        if form.is_valid():
            
            # update the member email
            member_activation_email.test_email_address = form.cleaned_data['test_email_address']
            member_activation_email.save()
            
            try:                
                # send the activation email to the test address
                sent = member_activation_email.send_test(request)
                messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
            
            except Exception as e:
                messages.error(request, repr(e))

            # redirect
            return HttpResponseRedirect(reverse('usersadmin:send_member_activation_emails'))
        
    # if sending to inactive users...
    if request.method == 'POST' and 'send' in request.POST:
        
        try:            
            # send the activation email to inactive users
            sent = member_activation_email.send_to_inactive_users(request)
            messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
        
        except Exception as e:
            messages.error(request, repr(e))

        # redirect
        return HttpResponseRedirect(reverse('usersadmin:send_member_activation_emails'))
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/send_member_activation_emails.html', context)

# imports a list of names and email addresses
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
                return HttpResponseRedirect(reverse('usersadmin:import_member_names_and_email_addresses'))
        
        # add exceptions to errors and log number of users created and existing
        except Exception as e:
            messages.error(request, repr(e))
            log_users()
                        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/import_member_names_and_email_addresses.html', context)

# activates the member
@staff_member_required
def activate(request, activation_key):
    pass