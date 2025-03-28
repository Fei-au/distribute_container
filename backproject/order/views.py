from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import random
import os
from order.tasks import send_email
from pubsub.pub import publish_messages


PUBLISHER_ID = os.getenv('PUBLISHER_ID', 'publisher1')

# Create your views here.

def generate_uid():
    return str(random.randint(1000, 9999))

def order(request):
    return HttpResponse("Hello, world. You're at the order index.")

def order_list(request):
    l = cache.get('order_list')
    return HttpResponse(f"Order list: {l}")

def order_detail(request, order_id):
    data = cache.get(str(order_id))
    if data is None:
        return HttpResponse("Order not found")
    return HttpResponse(f"Order {order_id}: name={data['name']}, item={data['item']}")

def add_order(request):
    # write to redis
    name = request.GET.get('name')
    item = request.GET.get('item')
    uid = generate_uid()
    data = {
        'uid': uid,
        'name': name,
        'item': item
    }
    cache.set(uid, data)
    l = cache.get('order_list')
    if l is None:
        l = []
    l.append(uid)
    cache.set('order_list', l)
    # send_email.delay(uid, f"Order {uid} added")
    publish_messages(PUBLISHER_ID, uid, f"Order {uid} added")
    return HttpResponse(f"Order added with ID: {uid}")

def delete_order(request):
    # delete from redis
    uid = request.GET.get('uid')
    cache.delete(uid)
    l = cache.get('order_list')
    if l is not None:
        l.remove(uid)
        cache.set('order_list', l)
    else:
        return HttpResponse("Delete order not found")
    publish_messages(PUBLISHER_ID, uid, f"Order {uid} deleted")
    return HttpResponse("Order deleted")

def update_order(request):
    # update redis
    uid = request.GET.get('uid')
    old_data = cache.get(uid)
    if old_data is None:
        return HttpResponse("Update order not found")
    item = request.GET.get('item')
    data = {
        'uid': uid,
        'name': old_data['name'],
        'item': item
    }
    cache.set(uid, data)
    # send_email.delay(uid, f"Order {uid} updated")
    publish_messages(PUBLISHER_ID, uid, f"Order {uid} updated")
    return HttpResponse("Order updated")
