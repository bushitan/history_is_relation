# -*- coding: utf-8 -*-
from django.contrib import admin
from vmaig_comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'story__title', 'comment')
    list_filter = ('create_time',)
    list_display = ('user', 'story', 'create_time')
    fields = ('user', 'story', 'comment')

admin.site.register(Comment, CommentAdmin)
