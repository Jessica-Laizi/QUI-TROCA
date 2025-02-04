from django.shortcuts import render,redirect
from inventario.models import Inventario
from django.conf import settings
from pathlib import os



# Create your views here.

def index(request):
    return render(request, "index.html")

def listagem(request):
    listagem=Inventario.objects.all()
    return render(request,  "listagem.html", {'listagem':listagem})

def categorias(request,categoria):
    inventario=Inventario.objects.all()
    return render(request,  "categorias.html", {'inventario':inventario,'categoria':categoria})

def add(request):
    return render(request, "form.html")

def save(request):
    if request.method=="POST":
        data=request.POST 
        nomeFoto=data.get("nome").replace(" ", "")+".jpg"
        inv=Inventario(nome=data.get("nome"),validade=data.get("validade"),quantidade=data.get("quantidade"),disponivel=data.get("disponivel"),descricao=data.get("descricao"), marca=data.get("marca"), estado_de_uso=data.get("estado_de_uso"), imagem=nomeFoto)
        inv.save()
        save_img(request.FILES["imagem"], nomeFoto)
        return redirect(index)

def save_img(recebido, nome):
    with open(os.path.join(settings.BASE_DIR,"static/img/",nome),"wb+") as destination:
        for parte in recebido.chunks():
           destination.write(parte) 
           
def show(request, id):
    inv=Inventario.objects.get(pk=id)
    return render(request, "show.html", {"inv": inv})

def delete(request, id):
     inv=Inventario.objects.get(pk=id)
     inv.delete()
     return redirect(index)

def perfil(request):
    usuario = request.user
    return render(request, "perfil.html", {"usuario":usuario})
    
        
def details(request, id):
    inv=Inventario.objects.get(pk=id)
    return render(request, "detalhes.html", {"inv": inv})

def save_item(request):
    return render(request, "cadastro_itens.html")
