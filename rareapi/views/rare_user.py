"""View module for handling requests about user"""
from django.contrib.auth.models import User
from rareapi.models import RareUser
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class RareUserView(ViewSet):
    """Trove user view"""

    def list(self, request):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """

        users = RareUser.objects.all()
        serializer = RareUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """

        try:
            rareUser = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rareUser)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def current(self, request):
        """Only get actors back that are currently active on a book"""

        rare_user = RareUser.objects.get(user=request.auth.user)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = User
        depth = 1
        fields = 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """

    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = 'id', 'bio', 'profile_image_url', 'user'