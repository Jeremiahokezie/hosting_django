# Generated by Django 4.0.4 on 2022-07-18 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product', models.CharField(max_length=100)),
                ('Price', models.CharField(max_length=100)),
                ('Quantity', models.IntegerField()),
            ],
        ),
    ]