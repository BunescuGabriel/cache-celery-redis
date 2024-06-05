from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .documents import TelefonDocument
from .models import Telefon, CartItem, Payment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from elasticsearch_dsl.query import MultiMatch, Wildcard


@cache_page(60*5, cache='default')
def telefon(request):
    telefons = Telefon.objects.all()
    template = loader.get_template('home.html')
    context = {
        'telefons': telefons,
    }
    return HttpResponse(template.render(context, request))


def about(request):
    return render(request, 'about.html')


def search(request):
    q = request.GET.get("q")
    context = {}
    if q:
        s = TelefonDocument.search().query(
            MultiMatch(query=q, fields=['model', 'producator', 'procesor', 'descriere'], fuzziness='AUTO')
            |
            Wildcard(model=q.lower() + '*')
            |
            Wildcard(producator=q.lower() + '*')
            |
            Wildcard(procesor=q.lower() + '*')
            |
            Wildcard(descriere=q.lower() + '*')
        )
        context["telefons"] = s.to_queryset()
    else:
        context["telefons"] = Telefon.objects.all()
    return render(request, 'home.html', context)






def cos(request):
    user_id = request.user.id
    cache_key = f'cart_items_{user_id}'
    cart_items = cache.get(cache_key)
    
    if cart_items is None:
        cart_items = list(CartItem.objects.filter(user=request.user))
        cache.set(cache_key, cart_items, 900)  # 900 seconds
    
    return render(request, 'cos.html', {'cart_items': cart_items})


def add_to_cart(request, phone_id):
    telefon = get_object_or_404(Telefon, id=phone_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, telefon=telefon)

    if not created:
        cart_item.save()
        
    user_id = request.user.id
    cache_key = f'cart_items_{user_id}'
    
    # Invalidează cache-ul pentru utilizatorul respectiv
    cache.delete(cache_key)
    
    return JsonResponse({'status': 'success'})

def remove_to_cart(request, phone_id):
    telefon = get_object_or_404(Telefon, id=phone_id)
    
    cart_item = CartItem.objects.filter(user=request.user, telefon=telefon).first()
    
    if cart_item:
        cart_item.delete()
        
        # Invalidează cache-ul pentru utilizatorul respectiv
        user_id = request.user.id
        cache_key = f'cart_items_{user_id}'
        cache.delete(cache_key)
        
        return HttpResponse(status=200) 
    else:
        return JsonResponse({'error': 'Elementul nu a fost găsit în coș.'}, status=404)
    


@login_required
@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_items = data.get('selected_items', [])

        if not selected_items:
            return JsonResponse({'error': 'Nu s-au selectat produse pentru plată.'}, status=400)

        total_price = sum(float(item['totalPrice']) for item in selected_items)
        item_ids = [item['itemId'] for item in selected_items]  # Colectăm item.id-urile

        cart_items = CartItem.objects.filter(id__in=item_ids)

        if cart_items.exists():
            payment = Payment.objects.create(user=request.user, total_price=total_price)
            payment.cart.set(cart_items)  # Adăugăm item.id-urile în câmpul ManyToMany
            cart_items.delete()
            
            user_id = request.user.id
            cache_key = f'cart_items_{user_id}'
            cache.delete(cache_key)
        

            return JsonResponse({'success': 'Plata a fost efectuată cu succes!'})
        
        return JsonResponse({'error': 'Produsele selectate nu există în coș.'}, status=400)

    return JsonResponse({'error': 'Metoda de request trebuie să fie POST.'}, status=405)


def success(request):
    return render(request, 'success.html')
    