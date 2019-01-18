# Generated by Django 2.1.4 on 2019-01-15 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactorBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('class_name', models.CharField(choices=[('AbuFactorBuyBreak', '海龟买'), ('AbuDoubleMaBuy', '双均线买')], editable=False, max_length=32, verbose_name='策略')),
            ],
            options={
                'verbose_name': '买策略',
                'verbose_name_plural': '买策略',
            },
        ),
        migrations.CreateModel(
            name='FactorSell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('class_name', models.CharField(choices=[('AbuFactorSellBreak', '海龟卖'), ('AbuDoubleMaSell', '双均线卖')], editable=False, max_length=32, verbose_name='策略')),
            ],
            options={
                'verbose_name': '卖策略',
                'verbose_name_plural': '卖策略',
            },
        ),
        migrations.CreateModel(
            name='RunLoopGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('description', models.TextField(verbose_name='说明')),
                ('status', models.CharField(blank=True, default='新建', max_length=64, verbose_name='状态')),
                ('read_cash', models.IntegerField(verbose_name='初始化资金')),
            ],
            options={
                'verbose_name': '回测',
                'verbose_name_plural': '回测',
            },
        ),
        migrations.CreateModel(
            name='FactorBuyBreakXd',
            fields=[
                ('factorbuy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='runloop.FactorBuy')),
                ('xd', models.CharField(max_length=64, verbose_name='周期')),
            ],
            options={
                'verbose_name': '海龟买入',
                'verbose_name_plural': '海龟买入',
            },
            bases=('runloop.factorbuy',),
        ),
        migrations.CreateModel(
            name='FactorSellBreakXd',
            fields=[
                ('factorsell_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='runloop.FactorSell')),
                ('xd', models.CharField(max_length=64, verbose_name='周期')),
            ],
            options={
                'verbose_name': '海龟卖出',
                'verbose_name_plural': '海龟卖出',
            },
            bases=('runloop.factorsell',),
        ),
        migrations.AddField(
            model_name='runloopgroup',
            name='factor_buys',
            field=models.ManyToManyField(related_name='factor_buy_groups', to='runloop.FactorBuy', verbose_name='买策略组合'),
        ),
        migrations.AddField(
            model_name='runloopgroup',
            name='factor_sells',
            field=models.ManyToManyField(related_name='factor_sell_groups', to='runloop.FactorSell', verbose_name='卖策略组合'),
        ),
        migrations.AddField(
            model_name='runloopgroup',
            name='stocks',
            field=models.ManyToManyField(related_name='stock_groups', to='base.Stock', verbose_name='股票组合'),
        ),
    ]
