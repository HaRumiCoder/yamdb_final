import secrets
import string

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from reviews.models import Category, Genre, Title, User, Review
from api.permissions import (IsAdminUserPermission, ReadOnly,
                             CreateCommentOrRewiewPermission)
from api.serializer import (CategorySerializer, CommentSerializer,
                            CreateTokenSerializer, CreateUserSerializer,
                            GenreSerializer, ReviewSerializer,
                            UserMeSerializer, UserSerializer,
                            ReadTitleserializer, WriteTitleSerializer)
from api.viewsets import ListOrCreateOrDeleteViewsSet
from api.filters import TitleFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUserPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('date_joined',)


class CategoryViewSet(ListOrCreateOrDeleteViewsSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnly | IsAdminUserPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ('id',)


class GenreViewSet(ListOrCreateOrDeleteViewsSet):
    permission_classes = [ReadOnly | IsAdminUserPermission]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    permission_classes = [ReadOnly | IsAdminUserPermission]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,
                       TitleFilterBackend)
    filterset_fields = ('year',)
    ordering_fields = ('id',)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return WriteTitleSerializer
        return ReadTitleserializer


class UserMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        username = self.request.user.username
        obj = get_object_or_404(self.queryset, username=username)
        self.check_object_permissions(self.request, obj)
        return obj


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            alphabet = string.ascii_letters + string.digits
            confirmation_code = ''.join(
                secrets.choice(alphabet) for i in range(15))
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            send_mail(
                'Код подтверждения регистрации YAMDB',
                f'Код подтверждения для пользователя <<{username}>>:'
                f' {confirmation_code}',
                '',
                (email,),
            )
            serializer.save(confirmation_code=confirmation_code)
            return Response(
                serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(generics.CreateAPIView):
    serialiser_class = CreateTokenSerializer

    def post(self, request):
        serializer = CreateTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data.get('username'))
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CreateCommentOrRewiewPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [CreateCommentOrRewiewPermission]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
