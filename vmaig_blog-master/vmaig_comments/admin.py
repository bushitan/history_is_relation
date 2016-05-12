# -*- coding: utf-8 -*-
from django.contrib import admin
from vmaig_comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'note__title', 'comment')
    list_filter = ('create_time',)
    list_display = ('user', 'note', 'create_time')
    fields = ('user', 'note', 'comment')

admin.site.register(Comment, CommentAdmin)
