from django.urls import path
from .views import resource_list_view, resource_upload_view, topic_list_view, topic_detail_view


urlpatterns = [
    # Resources
    path('resources/', resource_list_view, name='resource_list'),
    path('resources/upload/', resource_upload_view, name='resource_upload'),

    # Discussions
    path('forum/', topic_list_view, name='topic_list'),
    path('forum/<int:topic_id>/', topic_detail_view, name='topic_detail'),
]