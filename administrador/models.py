from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, login, senha, tipo_usuario, **extra_fields):
        if not login:
            raise ValueError()
        if tipo_usuario not in ['administrador', 'corretor']:
            raise ValueError()

        extra_fields['tipo_usuario'] = tipo_usuario
        user = self.model(login=login, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, senha, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(login, senha, tipo_usuario='administrador', **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPOS_USUARIO = [
        ('administrador', 'Administrador'),
        ('corretor', 'Corretor'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome")
    login = models.CharField(max_length=20, unique=True, verbose_name="Login")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, verbose_name="Tipo de Usuário")
    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r'^\d{11}$')],
        verbose_name="CPF"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Funcionário")  
    groups = models.ManyToManyField(
        Group,
        related_name="usuario_groups",
        blank=True,
        verbose_name="Groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuario_permissions",
        blank=True,
        verbose_name="User Permissions"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['nome', 'tipo_usuario']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_usuario_display()})"


class Desafios(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    imagem = models.ImageField(upload_to='desafios/', verbose_name="Imagem")
    descricao = models.TextField(verbose_name="Descrição")
    regras = models.TextField(verbose_name="Regras")
    corretores = models.ManyToManyField(
        Usuario,
        limit_choices_to={'tipo_usuario': 'corretor'},
        related_name='desafios',
        verbose_name="Corretores",
    )

    def __str__(self):
        return self.nome


from django.db import models

class Convite(models.Model):
    desafio = models.ForeignKey(Desafios, related_name='convites', on_delete=models.CASCADE)
    corretor = models.ForeignKey(Usuario, related_name='convites', on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)
    aceito = models.BooleanField(default=False) 
    recusado = models.BooleanField(default=False) 

    def __str__(self):
        return f"Convite para {self.corretor.nome} no desafio {self.desafio.nome}"
