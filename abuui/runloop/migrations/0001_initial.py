# Generated by Django 2.1.4 on 2019-01-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FactorBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='策略名称')),
            ],
            options={
                'verbose_name': '买策略',
                'verbose_name_plural': '买策略',
            },
        ),
        migrations.CreateModel(
            name='RunLoopGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=64)),
                ('description', models.TextField()),
                ('factor_buys', models.ManyToManyField(blank=True, related_name='factor_buy_groups', to='runloop.FactorBuy', verbose_name='FactorBuys')),
            ],
            options={
                'verbose_name': 'RunLoopGroup',
                'verbose_name_plural': 'RunLoopGroup',
            },
        ),
    ]
