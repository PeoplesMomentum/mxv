# returns the default template context
from mxv.settings import SITE_NAME_SHORT, SITE_NAME_LONG
def default(request):
    return { 
        'site_name_short': SITE_NAME_SHORT,
        'site_name_long': SITE_NAME_LONG }