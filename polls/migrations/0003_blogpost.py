# Generated by Django 3.0.8 on 2020-08-05 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200804_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('pub_time', models.DateTimeField()),
                ('b_userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Users')),
            ],
            options={
                'verbose_name': '标题',
                'verbose_name_plural': '标题',
                'ordering': ['-pub_time'],
            },
        ),
    ]
