# Generated by Django 5.1.2 on 2025-02-28 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('big_transport_app', '0004_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photos', models.ImageField(blank=True, null=True, upload_to='annonces/')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='big_transport_app.categories')),
            ],
        ),
    ]
