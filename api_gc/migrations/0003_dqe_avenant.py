# Generated by Django 4.2.13 on 2024-07-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_gc', '0002_alter_dqe_qte'),
    ]

    operations = [
        migrations.AddField(
            model_name='dqe',
            name='avenant',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Avenant N°'),
        ),
    ]
