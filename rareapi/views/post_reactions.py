from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from rareapi.models import PostReaction


class PostReactionView(ViewSet):
    def list (self, request):
        """handles the GET all for Postreactions"""
        postReactions = PostReaction.objects.all()
        serializer = PostReactionSerializer(postReactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles the GET for single Postreactions"""
        try:
            postReactions = PostReaction.objects.get(pk=pk)
            serializer = PostReactionSerializer(postReactions)
            return Response(serializer.data)
        except PostReaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        
        try:
            serializer = CreatePostReactionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            postReactions = PostReaction.objects.get(pk=pk)
            serializer = CreatePostReactionSerializer(postReactions, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        postReactions = PostReaction.objects.get(pk=pk)
        postReactions.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction')

class CreatePostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('user', 'post', 'reaction')