from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from rareapi.models import DeactivationQueue, RareUser


class DeactivationQueueView(ViewSet):
    def retrieve(self, request, pk):
        """handles the GET for single deactivationQueues"""
        try:
            admin = RareUser.objects.get(pk = pk)
            
            deactivation_queue = DeactivationQueue.objects.get(admin=admin)
            serializer = DeactivationQueueSerializer(deactivation_queue)
            return Response(serializer.data)
        except DeactivationQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        requester = RareUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateDeactivationQueueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(requester=requester)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            deactivation_queue = DeactivationQueue.objects.get(pk=pk)
            deactivation_queue.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except DeactivationQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class DeactivationQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeactivationQueue
        fields = ('id', 'admin', 'requester')

class CreateDeactivationQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeactivationQueue
        fields = ('id', 'admin')
        