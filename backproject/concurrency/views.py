from django.shortcuts import render
import time
from django.http import HttpResponse, HttpResponseServerError
import os
import requests
import httpx
# Create your views here.

def index(request):
    return HTTPResponse("Hello Concurrency Test!")


request_count = {}
def testcpu(request):
    pid = os.getpid()
    count = 0
    start = time.time()
    for i in range(10000000):
        count += 1
    end = time.time()
    if not request_count.get('pid'):
        request_count[pid] = 1
    else:
        request_count[pid] += 1
    time_used = (end - start) * 1000
    return HttpResponse(f"pid: {pid}, request count: {request_count[pid]}, time: {time_used:.2f}ms")

def testio(request):
    pid = os.getpid()
    response = requests.get("https://httpbin.org/delay/1")
    start = time.time()
    if not request_count.get('pid'):
        request_count[pid] = 1
    else:
        request_count[pid] += 1
    end = time.time()
    if not request_count.get('pid'):
        request_count[pid] = 1
    else:
        request_count[pid] += 1
    return HttpResponse(f"pid: {pid}, request count: {request_count[pid]}, time: {end - start:.2f}ms")

async def testasynccpu(request):
    pid = os.getpid()
    count = 0
    start = time.time()
    for i in range(10000000):
        count += 1
    end = time.time()
    if not request_count.get('pid'):
        request_count[pid] = 1
    else:
        request_count[pid] += 1
    time_used = (end - start) * 1000
    return HttpResponse(f"pid: {pid}, request count: {request_count[pid]}, time: {time_used:.2f}ms")

async def testasyncio(request):
    try:
        pid = os.getpid()
        url = "https://httpbin.org/delay/1"  # responds after 5 seconds
        start = time.time()
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.get(url)
        end = time.time()
        if not request_count.get('pid'):
            request_count[pid] = 1
        else:
            request_count[pid] += 1
        return HttpResponse(f"pid: {pid}, request count: {request_count[pid]}, time: {end - start:.2f}ms")
    except Exception as e:
        return HttpResponseServerError(str(e))
