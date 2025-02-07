from django.shortcuts import render,redirect
from inventario.models import Campus, Inventario, Usuario
from django.conf import settings
from pathlib import os



# Create your views here.

def index(request):
    return render(request, "index.html")

def listagem(request):
    listagem=Inventario.objects.all()
    campus=Campus.objects.all()
    return render(request,  "listagem.html", {'listagem':listagem, 'campus':campus})


def categorias(request,categoria):
    inventario=Inventario.objects.filter(disponivel='sim')
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
    inv = Usuario.objects.get(user_id=usuario.id)
    return render(request, "perfil.html", {"usuario":usuario, "inv": inv})
    
        
def details(request, id):
    inv=Inventario.objects.get(pk=id)
    return render(request, "detalhes.html", {"inv": inv})

def save_item(request):
    if request.method == "POST":
        data = request.POST
        inv = Inventario()
        inv.nome = data["nome"]
        inv.descricao = data["descricao"]
        inv.imagem = data["imagem"]
        inv.estado_de_uso = data["estado_de_uso"]
        inv.quantidade = data["quantidade"]
        inv.disponivel = data["disponivel"]
        inv.validade = data["validade"]
        inv.campus_id = data["campus_id"]
        inv.marca = data["marca"]
        inv.save()
    campus = Campus.objects.all()
        
    return render(request, "cadastro_itens.html",{"campus":campus})

def pag_troca(request, info):
    usuario = request.user
    inv = Usuario.objects.get(user_id=usuario.id)
    # ajustar para pegar apenas os itens salvos pelo usuário
    itens =Inventario.objects.all() 
    return render(request, "pag_troca.html", {"usuario":usuario, "inv": inv, "itens":itens, "info":info})
    

