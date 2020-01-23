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
        # Payment successful.
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        # Mark order as paid.
        order.paid = True
        order.save()

        # Create email containing invoice.
        subject = 'Mój sklep - rachunek nr {}'.format(order.id)
        message = 'W załączniku przesyłamy rachunek dla ostatniego zakupu.'
        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [order.email])

        # Generate PDF file.
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        css = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,
                                               stylesheets=[css,
                                                            "https://fonts.googleapis.com/css?family=Raleway:400,600&display=swap"])
        # Attach PDF file.
        email.attach('order_{}.pdf'.format(order.id),
                     out.getvalue(),
                     'application/pdf')
        # Sending an email.
        email.send()

        valid_ipn_received.connect(payment_notification)
