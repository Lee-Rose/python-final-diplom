# Generated by Django 4.1.3 on 2022-12-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_parameter_productinfo_productparameter_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='parameter',
            options={'verbose_name': 'Name parameter', 'verbose_name_plural': 'Names parameters'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-name',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productinfo',
            options={'verbose_name': 'Product Information', 'verbose_name_plural': 'Products information'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': 'Shop', 'verbose_name_plural': 'Shops'},
        ),
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('not_delivered', 'Not delivered'), ('delivered', 'Delivered')], default='not_delivered', max_length=50),
        ),
    ]
