from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from members.models import Member, MemberActivationEmail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from members.forms import EditMemberActivationEmailForm, SendMemberActivationEmailsForm, ImportMemberNamesAndEmailAddressesForm
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from mxv.settings import JOIN_URL, CREATE_INACTIVE_MEMBER_SECRET
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render

# signals that a conflict occurred
class HttpResponseConflict(HttpResponse):
    status_code = 409

# creates an inactive member for the email and name (POST with email, name and secret)
@csrf_exempt
def create_inactive_member(request):
        # if it's a post and the secret is correct...
        if request.method == 'POST' and request.POST['secret'] == CREATE_INACTIVE_MEMBER_SECRET:
            
            # if the member doesn't already exist...
            if not Member.objects.filter(email = request.POST['email']).exists():

                # create the member
                Member.objects.create_member(email = request.POST['email'], name = request.POST['name'])
                return HttpResponse(content = 'Created inactive member for ' + request.POST['email'])
            else:
                # signal that the member already exists
                return HttpResponseConflict(content = 'Member with email %s already exists' % request.POST['email'])
        else:
            return HttpResponseForbidden()

# edits the member activation email
@staff_member_required
def edit_member_activation_email(request):
    
    # include the django admin context for the member links
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
            return HttpResponseRedirect(reverse('membersadmin:edit_member_activation_email'))
        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/edit_member_activation_email.html', context)

# sends the member activation email
@staff_member_required
def send_member_activation_emails(request):
    
    # include the django admin context for the member links
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
            return HttpResponseRedirect(reverse('membersadmin:send_member_activation_emails'))
        
    # if sending to uninvited...
    if request.method == 'POST' and 'send_to_count_uninvited' in request.POST:
        
        # .. and the posted form is valid...
        form = SendMemberActivationEmailsForm(request.POST)
        if form.is_valid():
            
            # update the send count
            member_activation_email.send_count = form.cleaned_data['send_count']
            member_activation_email.is_active = form.cleaned_data['is_active']
            member_activation_email.save()
            
            try:                
                # send the activation email to uninvited members
                sent = member_activation_email.send_to_count_uninvited(request)
                messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
            
            except Exception as e:
                messages.error(request, repr(e))

            # redirect
            return HttpResponseRedirect(reverse('membersadmin:send_member_activation_emails'))
        
    # if sending to targeted...
    if request.method == 'POST' and 'send_to_count_targeted' in request.POST:
        
        # .. and the posted form is valid...
        form = SendMemberActivationEmailsForm(request.POST)
        if form.is_valid():
            
            # update the send count and active
            member_activation_email.send_count = form.cleaned_data['send_count']
            member_activation_email.is_active = form.cleaned_data['is_active']
            member_activation_email.save()
            
            try:                
                # send the activation email to targeted members
                sent = member_activation_email.send_to_count_targeted(request)
                messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
            
            except Exception as e:
                messages.error(request, repr(e))

            # redirect
            return HttpResponseRedirect(reverse('membersadmin:send_member_activation_emails'))
        
    # if sending to inactive members...
    if request.method == 'POST' and 'send' in request.POST:
        
        try:            
            # send the activation email to inactive members
            sent = member_activation_email.send_to_inactive_members(request)
            messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
        
        except Exception as e:
            messages.error(request, repr(e))

        # redirect
        return HttpResponseRedirect(reverse('membersadmin:send_member_activation_emails'))
                
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/send_member_activation_emails.html', context)

# imports a list of names and email addresses
@staff_member_required
def import_member_names_and_email_addresses(request):
    
    # track members
    members_created = 0
    members_already_existing = 0

    # include the django admin context for the member links
    context = site.each_context(request)

    # logs the members created and already existing
    def log_members():
        messages.info(request, "%d members created (%d already existed)" % (members_created, members_already_existing))
    
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
                    
                    # create a member from the name and email address                       
                    fields = line.split(",")                    
                    try:
                        name = fields[0].replace('"', '')
                        email = fields[1].replace('"', '')
                        Member.objects.create_member(name = name, email = email)
                        members_created += 1
                    except (IntegrityError):
                        members_already_existing += 1
            
                # log number of members created and existing
                log_members()
            
                # redirect
                return HttpResponseRedirect(reverse('membersadmin:import_member_names_and_email_addresses'))
        
        # add exceptions to errors and log number of members created and existing
        except Exception as e:
            messages.error(request, repr(e))
            log_members()
                        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/import_member_names_and_email_addresses.html', context)

# activates the member
def activate(request, activation_key):
    
    # get the member with the activation key
    member = Member.objects.filter(activation_key = activation_key).first()
    
    # redirect activation attempts for an unknown member to the join page
    if not member:
        return HttpResponseRedirect(JOIN_URL)
    
    # redirect activation attempts for an active member to the login page
    if member.is_active:
        return HttpResponseRedirect(reverse('login'))

    # if valid post...
    if request.method == 'POST':
        form = SetPasswordForm(member, request.POST)
        if form.is_valid():
            
            # make the member active and save the user's password
            member.is_active = True
            member = form.save()
            
            # log the member in
            update_session_auth_hash(request, member)
            authenticate(request)
            login(request, member)
            messages.success(request, 'Your password was successfully set!')
            return HttpResponseRedirect('/')
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SetPasswordForm(member)

    return render(request, 'members/activate.html', { 
        'member' : member,
        'form': form })

