# Generated by Django 5.1.5 on 2025-01-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Corretor', 'Corretor')], max_length=20, verbose_name='Tipo de Usuário'),
        ),
    ]
