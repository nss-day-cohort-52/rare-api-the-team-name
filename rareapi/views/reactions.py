from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from rareapi.models import Reaction


class ReactionView(ViewSet):
    def list (self, request):
        """handles the GET all for reactions"""
        reactions = Reaction.objects.order_by('label')
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """handles the GET for single reactions"""
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(reaction)
            return Response(serializer.data)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        
        try:
            serializer = CreateReactionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            post_reaction = Reaction.objects.get(pk=pk)
            serializer = CreateReactionSerializer(post_reaction, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post_reaction = Reaction.objects.get(pk=pk)
        post_reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')

class CreateReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('label', 'image_url')
        