from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from users.models import User, MemberActivationEmail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin import site
from .forms import MemberActivationEmailForm

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
def member_activation_email(request):
    
    # get the singleton activation email
    member_activation_email = MemberActivationEmail.get_solo()
    
    # if a post...
    if request.method == 'POST':
        
        # .. and the form is valid...
        form = MemberActivationEmailForm(request.POST)
        if form.is_valid():
            
            # update the member email
            member_activation_email.subject = form.cleaned_data['subject']
            member_activation_email.content = form.cleaned_data['content']
            member_activation_email.save()
            
        # redirect
        return HttpResponseRedirect('/admin/member_activation_email')
    else:
        # it's a get so populate the form with the current activation email
        form = MemberActivationEmailForm(instance = member_activation_email)
        
    # add the form to the django admin context
    context = site.each_context(request)
    context['form'] = form
    
    # render the page
    return render(request, 'users/member_activation_email.html', context)

