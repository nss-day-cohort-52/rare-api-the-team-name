from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from rareapi.models import Post, RareUser, Subscription


class PostView(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
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
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = CreatePostSerializer(post, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
        user_subscriptions = Subscription.objects.filter(
            follower=rare_user).values()
        
        post_list = []
        
        for subscription in user_subscriptions:
            posts = Post.objects.filter(user__pk=subscription['author_id']).values()
            new_posts = PostSerializer(posts, many=True)
            post_list.append(new_posts.data)
            
        flat_list = [item for sublist in post_list for item in sublist]

        return Response(flat_list)


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
        fields = ['title', 'publication_date',
                  'image_url', 'content', 'approved']
