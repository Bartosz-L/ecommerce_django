from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order: {order.id}'
    message = f'Greetings, {order.first_name}! You have placed an order in our store. Order ID: {order.id}'
    mail_sent = send_mail(subject, message, 'admin@thisshop.com', [order.email])
    return mail_sent
