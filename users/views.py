from django.http.response import HttpResponse, HttpResponseForbidden
from users.models import User, MemberActivationEmail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin import site

# creates an inactive user for the email and name
@csrf_exempt
def create_inactive_user(request):
    try:
        if request.method == 'POST' and request.POST['secret'] == settings.CREATE_INACTIVE_USER_SECRET:
            User.objects.create_user(email = request.POST['email'], name = request.POST['name'])
            return HttpResponse(content = 'Created inactive user for ' + request.POST['email'])
        else:
            return HttpResponseForbidden()
    except (KeyError):
        return HttpResponseForbidden()

@staff_member_required
def member_activation(request):
    if request.method == 'POST':
        member_activation_email = MemberActivationEmail.get_solo()
        member_activation_email.subject = request.POST['subject']
        member_activation_email.content = request.POST['content']
        member_activation_email.save()
    return render(request, 'users/member_activation.html', site.each_context(request))