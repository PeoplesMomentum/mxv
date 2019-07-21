# returns the default template context
from mxv.settings import SITE_NAME_SHORT, SITE_NAME_LONG, JOIN_URL, PROFILES_VISIBLE_TO_NON_STAFF
def default(request):
    return { 
        'site_name_short': SITE_NAME_SHORT,
        'site_name_long': SITE_NAME_LONG,
        'join_url': JOIN_URL,
        'profiles_visible_to_non_staff': PROFILES_VISIBLE_TO_NON_STAFF
        }