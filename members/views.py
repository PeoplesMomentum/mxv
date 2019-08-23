from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from members.models import Member, ProfileField, activation_key_default, UpdateDetailsCampaign
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import site
from members.forms import SendMemberActivationEmailsForm, MemberProfileForm, VerifyEmailForm
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
from mxv.simple_email import send_simple_email


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
        form = forms.EmailForm(request.POST)
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
        form = forms.EmailForm()

    return render(request, 'members/request_activation_email.html', { 
        'form': form })

# well-known fields are always displayed on the profile
class WellKnownFields:
    full_name = ProfileField(field_path = 'person.full_name', display_text = 'Full name', field_type = 'Char', required = True, admin_only = False)
    first_name = ProfileField(field_path = 'person.first_name', display_text = 'First name', field_type = 'Char', required = True, admin_only = False)
    last_name = ProfileField(field_path = 'person.last_name', display_text = 'Last name', field_type = 'Char', required = True, admin_only = False)
    login_email = ProfileField(field_path = 'email', display_text = 'Login email', field_type = 'Email', required = True, admin_only = False)
    other_email = ProfileField(field_path = 'person.email', display_text = 'Other email', field_type = 'Email', required = True, admin_only = False)
    
    # sets login email to be a member field instead of a nation builder field
    def __init__(self):
        self.login_email.is_member_field = True
    
    # returns all the well-known fields
    def all(self):
        return [self.full_name, self.first_name, self.last_name, self.login_email, self.other_email]
    
    # returns all the well-known fields' names (in valid field name format)
    def all_names(self):
        names = []
        for field in self.all():
            names.append(field.field_path.replace('.', '__'))
        return names

# returns a mailto link that creates an error email for the member to send    
def error_mailto(name):
    return 'mailto:membership@peoplesmomentum.com?subject=Profile%20error&body=Hi.%0A%0A%20%20I%20tried%20to%20access%20my%20profile%20page%20on%20My%20Momentum%20but%20got%20an%20error%3A%20%22Can%27t%20look%20up%20profile.%22%0A%0A%20%20Can%20you%20help%20please%3F%0A%0AThanks%2C%0A%0A' + name + '.'    

# displays the member's profile page
@login_required
def profile(request):
    
    # redirect if profiles are not visible to this member
    member = request.user
    if not member.is_superuser and not PROFILES_VISIBLE_TO_NON_STAFF:
        return redirect('index')
    
    # build the profile fields from the well-known fields and profile fields
    well_known_fields = WellKnownFields()
    profile_fields = well_known_fields.all()        
    if member.is_superuser:
        profile_fields.extend(ProfileField.objects.all())
    else:
        profile_fields.extend(ProfileField.objects.filter(admin_only = False))
    
    # get the member's nation builder id if required
    nb = NationBuilder()
    if not member.nation_builder_id:
        member.nation_builder_id = nb.GetIdFromEmail(member.email)
        member.save()
    member_in_nation_builder = member.nation_builder_id != None
    
    # if post...
    if request.method == 'POST':
        
        # remove the other email field from the profile fields if the get form was built without it
        if 'hide_other_email' in request.POST:
            profile_fields.remove(well_known_fields.other_email)
            
        # remove the full_name field as it is only there so that nation builder name changes can be detected during a GET
        profile_fields.remove(well_known_fields.full_name)
        
        # if the form is valid...
        form = MemberProfileForm(request.POST, instance = member, profile_fields = profile_fields)
        if form.is_valid():
            
            # get the profile field values
            profile_field_values = form.profile_field_values()

            # replace or use other email
            other_email_choice = ''
            if 'other_email' in request.POST:
                other_email_choice = request.POST.get('other_email')
                if other_email_choice == 'replace_other_with_login':
                    profile_field_values['person.email'] = member.email
                else:
                    member.email = profile_field_values['person.email']

            # write the profile fields and save the member
            nb.SetFieldPathValues(member.nation_builder_id, profile_field_values)
            form.save()

            # messages            
            messages.success(request, 'Profile saved')
            if other_email_choice == 'replace_other_with_login':
                messages.success(request, 'Other email replaced with login email')
            elif other_email_choice == 'use_other_as_login':
                messages.success(request, 'Other email is now your login email as well')
            
            return redirect("members:profile")
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
      
    else:
        # if the member is known in nation builder...
        if member_in_nation_builder:
        
            # get the profile field values             
            profile_fields = nb.GetProfileFieldValues(member, profile_fields)
                
            # update member name here in case first or last name have been edited here or in nation builder
            nb_full_name = [field.value_string for field in profile_fields if field.field_path == well_known_fields.full_name.field_path][0]
            if nb_full_name != member.name and nb_full_name != '':
                member.name = nb_full_name
                member.save()
                    
        form = MemberProfileForm(instance = member, profile_fields = profile_fields)
        
    return render(request, 'members/profile.html', { 
        'form': form,
        'exclude_from_form': well_known_fields.all_names(),
        'hide_other_email': well_known_fields.other_email.value_string == well_known_fields.login_email.value_string,
        'member_in_nation_builder': member_in_nation_builder,
        'error_mailto': error_mailto(member.name)
        })
    
