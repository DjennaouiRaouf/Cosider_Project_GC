# Generated by Django 4.2.10 on 2024-02-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_gc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unite',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.CharField(db_column='code_unite', max_length=500, primary_key=True, serialize=False, verbose_name='Code Unité')),
                ('libelle', models.CharField(max_length=500, verbose_name='Libelle')),
                ('date_ouverture', models.DateField(verbose_name="Date d'ouverture")),
                ('date_cloture', models.DateField(null=True, verbose_name='Date de cloture')),
            ],
        ),
    ]
