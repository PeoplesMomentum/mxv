from django.http.response import HttpResponse, HttpResponseForbidden
from users.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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
    