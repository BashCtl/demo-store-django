from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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