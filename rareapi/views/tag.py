from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag


class TagView(ViewSet):
    def retrieve(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        

    def list(self, request):
        tags = Tag.objects.order_by('label')
        label = request.query_params.get('q', None)
        if label is not None:
            tags = tags.filter(label=label)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        try:
            serializer = CreateTagSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = CreateTagSerializer(tag, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')
        
class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['label']