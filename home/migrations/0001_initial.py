# Generated by Django 5.1.4 on 2024-12-23 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('population', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Население')),
                ('area', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Площадь')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('image_small', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение, миниатюра')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.country')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('-population',),
            },
        ),
    ]