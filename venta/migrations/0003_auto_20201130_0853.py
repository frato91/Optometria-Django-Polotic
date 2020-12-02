# Generated by Django 3.1.3 on 2020-11-30 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='productos',
        ),
        migrations.AddField(
            model_name='pedido',
            name='pago',
            field=models.CharField(choices=[('tc', 'Tarjeta de credito'), ('bv', 'Billetera virtual'), ('ef', 'Efectivo'), ('de', 'Debito')], default='ef', max_length=20),
        ),
        migrations.AlterField(
            model_name='productos',
            name='precio',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='PedidoProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.productos')),
            ],
        ),
    ]