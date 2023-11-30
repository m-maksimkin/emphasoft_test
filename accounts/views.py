from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': str(user.auth_token),
            },
            status=status.HTTP_201_CREATED,
        )