# allows the member to enter a new login email and sends a verification email to it
@login_required
def change_login_email(request):
    member = request.user
    
    # if valid post...
    if request.method == 'POST':
        form = forms.EmailForm(request.POST)
        if form.is_valid():
                        
            # record a single-use verification key and new login email on the member's record
            member.login_email_verification_key = activation_key_default()
            member.new_login_email = form.cleaned_data.get('email')
            member.save()
            
            # send the verification email
            send_simple_email(
                member.new_login_email, 
                'My Momentum - verify your new login email', 
                'Click here to verify your new login email: %s' % request.build_absolute_uri(reverse('members:verify_login_email', kwargs = {'login_email_verification_key': member.login_email_verification_key})))
         
            # redirect to verification email sent page
            return redirect("members:login_email_verification_sent")
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.EmailForm()

    return render(request, 'members/change_login_email.html', { 
        'form': form })    

# tells the member that a verification email has been sent
@login_required
def login_email_verification_sent(request):
    member = request.user
    return render(request, 'members/login_email_verification_sent.html', { 'new_login_email': member.new_login_email})    

# lets the member log in with their new login email
@login_required
def verify_login_email(request, login_email_verification_key):
    verification_key_found = True
    
    # if valid post...
    if request.method == 'POST':
        form = VerifyEmailForm(request = request, data = request.POST)
        if form.is_valid():
            
            # change the login email and clear the key and new email from the member's record
            member = request.user
            member.email = member.new_login_email
            member.new_login_email = None
            member.login_email_verification_key = None
            member.save()
            
            # change the nation builder email
            nb = NationBuilder()
            nb.SetFieldPathValues(member.nation_builder_id, { 'person.email': member.email })
            
            # redirect to profile with a success message
            messages.success(request, 'Login email successfully changed')
            return redirect('members:profile')
                
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # get the member for the verification key
        member = Member.objects.filter(login_email_verification_key = login_email_verification_key).first()
        if member:
            form = VerifyEmailForm(request = request, initial = {'email': member.new_login_email})
        else:            
            verification_key_found = False
            form = VerifyEmailForm()

    return render(request, 'members/verify_login_email.html', { 
        'form': form,
        'verification_key_found': verification_key_found })    

# displays the update details campaign pages
@login_required
def update_details(request, page):
    campaign = UpdateDetailsCampaign.get_solo()
    member = request.user
    page = int(page)
    
    # get the fields for the page
    tags = None
    profile_fields = None
    well_known_fields = WellKnownFields()
    if page == 1:
        # get all the tags
        tags = list(campaign.tags.all())
    elif page == 2:
        # build the profile fields from the well-known full name field and the campaign fields
        profile_fields = list(campaign.fields.all())
        profile_fields.append(well_known_fields.full_name)

    # get the member's nation builder id if required
    nb = NationBuilder()
    if not member.nation_builder_id:
        member.nation_builder_id = nb.GetIdFromEmail(member.email)
        member.save()
    member_in_nation_builder = member.nation_builder_id != None
    
    if request.method == 'GET':
        # if the member is known in nation builder...
        if member_in_nation_builder:
        
            if page == 1:
                # get the tags
                member_tags= nb.GetPersonTags(member.nation_builder_id)
                for tag in tags:
                    tag.value_string = 'True' if tag.tag in member_tags else 'False'
                
            elif page == 2:          
                # get the campaign field values
                profile_fields = nb.GetProfileFieldValues(member, profile_fields)
                    
                # update member name here in case first or last name have been edited here or in nation builder
                nb_full_name = [field.value_string for field in profile_fields if field.field_path == well_known_fields.full_name.field_path][0]
                if nb_full_name != member.name and nb_full_name != '':
                    member.name = nb_full_name
                    member.save()
 
        form = MemberProfileForm(instance = member, profile_fields = profile_fields, tags = tags)
    else:
        if profile_fields:
            # update member name here in case first or last name have been edited here or in nation builder
            # (not redirecting back to here after successful post so can't deal with this in the GET as we do for the profile page)
            nb_full_name = [field.value_string for field in profile_fields if field.field_path == well_known_fields.full_name.field_path][0]
            if nb_full_name != member.name and nb_full_name != '':
                member.name = nb_full_name
                member.save()

            # remove the full_name field as it is only there so that nation builder name changes can be detected during a GET
            profile_fields.remove(well_known_fields.full_name)

        # if the form is valid...
        form = MemberProfileForm(request.POST, instance = member, profile_fields = profile_fields, tags = tags)
        if form.is_valid():
            
            if page == 1:    
                # get the tag values
                tag_values = form.tag_values()
                
                # clear and set the tags
                tags_to_set = []
                tags_to_clear = []
                for tag in tags:
                    if tag_values[tag.tag]:
                        tags_to_set.append(tag.tag)
                    else:
                        tags_to_clear.append(tag.tag)
                if len(tags_to_set) > 0:
                    nb.SetPersonTags(member.nation_builder_id, tags_to_set)
                if len(tags_to_clear) > 0:
                    nb.ClearPersonTags(member.nation_builder_id, tags_to_clear)
                
                # redirect to page 2 (with all GET parameters as-is)
                return redirect('members:update_details', page = 2)
                
                pass
            elif page == 2:
                # get the extra field values
                profile_field_values = form.profile_field_values()
        
                # write the profile fields and save the member
                nb.SetFieldPathValues(member.nation_builder_id, profile_field_values)
                form.save()
            
                # redirect to campaign URL (with all GET parameters as-is)
                return redirect(campaign.redirect_url)
                
        else:
            #show errors
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'members/update_details.html', { 
        'pre_text': campaign.pre(page),
        'post_text': campaign.post(page),
        'form': form,
        'exclude_from_form': [well_known_fields.full_name.field_path.replace('.', '__')],
        'member_in_nation_builder': member_in_nation_builder,
        'error_mailto': error_mailto(member.name),
        'page': page })
    




