# Generated by Django 3.1.7 on 2021-04-03 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringToken',
            fields=[
                ('token_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authtoken.token')),
                ('last_action', models.DateTimeField(auto_now=True)),
            ],
            bases=('authtoken.token',),
        ),
    ]
