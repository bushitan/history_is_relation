from django.conf.urls import url
from vmaig_comments.views import CommentControl,UploadView


urlpatterns = [
        # url(r'^comment/(?P<slug>\w+)$', CommentControl.as_view()),
        url(r'^upload/(?P<slug>\w+)$', UploadView.as_view()),
        url(r'^comment/(?P<note_id>\w+)/(?P<story_id>\w+)$', CommentControl.as_view()),
]
