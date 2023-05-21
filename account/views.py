from rest_framework.response import Response
from .models import User
from .serializer import UserRegisterSerializer
from rest_framework import generics, status, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.db.models import Q


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'status': 201,
            'Сообщение': 'Пользователь успешно создан'
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class UserAuthorization(APIView):
    def post(self, request):
        email_or_phone_number = request.data.get('email_or_phone_number')
        password = request.data.get('password')
        user = User.objects.filter(Q(email=email_or_phone_number) | Q(phone_number=email_or_phone_number)).first()
        if user is not None and user.is_active and user.check_password(password):
            if user.access:
                return Response({'Сообщение': 'У вас нет доступа к данному ресурсу'},
                                status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response({'Сообщение': 'Вы успешно вошли в свой аккаунт!'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'Сообщение': 'Неверный email, номер телефона или пароль'},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response({'Сообщение': 'Вы успешно вышли из своего аккаунта.'}, status=status.HTTP_200_OK)
