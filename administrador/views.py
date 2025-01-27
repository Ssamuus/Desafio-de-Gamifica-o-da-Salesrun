from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Desafios, Convite

def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get("login")
        senha = request.POST.get("senha")

        user = authenticate(request, login=login_input, password=senha)
        if user:
            login(request, user)
            if user.tipo_usuario == "administrador":
                return redirect("homeadmin")
            elif user.tipo_usuario == "corretor":
                return redirect("desafios_corretor")
        else:
            return render(request, "administrador/login.html", {"erro": "Credenciais inválidas!"})

    return render(request, "administrador/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home_adm_view(request):
    if request.user.tipo_usuario != "administrador":
        return redirect("login")
    return render(request, "administrador/home_admin.html")

@login_required
def desafios_corretor_view(request):
    if request.user.tipo_usuario != "corretor":
        return redirect("login")
    
    desafios = Desafios.objects.filter(corretores=request.user)
    if request.method == "POST":
        desafio_id = request.POST.get("desafio_id")
        desafio = Desafios.objects.get(id=desafio_id)
        desafio.corretores.remove(request.user)
        return redirect("desafios_corretor") 
    
    return render(request, "administrador/desafios_corretor.html", {"desafios": desafios})

@login_required
def cadastro_view(request):

    if request.method == "POST":
        tipo_usuario = request.POST.get("tipo_usuario")
        nome = request.POST.get("nome")
        login = request.POST.get("login")
        senha = request.POST.get("senha")
        cpf = request.POST.get("cpf", None).replace('.', '').replace('-', '')   

        if Usuario.objects.filter(login=login).exists():
            return render(request, "administrador/cadastro.html", {"erro": "Login já está em uso!"})

        if tipo_usuario == "administrador":
            Usuario.objects.create_user(nome=nome, login=login, senha=senha, tipo_usuario="administrador")
        elif tipo_usuario == "corretor":

            if Usuario.objects.filter(cpf=cpf).exists():
                return render(request, "administrador/cadastro.html", {"erro": "CPF já está em uso!"})
            if not cpf:
                return render(request, "administrador/cadastro.html", {"erro": "CPF em branco!"})
            if len(cpf) != 11:
                return render(request, "administrador/cadastro.html", {"erro": "O CPF deve conter exatamente 11 dígitos!"})
            Usuario.objects.create_user(nome=nome, login=login, senha=senha, cpf=cpf, tipo_usuario="corretor")

        return redirect("lista_usuarios")

    return render(request, "administrador/cadastro.html")


@login_required
def lista_desafios_view(request):
    if request.user.tipo_usuario != "administrador":
        return redirect("login")  

    desafios = Desafios.objects.prefetch_related("corretores").all()
    return render(request, "administrador/desafios.html", {"desafios": desafios})

def lista_usuarios_view(request):
    if request.user.tipo_usuario != "administrador":
        return redirect("login")

    usuarios = Usuario.objects.all()
    return render(request, "administrador/usuarios.html", {"usuarios": usuarios})


@login_required
def cadastro_desafio_view(request):
    if request.user.tipo_usuario != "administrador":
        return redirect("login") 

    if request.method == "POST":
        nome = request.POST.get("nome")
        imagem = request.FILES.get("imagem")
        descricao = request.POST.get("descricao")
        regras = request.POST.get("regras")
        corretores_cpfs = request.POST.getlist("corretores") 
        desafio = Desafios.objects.create(
            nome=nome,
            imagem=imagem,
            descricao=descricao,
            regras=regras,
        )

        if corretores_cpfs:
            corretores = Usuario.objects.filter(cpf__in=corretores_cpfs, tipo_usuario="corretor")
            for corretor in corretores:
                Convite.objects.create(desafio=desafio, corretor=corretor)

        desafio.save()
        return redirect("lista_desafios")

    corretores = Usuario.objects.filter(tipo_usuario="corretor")
    return render(request, "administrador/cadastro_desafio.html", {"corretores": corretores})



@login_required
def apagar_desafio_view(request, desafio_id):
    if request.user.tipo_usuario != "administrador":
        return redirect("login")

    desafio = get_object_or_404(Desafios, id=desafio_id)
    desafio.delete()
    return redirect("lista_desafios")

@login_required
def apagar_usuario_view(request, usuario_id):
    if request.user.tipo_usuario != "administrador":
        return redirect("login") 
    usuario = get_object_or_404(Usuario, id=usuario_id)
    excluir_usuario_logado = usuario == request.user

    usuario.delete()
    if excluir_usuario_logado:
        logout(request) 
        return redirect("login")

    return redirect("lista_usuarios")



@login_required
def editar_desafio_view(request, desafio_id):
    if request.user.tipo_usuario != "administrador":
        return redirect("login") 

    desafio = get_object_or_404(Desafios, id=desafio_id)

    if request.method == "POST":
        desafio.nome = request.POST.get("nome", desafio.nome)
        desafio.descricao = request.POST.get("descricao", desafio.descricao)
        desafio.regras = request.POST.get("regras", desafio.regras)
        if request.FILES.get("imagem"):
            desafio.imagem = request.FILES.get("imagem")
        corretores_ids = request.POST.getlist("corretores")
        if corretores_ids:
            corretores = Usuario.objects.filter(id__in=corretores_ids, tipo_usuario="corretor")
            for corretor in corretores:
                Convite.objects.create(desafio=desafio, corretor=corretor)

        desafio.save()
        return redirect("lista_desafios")

    corretores = Usuario.objects.filter(tipo_usuario="corretor")
    return render(request, "administrador/editar_desafio.html", {"desafio": desafio, "corretores": corretores})


@login_required
def editar_usuario_view(request, usuario_id):
    if request.user.tipo_usuario != "administrador":
        return redirect("login") 

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        login = request.POST.get("login", usuario.login)
        nome = request.POST.get("nome", usuario.nome)
        tipo_usuario = request.POST.get("tipo_usuario", usuario.tipo_usuario)
        senha = request.POST.get("senha", None)
        cpf_novo = request.POST.get("cpf", "").replace('.', '').replace('-', '') if tipo_usuario == "corretor" else None

        if Usuario.objects.filter(login=login).exclude(id=usuario.id).exists():
            return render(
                request,
                "administrador/editar_usuario.html",
                {"usuario": usuario, "erro": "Login já está em uso!"}
            )

        if tipo_usuario == "corretor":
            if not cpf_novo:
                return render(
                    request,
                    "administrador/editar_usuario.html",
                    {"usuario": usuario, "erro": "CPF é obrigatório para corretores!"}
                )
            if len(cpf_novo) != 11 or not cpf_novo.isdigit():
                return render(
                    request,
                    "administrador/editar_usuario.html",
                    {"usuario": usuario, "erro": "O CPF deve conter exatamente 11 dígitos numéricos!"}
                )
            if Usuario.objects.filter(cpf=cpf_novo).exclude(id=usuario.id).exists():
                return render(
                    request,
                    "administrador/editar_usuario.html",
                    {"usuario": usuario, "erro": "CPF já está em uso!"}
                )

            if usuario.cpf != cpf_novo:
                usuario.desafios.clear() 
        else:
            cpf_novo = None
            usuario.desafios.clear()

        usuario.nome = nome
        usuario.login = login
        usuario.tipo_usuario = tipo_usuario
        usuario.cpf = cpf_novo

        if senha: 
            usuario.set_password(senha) 

        usuario.save()  

      
        if usuario == request.user and tipo_usuario == "corretor":
            logout(request)
            return redirect("login")

        return redirect("lista_usuarios")

    return render(request, "administrador/editar_usuario.html", {"usuario": usuario})



@login_required
def convite_corretor_view(request):
    if request.user.tipo_usuario != "corretor":
        return redirect("login")

    convites = Convite.objects.filter(corretor=request.user, aceito=False, recusado=False)

    if request.method == "POST":
        convite_id = request.POST.get("convite_id")
        resposta = request.POST.get("resposta") 

        try:
            convite = Convite.objects.get(id=convite_id, corretor=request.user)

            if resposta == "aceitar":
                convite.aceito = True
                desafio = convite.desafio
                desafio.corretores.add(request.user)
            elif resposta == "recusar":
                convite.recusado = True

            convite.save()
        except Convite.DoesNotExist:
            pass

        return redirect("convites_corretor")

    return render(request, "administrador/convites.html", {"convites": convites})
