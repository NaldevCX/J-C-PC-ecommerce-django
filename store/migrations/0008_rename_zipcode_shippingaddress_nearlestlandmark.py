# Generated by Django 3.2.3 on 2021-11-04 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_orderitem_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcode',
            new_name='nearlestlandmark',
        ),
    ]
