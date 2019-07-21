from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from members.models import Member, MemberEditableNationBuilderField
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from members.forms import SendMemberActivationEmailsForm, MemberProfileForm
from django.contrib import messages
from django.urls import reverse
from mxv.settings import JOIN_URL, CREATE_INACTIVE_MEMBER_SECRET, PROFILES_VISIBLE_TO_NON_STAFF
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect
from mxv.models import EmailSettings
from mxv import forms
from django.contrib.auth.decorators import login_required
from mxv.nation_builder import NationBuilder

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
                member = Member.objects.create_member(email = request.POST['email'], name = request.POST['name'])
                
                # send the activation email
                activation_email = EmailSettings.get_solo().activation_email
                if activation_email:
                    try:
                        activation_email.send_to(request, [member.email])
                    except Exception as e:
                        return HttpResponseBadRequest(content = repr(e) + ' (email address is probably invalid)')
                
                return HttpResponse(content = 'Created inactive member for ' + request.POST['email'])
            else:
                # signal that the member already exists
                return HttpResponseConflict(content = 'Member with email %s already exists' % request.POST['email'])
        else:
            return HttpResponseForbidden()

# sends the member activation email
@staff_member_required
def send_member_activation_emails(request):
    
    # include the django admin context for the member links
    context = site.each_context(request)

    # populate the form with the email settings in case this is a GET
    email_settings = EmailSettings.get_solo()
    form = SendMemberActivationEmailsForm(instance = email_settings)
    
    # if a valid post...
    if request.method == 'POST':
        form = SendMemberActivationEmailsForm(request.POST)
        if form.is_valid():           
            try:
                
                # update the email settings
                if not ('cancel' in request.POST):
                    email_settings.test_email_address = form.cleaned_data['test_email_address']
                    email_settings.send_count = form.cleaned_data['send_count']
                    email_settings.is_active = form.cleaned_data['is_active']
                    email_settings.activation_email = form.cleaned_data['activation_email']
                    email_settings.save()

                # if there is an activation email set...
                if email_settings.activation_email:
                    
                    # send the activation email to the test address
                    if 'send_test' in request.POST:
                        sent = email_settings.activation_email.send_test(request)
                        messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
                        
                    # send the activation email to uninvited members
                    if 'send_to_count_uninvited' in request.POST:
                        sent = email_settings.activation_email.send_to_count_uninvited(request)
                        messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
                        
                    # send the activation email to targeted members
                    if 'send_to_count_targeted' in request.POST:
                        sent = email_settings.activation_email.send_to_count_targeted(request)
                        messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
                        
                    # send the activation email to inactive members
                    if 'send' in request.POST:
                        sent = email_settings.activation_email.send_to_inactive_members(request)
                        messages.info(request, "%d member%s emailed" % (sent, 's' if sent != 1 else ''))
                    
            except Exception as e:
                messages.error(request, repr(e))
        
        # redirect
        return HttpResponseRedirect(reverse('membersadmin:send_member_activation_emails'))
                        
    # add the form to the context
    context['form'] = form
    
    # render the page
    return render(request, 'admin/send_member_activation_emails.html', context)

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
            
            # redirect to next if required
            next_redirect = request.GET.get('next', None)
            if next_redirect:
                return HttpResponseRedirect(next_redirect)
            else:
                return HttpResponseRedirect('/')
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SetPasswordForm(member)

    return render(request, 'members/activate.html', { 
        'member' : member,
        'form': form })

# allows entry of an email address to which an activation email will be sent
def request_activation_email(request):
    
    # if valid post...
    if request.method == 'POST':
        form = forms.RequestActivationEmailForm(request.POST)
        if form.is_valid():
            
            # and the email entered is for an inactive member...
            email = form.cleaned_data.get('email')
            try:
                inactive_member = Member.objects.get(email = email, is_active = False)
            except:
                inactive_member = None
            if inactive_member:
                
                # send an activation email
                activation_email = EmailSettings.get_solo().activation_email
                if activation_email:
                    try:
                        activation_email.send_to(request, [inactive_member.email])
                    except:
                        pass
         
            # always notify that an activation email might have been sent
            messages.info(request, 'If you’re a member but haven’t activated your account yet then you’ve been sent an activation email (so check your email inbox and spam folders)')

            return HttpResponseRedirect('/')
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.RequestActivationEmailForm()

    return render(request, 'members/request_activation_email.html', { 
        'form': form })

# displays the member's profile page
@login_required
def profile(request):
    
    # redirect if profiles are not visible to this user
    if not request.user.is_superuser and not PROFILES_VISIBLE_TO_NON_STAFF:
        return redirect('index')

    # get the member's nation builder id
    member = request.user
    nb = NationBuilder()
    if not member.nation_builder_id:
        member.nation_builder_id = nb.GetIdFromEmail(member.email)
        member.save()
    
    # if the member is known in nation builder...
    extra_fields = []
    member_in_nation_builder = member.nation_builder_id != None
    if member_in_nation_builder:
    
        # get the profile fields
        if member.is_superuser:
            profile_fields = MemberEditableNationBuilderField.objects.order_by('display_order')
        else:
            profile_fields = MemberEditableNationBuilderField.objects.filter(admin_only = False).order_by('display_order')
        
        # get values for the profile fields
        member_fields = nb.PersonFieldsAndValues(member.nation_builder_id)
        for profile_field in profile_fields:
            values = [field[1] for field in member_fields if field[0] == profile_field.field_path]
            if len(values) > 0:
                profile_field.value_string = values[0]
                extra_fields.append(profile_field)
    
    # if valid post...
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance = member, extra_fields = extra_fields)
        if form.is_valid():
            
            # write the member-editable fields
            extra_field_values = form.extra_field_values()
            nb.SetFieldPathValues(member.nation_builder_id, extra_field_values)
            
            # save the member
            form.save()

            messages.success(request, 'Profile saved')
            return redirect("members:profile")      
    else:
        form = MemberProfileForm(instance = member, extra_fields = extra_fields)
    return render(request, 'members/profile.html', { 
        'form': form,
        'email': member.email,
        'member_in_nation_builder': member_in_nation_builder
        })
    
    
    
    
    