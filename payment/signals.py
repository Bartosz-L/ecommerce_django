from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Płatność zakończyła się powodzeniem.
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        # Oznaczenie zamówienia jako opłaconego.
        order.paid = True
        order.save()

        # Utworzenie wiadomości e-mail zawierającej rachunek.
        subject = 'Mój sklep - rachunek nr {}'.format(order.id)
        message = 'W załączniku przesyłamy rachunek dla ostatniego zakupu.'
        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [order.email])

        # Wygenerowanie dokumentu PDF.
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=stylesheets)
        # Dołączenie pliku w formacie PDF.
        email.attach('order_{}.pdf'.format(order.id),
                     out.getvalue(),
                     'application/pdf')
        # Wysłanie wiadomości e-mail.
        email.send()


valid_ipn_received.connect(payment_notification)
