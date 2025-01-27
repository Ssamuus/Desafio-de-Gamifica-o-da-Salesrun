# Generated by Django 5.1.5 on 2025-01-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0004_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo_usuario',
            field=models.CharField(choices=[('administrador', 'Administrador'), ('corretor', 'Corretor')], max_length=20, verbose_name='Tipo de Usuário'),
        ),
    ]
