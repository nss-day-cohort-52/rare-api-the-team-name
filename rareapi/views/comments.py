from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment

class CommentView(ViewSet):
    def list (self, request):
        """handles the GET all for comments"""
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """handles the GET for single comments"""
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model: Comment
        fields = ('id', 'content', 'created_on', 'author', 'post')