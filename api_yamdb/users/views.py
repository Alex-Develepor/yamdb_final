from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import UserIsAdmin, UserIsSuperuser
from .serializers import (ConfirmationCodeSerializer, MeSerializer,
                          RegistrationSerializer, UserOutSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserIsAdmin | UserIsSuperuser]
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        user = request.user
        user = get_object_or_404(User, username=user.username)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['POST'])
def signup(request):
    """Регистрация нового пользователя и отправка кода на почту."""
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Регистрация',
        f'Проверочный код: {confirmation_code}',
        'Yamdb@mail.ru',
        [email])
    user_serializer = UserOutSerializer(user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Проверка кода и отправка токена."""
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data['username']
    )
    confirmation_code = serializer.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        data={'error': 'Ошибка отправки кода подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )
