# Generated by Django 3.0 on 2020-01-08 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0002_auto_20160226_1747'),
        ('main', '0010_game_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='authtoken.Token'),
        ),
    ]