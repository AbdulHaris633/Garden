# Generated by Django 5.1.3 on 2024-12-09 20:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('url', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('description', models.TextField(max_length=100, null=True)),
            ],
        ),
    ]
