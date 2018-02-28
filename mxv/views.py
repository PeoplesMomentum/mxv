from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.views import PasswordResetView
from .settings import SITE_NAME_SHORT, SITE_NAME_LONG, ALLOW_ERROR_URL
from django.http import Http404
from mxv.settings import TRACK_VOTING_VISIBLE_TO_NON_STAFF


# landing page
def index(request):
    template = loader.get_template('mxv/index.html')
    context = {'show_voting': TRACK_VOTING_VISIBLE_TO_NON_STAFF or request.user.is_staff,}
    return HttpResponse(template.render(context, request))

# pass the site names to the password reset context
class ExtraContextPasswordResetView(PasswordResetView):
    extra_email_context = {
         'site_name_short': SITE_NAME_SHORT,
         'site_name_long': SITE_NAME_LONG,
         }

# raises an error if allowed
def error(request):
    if ALLOW_ERROR_URL:
        raise Exception('error test')
    else:
        raise Http404('not found')
        
