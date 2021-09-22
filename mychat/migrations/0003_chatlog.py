# Generated by Django 3.2 on 2021-07-17 00:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mychat', '0002_chatroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='メッセージ')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mychat.user')),
            ],
        ),
    ]