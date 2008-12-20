from django.contrib import admin
from projects.models import Project, Topic, Task
from groups.admin import InlineMembers

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'private', 'deleted')
    inlines = [InlineMembers]

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Task)

