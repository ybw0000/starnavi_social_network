from drf_yasg.openapi import FORMAT_DATE
from drf_yasg.openapi import IN_QUERY
from drf_yasg.openapi import Parameter
from drf_yasg.openapi import TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Like
from posts.models import Post
from posts.serializers import AnalyticsQueryParamsSerializer
from posts.serializers import PostSerializer
from posts.swagger_schemas import liked_response_schema
from posts.swagger_schemas import not_found_response_schema
from posts.swagger_schemas import unliked_response_schema


class CreateListPostView(CreateAPIView, ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description='Get list of posts',
        tags=['posts'],
        security=[],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description='Create a post',
        tags=['posts'],
        security=[{'Bearer': []}],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrievePostView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['posts'],
        security=[],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LikePostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    queryset = Post.objects.all()

    @swagger_auto_schema(
        responses={
            201: liked_response_schema,
            200: unliked_response_schema,
            404: not_found_response_schema,
        }
    )
    def patch(self, request, *args, **kwargs):
        post = get_object_or_404(Post.objects.all(), pk=kwargs['pk'])
        user = request.user

        existing_like = Like.objects.filter(post=post, user=user).first()
        if existing_like:
            existing_like.delete()
            return Response({'message': 'Unliked.'}, status=status.HTTP_200_OK)

        Like.objects.create(post=post, user=user)
        return Response({'message': 'Liked.'}, status=status.HTTP_201_CREATED)


class AnalyticsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            Parameter(
                'date_from', IN_QUERY, description='Start date for analytics', type=TYPE_STRING, format=FORMAT_DATE
            ),
            Parameter('date_to', IN_QUERY, description='End date for analytics', type=TYPE_STRING, format=FORMAT_DATE),
        ]
    )
    def get(self, request: Request, *args, **kwargs):
        serializer = AnalyticsQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        date_from = serializer.validated_data.get('date_from')
        date_to = serializer.validated_data.get('date_to')

        result = [
            {'date': item['created_at__date'], 'likes_count': item['likes_count']}
            for item in Like.get_likes_in_date_range(date_from, date_to)
        ]

        return Response(result, status=status.HTTP_200_OK)
