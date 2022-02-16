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

    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        """Post subscription"""

        follower = RareUser.objects.get(pk=request.auth.user.id)
        author = RareUser.objects.get(pk=pk)
        follower.following.add(author)
        return Response({'message': 'Subscription added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        """Delete subscription"""

        follower = RareUser.objects.get(pk=request.auth.user.id)
        author = RareUser.objects.get(pk=pk)
        follower.following.remove(author)

        return Response({'message': 'Subscription deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def admin(self, request, pk):
        """Put request to is_staff"""

        user = User.objects.get(pk=pk)
        user.is_staff = True
        user.save()

        return Response({'message': 'User is now an admin'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def author(self, request, pk):
        """Put request to is_staff"""

        user = User.objects.get(pk=pk)
        admin_list = User.objects.filter(is_staff=True, is_active=True)
        serialized = UserSerializer(admin_list, many=True)

        if len(serialized.data) <= 1 and user.is_staff is True:
            return Response({'message': 'Cannot be changed- this is the only active admin remaining'}, status=status.HTTP_409_CONFLICT)
        else:
            user.is_staff = False
            user.save()
            return Response({'message': 'User is now an author'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def activate(self, request, pk):
        """Put request to active"""

        user = RareUser.objects.get(pk=pk)
        user.active = True
        user.save()

        return Response({'message': 'User has been activated'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def deactivate(self, request, pk):
        """Put request to active"""

        user = RareUser.objects.get(pk=pk)
        admin_list = RareUser.objects.filter(user__is_staff=True, active=True)
        serialized = RareUserSerializer(admin_list, many=True)

        if len(serialized.data) <= 1 and user.user.is_staff is True:
            return Response({'message': 'Cannot be changed- this is the only active admin remaining'}, status=status.HTTP_409_CONFLICT)
        else:
            user.active = False
            user.save()
            return Response({'message': 'User has been deactivated'}, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = User
        depth = 1
        fields = 'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'date_joined'


class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """

    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = 'id', 'bio', 'profile_image_url', 'user', 'following', 'followers', 'active'
