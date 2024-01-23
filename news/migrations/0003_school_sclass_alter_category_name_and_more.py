# Generated by Django 4.2.7 on 2024-01-20 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_category_name_en_category_name_ru_post_title_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('address', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.school')),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='category name', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(help_text='category name', max_length=64, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(help_text='category name', max_length=64, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('sclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.sclass')),
            ],
        ),
    ]