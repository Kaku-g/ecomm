from django import template
from store.models import Order,Cart



register = template.Library()



@register.filter
def cart_total(user):
    order= Order.objects.filter(user=user,ordered=False)
    num=0
    if order.exists():
        order_item= Order.objects.filter(
            user=user
        )[0]
        #return order_item

        quantity=0
        orders=  order[0].orderitems.filter(purchased=False)
        for item in orders:
            quantity+= item.quantity

        return quantity
       # return order[0].orderitems.quantity

    else:
        return 0
