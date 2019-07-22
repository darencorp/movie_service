from django.urls import path
from rest_framework.routers import DefaultRouter

from movies.views.comment import CommentViewSet
from movies.views.movie import MovieViewSet, top

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('top/', top, name='top')
]

urlpatterns += router.urls

