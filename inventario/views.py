from django.shortcuts import render,redirect
from inventario.models import Campus, Inventario, Solicitacao, Usuario, Categoria
from django.conf import settings
from pathlib import os
from django.contrib.auth import logout 
import numpy as np


# Create your views here.

def index(request):
    return render(request, "index.html")

def listagem(request):
    listagem=Inventario.objects.all()
    campus=Campus.objects.all()
    categorias=Categoria.objects.all()
    return render(request, "listagem.html", {'listagem':listagem, 'campus':campus, 'categorias':categorias})


def categorias(request,categoria):
    inventario=Inventario.objects.filter(disponivel='sim', categoria_id=categoria)
    categorias=Categoria.objects.all()
    return render(request,  "categorias.html", {'inventario':inventario,'categorias':categorias})

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
    inv = Usuario.objects.filter(user_id=usuario.id)
    if not inv:
        return redirect(cadastro_usuario)
    return render(request, "perfil.html", {"usuario":usuario, "inv": inv[0]})
    
        
def details(request, id):
    if request.method=="POST":
        data = request.POST
        inv=Inventario.objects.get(pk=data["item_id"])
        user=Usuario.objects.get(user_id= request.user.id)
        s= Solicitacao() 
        s.quantidade = data["quantidade"]
        s.campus_destino_id = user.campus_id
        s.campus_origem_id = inv.campus_id
        s.item_id = inv.id
        s.solicitante_id = user.user_id
        s.status_id = 1 #rever como pegar as informações do banco
        s.save()
        return redirect(pag_troca, "andamento")
    inv=Inventario.objects.get(pk=id)
    return render(request, "detalhes.html", {"inv": inv})

def atualiza_solicitacao(request, id, status):
    user=Usuario.objects.get(user_id= request.user.id)
    s= Solicitacao.objects.filter(item_id=id).exclude(status_id = 4)[0]
    s.avaliador_id = user.user_id
    s.status_id = status #rever como pegar as informações do banco
    s.save()
    
    return redirect(pag_troca, "andamento")
    

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
    if info=="campus":  # ajustar para pegar apenas os itens salvos pelo usuário
        itens =Inventario.objects.filter(campus_id = inv.campus_id) 
    elif info == "andamento":
        # itens =Inventario.objects.all()
        s =Solicitacao.objects.values_list("item_id").filter(status_id = 1, solicitante_id = usuario.id)
        itens_id = np.asarray(list(s))
        itens  =Inventario.objects.filter(pk__in = itens_id)
    elif info == "pendente":
        # itens =Inventario.objects.all()
        s =Solicitacao.objects.values_list("item_id").filter(status_id = 5, solicitante_id = usuario.id)
        itens_id = np.asarray(list(s))
        itens  =Inventario.objects.filter(pk__in = itens_id)
      
    elif info == "cancelado":
        # itens =Inventario.objects.all()
        s =Solicitacao.objects.values_list("item_id").filter(status_id = 2, solicitante_id = usuario.id)
        itens_id = np.asarray(list(s))
        itens  =Inventario.objects.filter(pk__in = itens_id)
    elif info == "salvo":
        # itens =Inventario.objects.all()
        s =Solicitacao.objects.values_list("item_id").filter(status_id = 3, solicitante_id = usuario.id)
        itens_id = np.asarray(list(s))
        itens  =Inventario.objects.filter(pk__in = itens_id)
    elif info == "concluido":
        # itens =Inventario.objects.all()
        s =Solicitacao.objects.values_list("item_id").filter(status_id = 4, solicitante_id = usuario.id)
        itens_id = np.asarray(list(s))
        itens  =Inventario.objects.filter(pk__in = itens_id)
    
    return render(request, "pag_troca.html", {"usuario":usuario, "inv": inv, "itens":itens, "info":info})
    
def logout_user (request):
    logout (request)
    return redirect(index)

def cadastro_usuario(request):
    if request.method == "POST":
        data = request.POST
        inv = Usuario()
        
        inv.matricula = data["matricula"]
        inv.ingresso = data["ingresso"]
        inv.campus_id = data["campus_id"]
        inv.status = data["status"]
        inv.user_id = request.user.id
        inv.save()
        request.user.first_name = data["nome"]
        request.user.save()
        return redirect (perfil)
    campus = Campus.objects.all()
    
    return render(request, "cadastro_usuario.html", {"campus":campus})



