# Generated by Django 4.0.3 on 2022-04-10 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NFTcore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='card/img')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('help_link', models.URLField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LayerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
