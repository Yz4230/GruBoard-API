# Generated by Django 3.0.3 on 2020-02-28 19:13

from django.db import migrations, models
import django.db.models.deletion
import openboard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.CharField(default=openboard.models.create_id, editable=False, max_length=8, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256, null=True)),
                ('admin_auth', models.CharField(default=openboard.models.create_admin_auth, editable=False, max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.CharField(default=openboard.models.create_id, editable=False, max_length=8, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='openboard.Board')),
            ],
        ),
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.CharField(default=openboard.models.create_id, editable=False, max_length=8, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256, null=True)),
                ('auth', models.CharField(default=openboard.models.create_auth, editable=False, max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openboard.Board')),
            ],
        ),
    ]
