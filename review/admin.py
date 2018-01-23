from django.contrib import admin
from review.models import Track, Theme, Proposal, Comment

# themes in a track
class ThemeInline(admin.TabularInline):
    model = Theme
    extra = 0

# track admin
class TrackAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'display_order', )
    inlines = (ThemeInline,)
    
    def get_queryset(self, request):
        qs = super(TrackAdmin, self).get_queryset(request)
        return qs.order_by('display_order')
    
# theme admin
class ThemeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'guidance', )
    list_display = ('name', 'description', 'guidance', 'track', 'display_order', )
    
    def get_queryset(self, request):
        qs = super(ThemeAdmin, self).get_queryset(request)
        return qs.order_by('track__display_order', 'display_order')
    
# proposal admin
class ProposalAdmin(admin.ModelAdmin):
    search_fields = ('name', 'text',)
    list_display = ('name', 'theme', )
    
# comment admin
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('short_text', 'proposal', )
     
# registration
admin.site.register(Track, TrackAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Comment, CommentAdmin)
