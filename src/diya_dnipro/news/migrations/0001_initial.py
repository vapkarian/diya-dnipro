# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 20:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Назва')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата розміщення')),
                ('is_top', models.BooleanField(default=False, verbose_name='Додати до топу?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показувати?')),
            ],
            options={
                'verbose_name': 'запис новини',
                'verbose_name_plural': 'Новини',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Назва')),
                ('url', models.CharField(max_length=128, verbose_name='Посилання')),
                ('priority_order', models.PositiveSmallIntegerField(unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Показувати?')),
            ],
            options={
                'verbose_name': 'запис категорії',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='Нотатки')),
                ('file', models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='Зображення')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Category', verbose_name='Категорія'),
        ),
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(help_text='Якщо не обрано, за замовчуванням використовується <a href="/static/news/img/default-preview.png" target="_blank">стандартне зображення</a>.', related_name='articles', to='news.Image', verbose_name='Додаткові зображення до статті'),
        ),
        migrations.AddField(
            model_name='article',
            name='main_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_articles', to='news.Image', verbose_name='Основне зображення до статті'),
        ),
        migrations.AddField(
            model_name='article',
            name='top_image',
            field=models.ForeignKey(help_text='Оптимальний розмір - 727 x 378.', on_delete=django.db.models.deletion.CASCADE, related_name='top_articles', to='news.Image', verbose_name='Зображення для ТОПу'),
        ),
    ]