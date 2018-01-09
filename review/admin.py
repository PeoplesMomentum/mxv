from django.contrib import admin
from review.models import Track, Theme

# themes in a track
class ThemeInline(admin.TabularInline):
    model = Theme
    extra = 0

# track admin
class TrackAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description', 'display_order', )
    inlines = (ThemeInline,)
    
    def get_queryset(self, request):
        qs = super(TrackAdmin, self).get_queryset(request)
        return qs.order_by('display_order')
    
# theme admin
class ThemeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description', 'track', 'display_order', )
    
    def get_queryset(self, request):
        qs = super(ThemeAdmin, self).get_queryset(request)
        return qs.order_by('track__display_order', 'display_order')
     
# registration
admin.site.register(Track, TrackAdmin)
admin.site.register(Theme, ThemeAdmin)