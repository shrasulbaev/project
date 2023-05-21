from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.db import models
from shashop.models import OrderItem, Product
from telegram_bot import send_message_to_telegram


# @receiver(m2m_changed, sender=Order.products.through)
def update_product_count(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove':
        # После добавления или удаления товаров из заказа
        product_ids = instance.products.values_list('id', flat=True)
        count = instance.products.count()

        # Обновление количества товара на складе
        Product.objects.filter(id__in=product_ids).update(count_product=count)



@receiver(post_save, sender=OrderItem)
def send_order_item_to_telegram(sender, instance, created, **kwargs):
    if created:
        # Соберите текст сообщения с информацией о заказе
        message = f"Новый ордер-айтем:\nАдрес: {instance.address}\nРегион: {instance.region}"

        # Отправьте сообщение в телеграм-бот
        send_message_to_telegram(message)
