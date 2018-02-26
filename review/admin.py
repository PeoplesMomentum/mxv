from django.contrib import admin
from review.models import Track, Theme, Proposal, Comment, ModerationRequest, ModerationRequestNotification, Amendment
from django.urls.base import reverse
from django.utils.safestring import mark_safe

"""
  - search all text fields and created_by name/email for member-created entities
  - list display card fields followed by parent entity as link
  - parent entity as first field
  - group fields 
  - member-created entity fields read-only (this prevents admins from creating these entities, could fix with separate add/change forms?)
"""
    
class TrackAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    list_display = ('name', 'description')
    fields = (
        ('name', 'display_order'),
        'description', 
        ('show_amendments', 'show_comments'),
        ('allow_submissions', 'allow_comments', 'allow_nominations'),
        ('submission_start', 'submission_end'), 
        ('nomination_start', 'nomination_end')
    )
    
    def get_queryset(self, request):
        qs = super(TrackAdmin, self).get_queryset(request)
        return qs.order_by('display_order')

    
class ThemeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'guidance')
    list_display = ('name', 'description', 'track_link')
    fields = (
        'track_link', 
        ('name', 'display_order'),
        'description', 
        'guidance'
    )
    readonly_fields = ('track_link',)
    
    def get_queryset(self, request):
        qs = super(ThemeAdmin, self).get_queryset(request)
        return qs.order_by('track__display_order', 'display_order')
    
    def track_link(self, theme):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:review_track_change', args=(theme.track.pk,)), theme.track.name))
    track_link.short_description = 'track'
    
class ProposalAdmin(admin.ModelAdmin):
    search_fields = ('name', 'summary', 'text', 'created_by__name', 'created_by__email')
    list_display = ('name', 'summary', 'created_by_link', 'created_at', 'theme_link')
    fields = (
        'theme_link',
        ('created_by_link', 'created_at'),
        'name',
        'summary',
        'text'
    )
    readonly_fields = ('theme_link', 'created_by_link', 'created_at', 'name', 'summary', 'text')
    
    def theme_link(self, proposal):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:review_theme_change', args=(proposal.theme.pk,)), proposal.theme.name))
    theme_link.short_description = 'theme'

    def created_by_link(self, proposal):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:members_member_change', args=(proposal.created_by.pk,)), proposal.created_by.email))
    created_by_link.short_description = 'created by'

class AmendmentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'text', 'created_by__name', 'created_by__email')
    list_display = ('name', 'created_by_link', 'created_at', 'proposal_link')
    fields = (
        'proposal_link',
        ('created_by_link', 'created_at'),
        'name',
        'text'
    )
    readonly_fields = ('proposal_link', 'created_by_link', 'created_at', 'name', 'text')
    
    def proposal_link(self, amendment):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:review_proposal_change', args=(amendment.proposal.pk,)), amendment.proposal.name))
    proposal_link.short_description = 'proposal'

    def created_by_link(self, amendment):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:members_member_change', args=(amendment.created_by.pk,)), amendment.created_by.email))
    created_by_link.short_description = 'created by'
     
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text', 'created_by__name', 'created_by__email')
    list_display = ('text', 'created_by_link', 'created_at', 'proposal_link')
    fields = (
        'proposal_link',
        ('created_by_link', 'created_at'),
        'text'
    )
    readonly_fields = ('proposal_link', 'created_by_link', 'created_at', 'text')
    
    def proposal_link(self, comment):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:review_proposal_change', args=(comment.proposal.pk,)), comment.proposal.name))
    proposal_link.short_description = 'proposal'

    def created_by_link(self, comment):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:members_member_change', args=(comment.created_by.pk,)), comment.created_by.email))
    created_by_link.short_description = 'created by'
     
class ModerationRequestAdmin(admin.ModelAdmin):
    search_fields = ('reason', 'requested_by__name', 'requested_by__email')
    list_display = ('reason', 'requested_by_link', 'requested_at', 'moderated_entity_link', 'moderated_entity_created_by_link', 'moderated')
    fields = (
        'moderated_entity_type',
        'moderated_entity_link',
        'moderated_entity_created_by_link',
        ('requested_by_link', 'requested_at'),
        'reason',
        'moderated'
    )
    readonly_fields = ('moderated_entity_type', 'moderated_entity_link', 'moderated_entity_created_by_link', 'requested_by_link', 'requested_at', 'reason')
    
    def moderated_entity_type(self, obj):
        if obj.proposal:
            return 'proposal'
        if obj.amendment:
            return 'amendment'
        if obj.comment:
            return 'comment'
    
    def moderated_entity_link(self, obj):
        entity_href = ''
        entity_text = ''
        if obj.proposal:
            entity_href = reverse('admin:review_proposal_change', args=(obj.proposal.pk,))
            entity_text = obj.proposal.name
        if obj.amendment:
            entity_href = reverse('admin:review_amendment_change', args=(obj.amendment.pk,))
            entity_text = obj.amendment.name
        if obj.comment:
            entity_href = reverse('admin:review_comment_change', args=(obj.comment.pk,))
            entity_text = obj.comment.text
        return mark_safe('<a href="%s">%s</a>' % (entity_href, entity_text)) 
    moderated_entity_link.short_description = 'moderated entity'
     
    def requested_by_link(self, moderationrequest):
        return mark_safe('<a href="%s">%s</a>' % (reverse('admin:members_member_change', args=(moderationrequest.requested_by.pk,)), moderationrequest.requested_by.email))
    requested_by_link.short_description = 'requested by'
     
    def moderated_entity_created_by_link(self, moderationrequest):
        entity_href = ''
        entity_text = ''
        if moderationrequest.proposal:
            entity_href = reverse('admin:members_member_change', args=(moderationrequest.proposal.created_by.pk,))
            entity_text = moderationrequest.proposal.created_by.email
        if moderationrequest.amendment:
            entity_href = reverse('admin:members_member_change', args=(moderationrequest.amendment.created_by.pk,))
            entity_text = moderationrequest.amendment.created_by.email
        if moderationrequest.comment:
            entity_href = reverse('admin:members_member_change', args=(moderationrequest.comment.created_by.pk,))
            entity_text = moderationrequest.comment.created_by.email
        return mark_safe('<a href="%s">%s</a>' % (entity_href, entity_text)) 
    moderated_entity_created_by_link.short_description = 'moderated entity created by'
    
    def response_change(self, request, obj):
        if 'turn_moderation_into_comment' in request.POST:
            moderation = obj
            
            # moderated proposal
            if moderation.proposal:
                moderation.proposal.comments.create(
                    proposal = moderation.proposal, 
                    created_by = moderation.requested_by, 
                    created_at = moderation.requested_at, 
                    text = moderation.reason)
                
            # moderated amendment
            if moderation.amendment:
                moderation.amendment.proposal.comments.create(
                    proposal = moderation.amendment.proposal, 
                    created_by = moderation.requested_by, 
                    created_at = moderation.requested_at, 
                    text = moderation.reason)
                
            # moderated comment
            if moderation.comment:
                moderation.comment.proposal.comments.create(
                    proposal = moderation.comment.proposal, 
                    created_by = moderation.requested_by, 
                    created_at = moderation.requested_at, 
                    text = moderation.reason)

            # delete the moderation
            moderation.delete()
            
        # call the inherited
        return admin.ModelAdmin.response_change(self, request, obj)
     
admin.site.register(Track, TrackAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Amendment, AmendmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ModerationRequest, ModerationRequestAdmin)
admin.site.register(ModerationRequestNotification)
