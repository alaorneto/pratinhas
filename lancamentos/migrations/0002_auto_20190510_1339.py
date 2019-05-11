# Generated by Django 2.2 on 2019-05-10 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lancamentos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='categoria',
        ),
        migrations.AddField(
            model_name='conta',
            name='conta_categoria',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journal',
            name='conta_credito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='journal_creditos', to='lancamentos.Conta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='journal',
            name='conta_debito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='journal_debitos', to='lancamentos.Conta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lancamento',
            name='conta_credito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creditos', to='lancamentos.Conta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lancamento',
            name='conta_debito',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='debitos', to='lancamentos.Conta'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Categoria',
        ),
    ]
