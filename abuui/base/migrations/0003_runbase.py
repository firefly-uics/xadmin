# Generated by Django 2.1.4 on 2019-01-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20190120_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='RunBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('start', models.DateField(verbose_name='开始')),
                ('end', models.DateField(verbose_name='结束')),
                ('description', models.TextField(blank=True, verbose_name='说明')),
                ('status', models.CharField(blank=True, default='新建', max_length=64, verbose_name='状态')),
                ('read_cash', models.IntegerField(verbose_name='初始化资金')),
                ('stocks', models.ManyToManyField(related_name='stock_groups', to='base.Stock', verbose_name='股票组合')),
            ],
        ),
    ]
