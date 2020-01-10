from django.contrib import admin
from.models import Community, Post, PostObject, CommunityMembership

# Register your models here.

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(PostObject)
admin.site.register(CommunityMembership)