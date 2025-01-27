# Generated by Django 5.1.5 on 2025-01-27 13:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_alter_usuario_tipo_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('aceito', models.BooleanField(default=False)),
                ('recusado', models.BooleanField(default=False)),
                ('corretor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites', to=settings.AUTH_USER_MODEL)),
                ('desafio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites', to='administrador.desafios')),
            ],
        ),
    ]
