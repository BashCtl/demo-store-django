from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Cart

def get_pagination(item_list, page):
    paginator = Paginator(item_list, 8)
    try:
        item_pagination = paginator.page(page)
    except PageNotAnInteger:
        item_pagination = paginator.page(1)
    except EmptyPage:
        item_pagination = paginator.page(paginator.num_pages)
    return item_pagination

def items_for_page(pagination):
    return [pagination.object_list[i:i+4] for i in range(0, len(pagination.object_list), 4)]

def get_cart_data(request):

    if request.user.is_authenticated:
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, complete=False)
        items = cart.items.all()
        cart_items = cart.get_cart_items
        print(cart_items)
        print(cart.get_total)
        return {'items': items, 'cart_items': cart_items, 'cart': cart}
    return {}