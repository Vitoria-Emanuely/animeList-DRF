# Generated by Django 3.2.8 on 2021-11-03 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adiciona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Assistindo', 'Assistindo'), ('Completo', 'Completo'), ('Quero assistir', 'Quero Assistir'), ('Desisti', 'Desisti')], default='Assistindo', max_length=255)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adicoes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Adiciona',
            },
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Generos',
            },
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('epsT', models.IntegerField(verbose_name='Episodios Totais')),
                ('estudio', models.ManyToManyField(related_name='animes', to='core.Estudio')),
                ('genero', models.ManyToManyField(related_name='animes', to='core.Genero')),
            ],
        ),
        migrations.CreateModel(
            name='AdicionaAnimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eps', models.IntegerField(verbose_name='Episodios')),
                ('adicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animesAdd', to='core.adiciona')),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.anime')),
            ],
        ),
    ]
