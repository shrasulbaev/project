from os import name

from .models import Order, OrderItem, Comment, Like, Product, Category, Favorites
from .serializers import CreateOrderItemSerializer, OrderSerializer, OrderItemSerializer, CommentSerializer, \
    LikeSerializer, ProductSerializer, CategorySerializer, FavoritesSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

class OrderItemCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = CreateOrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order_item = serializer.save()
        message = "Вы успешно оформили заказ. Ожидайте прибытия курьера."
        return {"message": message, "order_item": OrderItemSerializer(order_item).data}


class OrderCreateListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = "Заказ успешно создан."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        message = "Корзина успешно получена."
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Корзина успешно обновлена."
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Корзина успешно удалена."
        return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        message = "Комментарий успешно создан."
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Комментарий успешно обновлен."
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Комментарий успешно удален."
        return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)


class LikeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = "Лайк успешно создан."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class LikeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Лайк успешно обновлен."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Лайк успешно удален."
        return Response({"message": message})


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductCommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Comment.objects.filter(product_id=product_id)


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = "Товар успешно создан."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    from django.shortcuts import render


    def create_product(request, price=None):
        if request.method == 'POST':
            # Получение данных для создания продукта из запроса

            try:
                # Создание продукта
                product = Product.objects.create(name=name, price=price)

                # Логирование успешного создания продукта
                logger.info('Продукт успешно создан: %s', product.name)

                # Возвращение успешного ответа
                return render(request, 'success.html', {'message': 'Продукт успешно создан.'})
            except Exception as e:
                # Логирование ошибки при создании продукта
                logger.error('Ошибка при создании продукта: %s', str(e))

                # Возвращение ошибочного ответа
                return render(request, 'error.html', {'message': 'Ошибка при создании продукта.'})

        # Обработка GET запроса или других методов
        return render(request, 'create_product.html')


class CategoryCreateListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = "Категория успешно создана."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class ProductUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Товар успешно обновлен."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Товар успешно удален."
        return Response({"message": message})

    def perform_destroy(self, instance):
        instance.delete()


class FavoritesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.query_params.get('is_favorite') == 'true':
            return self.queryset.filter(is_favorite=True)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = "Товар успешно добавлен в избранное."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class FavoritesRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = "Избранный товар успешно обновлен."
        response_data = {
            "message": message,
            "data": serializer.data
        }
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = "Избранный товар успешно удален."
        return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)