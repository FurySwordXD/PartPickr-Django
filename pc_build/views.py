from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template import loader
from . import scrapper
from .models import Part, Cart, Order, Shopping_Cart
# Create your views here.
import json

def index(request):
    return render(request, 'index.html', {'user': request.user})

def build(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        parts = {
            "Processor": cart.processor if cart.processor is not None  else None,
            "CPU Cooler": cart.cpu_cooler if cart.cpu_cooler is not None else None,
            "Motherboard": cart.motherboard if cart.motherboard is not None else None,
            "Memory": cart.memory if cart.memory is not None else None,
            "Storage": cart.storage if cart.storage is not None else None,
            "GPU": cart.gpu if cart.gpu is not None else None,
            "Case": cart.case if cart.case is not None else None,
            "PSU": cart.psu if cart.psu is not None else None,
            "OS": cart.os if cart.os is not None else None,
            "Monitor": cart.monitor if cart.monitor is not None else None
        }
        data = []

        for i in ('Processor', 'CPU Cooler', 'Motherboard', 'Memory', 'Storage', 'GPU', 'Case', 'PSU', 'OS', 'Monitor'):
            flag = False
            for block in data:
                if block['part_type'] == i:
                    for part in Part.objects.filter(part_type=i):
                        block['parts'].append({'title': part.title, 'image': part.image, 'currency': part.currency, 'price': str(part.price), 'id': part.id})
                    flag = True
            if not flag:
                l = []
                for part in Part.objects.filter(part_type=i):
                    l.append({'title': part.title, 'image': part.image, 'currency': part.currency, 'price': str(part.price), 'id': part.id})
                data.append({'part_type': i, 'parts': l})

        with open('data.json', 'w') as file:
            json.dump(data, file)

        return render(request, 'build.html', {'user': request.user, 'parts':parts, 'data':data})
    return redirect('/')

def add_part_build(request, part_id):
    if request.user.is_authenticated:
        part = Part.objects.get(id=part_id)
        cart = Cart.objects.get(user=request.user)
        part_type = part.values[part.names.index(part.part_type)]
        print('cart.'+part_type+' = part')
        exec('cart.'+part_type+' = part')
        cart.save()
        print(str(render(request, 'part.html', {'part': part})))
        add_part_shop(request, part_id)
        template = loader.get_template('part.html')
        return JsonResponse({'flag': True, 'html': template.render({'part': part}, request), 'message': 'Added part!' })
    return JsonResponse({'flag': False, 'message': 'Logged out!'})

def remove_part_build(request, part_id):
    if request.user.is_authenticated:
        part = Part.objects.get(id=part_id)
        cart = Cart.objects.get(user=request.user)
        part_type = part.values[part.names.index(part.part_type)]
        print('cart.'+part_type+' = None')
        exec('cart.'+part_type+' = None')
        cart.save()
        remove_part_shop(request, part_id)
        return JsonResponse({'flag': True, 'message': 'Removed part'})
    return JsonResponse({'flag': False, 'message': 'Logged out!'})

def scrape(request, part_type, pages):
    data = scrapper.scrape(part_type, pages)
    parts = Part.objects.filter(part_type=part_type)
    print(len(parts))
    for i in data:
        flag = False
        for part in parts:
            if i['Title'] == part.title:
                part.currency = i['Currency']
                part.price = i['price']
                flag = True
        if not flag:
            new_part = Part(part_type=part_type, title=i['Title'], image=i['Img_Src'], price=i['Price'], currency=i['Currency'])
            new_part.save()
    print(len(Part.objects.filter(part_type=part_type)))
    return HttpResponse(data)

def orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        data = []
        for order in orders:
            parts = []
            for part in order.parts.all():
                parts.append(part)
            data.append({'order_id': order.id, 'parts': parts})
        print(data)
        return render(request, 'orders.html', {'user': request.user, 'orders': reversed(data)})
    return redirect('/')
        
def order_info(request, order_id):
    order = Order.objects.get(pk=order_id)
    parts = []
    for part in order.parts.all():
        parts.append(part)
    data = {'order_id': order_id, 'parts': parts}
    return render(request, 'order_info.html', {'user': request.user, 'order': data, 'date': order.get_date(), 'time': order.get_time()})

def shop(request):
    parts = Part.objects.all()
    return render(request, 'shop.html', {'user': request.user, 'parts': parts})

def add_part_shop(request, part_id):
    if request.user.is_authenticated:
        part = Part.objects.get(id=part_id)
        shop_cart, created = Shopping_Cart.objects.get_or_create(user=request.user)
        shop_cart.save()
        shop_cart.parts.add(part)
        shop_cart.save()
        return JsonResponse({'flag': True, 'message': 'Added to cart!'}) 
    return JsonResponse({'flag': False, 'message': 'Not logged in!'}) 

def remove_part_shop(request, part_id):
    if request.user.is_authenticated:
        shop_cart, created = Shopping_Cart.objects.get_or_create(user=request.user)
        shop_cart.parts.remove(part_id)
        return JsonResponse({'flag': True, 'message': 'Removed from cart!'}) 
    return JsonResponse({'flag': False, 'message': 'Not logged in!'}) 

def cart(request):
    if request.user.is_authenticated:
        cart, created = Shopping_Cart.objects.get_or_create(user=request.user)
        parts = []
        for part in cart.parts.all():
            parts.append(part)
        if len(parts) > 0:
            return render(request, 'shop_cart.html', {'user': request.user, 'parts': parts})
        return redirect('/shop/')
    return redirect('/')

def checkout(request):
    if request.user.is_authenticated:
        cart = Shopping_Cart.objects.get(user=request.user)
        parts = []
        for part in cart.parts.all():
            parts.append(part)
        if len(parts) > 0:
            order = Order()
            order.user = request.user
            order.save()
            for i in parts:
                if i is not None:
                    order.parts.add(i)
            order.save()
            build = Cart.objects.get(user=request.user)
            if build is not None:
                build.delete()
            cart.delete()
            return redirect('/orders/'+str(order.id)+'/')
    return redirect('/shop/')