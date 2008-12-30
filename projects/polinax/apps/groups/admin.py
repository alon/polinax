from django.contrib import admin
from groups.models import AssociatedContent, Membership, Role

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'joined', 'karma_score', 'away')

class InlineMembers(admin.TabularInline):
    model = Membership

admin.site.register(Membership, MembershipAdmin)
admin.site.register(AssociatedContent)
admin.site.register(Role)
