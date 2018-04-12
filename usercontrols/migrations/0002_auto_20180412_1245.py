# Generated by Django 2.0.4 on 2018-04-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercontrols', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='user',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=36, primary_key=True, serialize=False),
        ),
    ]
