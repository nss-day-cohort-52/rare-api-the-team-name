from django.forms import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from rareapi.models import Subscription, RareUser


class SubscriptionView(ViewSet):
    def retrieve(self, request, pk):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateSubscriptionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(follower=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = CreateSubscriptionSerializer(subscription, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('author', )
