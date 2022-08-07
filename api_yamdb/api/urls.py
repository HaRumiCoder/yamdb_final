from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, CreateTokenView,
                       CreateUserView, GenreViewSet, ReviewViewSet,
                       TitlesViewSet, UserMeView, UserViewSet)

app_name = 'api'


router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/token/', CreateTokenView.as_view()),
    path('v1/users/me/', UserMeView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('', include(router_v1.urls)),
]
