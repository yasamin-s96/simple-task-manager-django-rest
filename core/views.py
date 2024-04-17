from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from .serializers import BaseUserInfoSerializer, UserProfileSerializer
from .models import User, Profile


class UserProfileView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(instance=request.user.profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



