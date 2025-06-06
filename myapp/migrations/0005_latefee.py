# Generated by Django 5.1.5 on 2025-04-27 11:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_author_bio_alter_author_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LateFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('borrowing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='late_fee', to='myapp.borrowing')),
            ],
        ),
    ]
