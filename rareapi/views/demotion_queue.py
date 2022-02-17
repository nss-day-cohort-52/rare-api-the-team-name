from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.forms import ValidationError
from rareapi.models import DemotionQueue, RareUser


class DemotionQueueView(ViewSet):
    def retrieve(self, request, pk):
        """handles the GET for single demotionQueues"""
        try:
            admin = RareUser.objects.get(pk=pk)

            demotion_queue = DemotionQueue.objects.get(admin=admin)
            serializer = DemotionQueueSerializer(demotion_queue)
            return Response(serializer.data)
        except DemotionQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        requester = RareUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateDemotionQueueSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(requester=requester)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            demotion_queue = DemotionQueue.objects.get(pk=pk)
            demotion_queue.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except DemotionQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class DemotionQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemotionQueue
        fields = ('id', 'admin', 'requester')


class CreateDemotionQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemotionQueue
        fields = ('id', 'admin')
