# Generated by Django 2.2.1 on 2019-05-12 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lancamentos', '0005_remove_lancamento_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='data_inicial',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='conta',
            name='saldo_inicial',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True),
        ),
    ]
