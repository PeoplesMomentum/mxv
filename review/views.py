from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Track

@login_required
def index(request):
    template = loader.get_template('review/index.html')
    context = { 'tracks' : Track.objects.all().order_by('display_order') }
    return HttpResponse(template.render(context, request))