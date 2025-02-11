# Generated by Django 5.1.5 on 2025-01-26 17:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('login', models.CharField(max_length=20, unique=True, verbose_name='Login')),
                ('senha', models.CharField(max_length=128, verbose_name='Senha')),
                ('tipo_usuario', models.CharField(choices=[('administrador', 'Administrador'), ('corretor', 'Corretor')], max_length=20, verbose_name='Tipo de Usuário')),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='O CPF deve conter exatamente 11 dígitos numéricos.', regex='^\\d{11}$')], verbose_name='CPF')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='É funcionário?')),
                ('groups', models.ManyToManyField(blank=True, related_name='usuario_groups', to='auth.group', verbose_name='Groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='usuario_permissions', to='auth.permission', verbose_name='User Permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Desafios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome')),
                ('imagem', models.ImageField(upload_to='desafios/', verbose_name='Imagem')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('regras', models.TextField(verbose_name='Regras')),
                ('corretores', models.ManyToManyField(limit_choices_to={'tipo_usuario': 'corretor'}, related_name='desafios', to='administrador.usuario', verbose_name='Corretores')),
            ],
        ),
    ]
