# Generated by Django 2.2 on 2019-06-21 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancamentos', '0009_auto_20190621_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='ultima_atualizacao',
            field=models.DateTimeField(),
        ),
    ]
