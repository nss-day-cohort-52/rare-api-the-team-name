from django.db.models import Count, Q
from django.forms import ValidationError
from rareapi.models import Post, RareUser
from rareapi.views.rare_user import RareUserSerializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class PostView(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.order_by('-publication_date')
        category = request.query_params.get('category', None)
        if category is not None:
            posts = posts.filter(category_id=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        try:
            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            post = serializer.save(user=user)
            post.tags.set(request.data["tags"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = CreatePostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_post = serializer.save()
            updated_post.tags.set(request.data["tags"])
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def subscribed(self, request):
        """Only get posts whose authors are associated with the current user's subscriptions"""

        rare_user = RareUser.objects.get(pk=request.auth.user.id)

        follower = RareUserSerializer(rare_user)

        posts = Post.objects.filter(
            user__pk__in=follower.data['following'])
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostSerializer(serializers.ModelSerializer):
    # event_count = serializers.IntegerField(default=None)
    # user_event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Post
        fields = '__all__'
        depth = 3

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'publication_date', 'image_url', 'content', 'approved', 'tags']
