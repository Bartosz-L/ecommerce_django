import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # get nonce token
        nonce = request.POST.get('payment_method_nonce', None)
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()

        context = {'order': order, 'client_token': client_token}
        return render(request, 'payment/process.html', context=context)


def payment_done(request):
    return render('payment/done.html')


def payment_canceled(request):
    return render('payment/canceled.html')
