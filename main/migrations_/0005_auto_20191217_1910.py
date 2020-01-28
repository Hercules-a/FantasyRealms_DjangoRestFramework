# Generated by Django 3.0 on 2019-12-17 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_extenduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='extend_user', to=settings.AUTH_USER_MODEL),
        ),
    ]