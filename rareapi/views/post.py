from django.forms import ValidationError
from rareapi.models import Post, RareUser
from django.contrib.auth.models import User
from rareapi.models.post_reaction import PostReaction
from rareapi.views.rare_user import RareUserSerializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.files.base import ContentFile
import uuid
import base64



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
        category = request.query_params.get('category_id', None)
        author = request.query_params.get('user_id', None)
        tag = request.query_params.get('tag_id', None)
        title = request.query_params.get('q', None)
        approved = request.query_params.get('approved', None)
        if title is not None:
            posts = posts.filter(title__icontains=f"{title}")
        if category is not None:
            posts = posts.filter(category_id=category)
        if author is not None:
            posts = posts.filter(user_id=author)
        if tag is not None:
            posts = posts.filter(tags=tag)
        if approved is not None:
            posts = posts.filter(approved=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        try:

            serializer = CreatePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            format, imgstr = request.data["image_url"].split(';base64,')
            ext = format.split('/')[-1]
            imgdata = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            post = serializer.save(user=user, image_url=imgdata)
            if request.auth.user.is_staff == 1:
                post = serializer.save(approved=True)
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
        
    @action(methods=['put'], detail=True)
    def edit_tags(self, request, pk):
        """Put request to is_staff"""

        post = Post.objects.get(pk=pk)
        post.tags.set(request.data)
        post.save()

        return Response({'message': 'Tags have been edited'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def approve(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.approved = True
        post.save()
        return Response({'message': 'Post has been approved by admin'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['put'], detail=True)
    def unapprove(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.approved = False
        post.save()
        return Response({'message': 'Post has been unapproved by admin'}, status=status.HTTP_204_NO_CONTENT)

class PostSerializer(serializers.ModelSerializer):
    # event_count = serializers.IntegerField(default=None)
    # user_event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Post
        fields = ['id', 'postreaction_set', 'title', 'publication_date', 'image_url', 'content', 'tags', 'category', 'user', 'approved']
        depth = 3

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'publication_date', 'content', 'tags', 'category']
