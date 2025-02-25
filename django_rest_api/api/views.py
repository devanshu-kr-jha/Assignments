from rest_framework import viewsets, status
from api.serializers import UserSerializer
from api.models import User
from api.pagination import CustomPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.filters import UserFilter


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()

        # applying filters
        filterset = UserFilter(request.GET, queryset=users)
        if filterset.is_valid():
            users = filterset.qs

        # paginating results
        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)

        # sorting results
        sort_field = request.GET.get("sort", None)
        if sort_field:
            print(sort_field)
            users = users.order_by(sort_field)

        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
