from django.shortcuts import redirect, render
from .models import Laptop, Contact
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Contact  
from .tasks import send_spam_email 

def laptop(request):
    laptops = Laptop.objects.all()
    template_name = loader.get_template('laptop.html')
    context = {
        'laptops': laptops,
    }
    return HttpResponse(template_name.render(context,request))


@csrf_exempt
def send_spam(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if name and email:
            contact = Contact.objects.create(name=name, email=email)
            send_spam_email.delay(contact.email)

            return redirect('/') 
        else:
            return HttpResponse("Invalid data", status=400)

    return render(request, 'contact_form.html', status=200)
