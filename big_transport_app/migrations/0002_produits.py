# Generated by Django 5.1.2 on 2024-11-22 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big_transport_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='produits/')),
            ],
        ),
    ]
