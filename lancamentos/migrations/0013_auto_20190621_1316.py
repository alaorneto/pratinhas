# Generated by Django 2.2 on 2019-06-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancamentos', '0012_auto_20190621_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='ultima_atualizacao',
            field=models.DateField(null=True),
        ),
    ]