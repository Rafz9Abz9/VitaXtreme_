from django.http import HttpResponse
from django_currentuser.middleware import (get_current_authenticated_user)
import time

from .models import Order, OrderLineItem
from cart import context_processors


class StripeWH_Handler:
    """Handle Stripe Webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """handles a generic/ unknown/unexpected webhook event"""

        return HttpResponse(
            content=f"unhandled Webhook received: {event["type"]}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event, request):
        """handles payment_intent.succeeded webhook from stripe"""

        intent = event.data.object
        pid = intent.id

        order_exist = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid__iexact=pid,
                    first_name__iexact=intent.metadata.first_name,
                    last_name__iexact=intent.metadata.last_name,
                    email__iexact=intent.metadata.email,
                    phone__iexact=intent.metadata.phone,
                    post_code__iexact=intent.metadata.post_code,
                    street_address__iexact=intent.metadata.street_address,
                    city__iexact=intent.metadata.city,
                    state__iexact=intent.metadata.state,
                    country__iexact=intent.metadata.country,
                    shipping_method__iexact=intent.metadata.shipping_method,
                    shipping_price__iexact=intent.metadata.shipping_price,
                    sub_total__iexact=intent.metadata.sub_total,
                    grand_total__iexact=intent.metadata.grand_total,
                )

                order_exist = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exist:
            return HttpResponse(
                content=f" Webhook received: {event["type"]}",
                status=200
            )
        else:
            order = None
            try:
                context = context_processors.cart_item(request)
                full_cart_item = context['full_cart_item']

                user = get_current_authenticated_user()

                order = Order.objects.create(
                    stripe_pid=pid,
                    first_name=intent.metadata.first_name,
                    last_name=intent.metadata.last_name,
                    email=intent.metadata.email,
                    phone=intent.metadata.phone,
                    post_code=intent.metadata.post_code,
                    street_address=intent.metadata.street_address,
                    city=intent.metadata.city,
                    state=intent.metadata.state,
                    country=intent.metadata.country,
                    shipping_method=intent.metadata.shipping_method,
                    shipping_price=intent.metadata.shipping_price,
                    sub_total=intent.metadata.sub_total,
                    grand_total=intent.metadata.grand_total,
                )
                if user:
                    order.user_id = user.id
                    order.save()
                for item in full_cart_item:
                    if item.product.quantity < int(item.quantity):
                        order.delete()
                        return HttpResponse(
                            content=f" Webhook received: {event["type"]} | {
                                item.product.name} is out of stock ",
                            status=403)

                    order_line_item = OrderLineItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f" Webhook received: {event["type"]} | ERROR:{e}",
                    status=500)

        return HttpResponse(
            content=f" Webhook received: {
                event["type"]} | SUCCESS: Created order in webhook",
            status=200
        )

    def handlefi_payment_intent_payment_failed(self, event):
        """handles payment_intent.failed webhook from stripe"""

        return HttpResponse(
            content=f"Webhook recieved: {event["type"]}",
            status=200
        )
