from django.contrib import admin
from review.models import Track, Theme, Proposal, Comment, ModerationRequest, ModerationRequestNotification, Amendment
from django.urls.base import reverse
from django.utils.safestring import mark_safe

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
     
# moderation request admin
class ModerationRequestAdmin(admin.ModelAdmin):
    search_fields = ('reason',)
    list_display = ('reason', 'requested_by', 'moderated_entity_created_by', 'moderated')
    readonly_fields = ('moderated_entity_type', 'entity_link', 'moderated_entity_created_by', 'requested_by', 'requested_at', 'reason')
    exclude = ('proposal', 'amendment', 'comment')
    
    def moderated_entity_type(self, obj):
        if obj.proposal:
            return 'proposal'
        if obj.amendment:
            return 'amendment'
        if obj.comment:
            return 'comment'
    
    def entity_link(self, obj):
        entity_href = ''
        entity_text = ''
        if obj.proposal:
            entity_href = reverse('admin:review_proposal_change', args=(obj.proposal.pk,))
            entity_text = obj.proposal.short_text()
        if obj.amendment:
            entity_href = reverse('admin:review_amendment_change', args=(obj.amendment.pk,))
            entity_text = obj.amendment.short_text()
        if obj.comment:
            entity_href = reverse('admin:review_comment_change', args=(obj.comment.pk,))
            entity_text = obj.proposal.short_text()
        return mark_safe('<a href="{}">{}</a>'.format(entity_href, entity_text))
    
    entity_link.short_description = 'moderated entity text'
     
# registration
admin.site.register(Track, TrackAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Amendment)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ModerationRequest, ModerationRequestAdmin)
admin.site.register(ModerationRequestNotification)
