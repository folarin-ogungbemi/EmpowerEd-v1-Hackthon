# Generated by Django 4.1.1 on 2023-02-18 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_resource_about_resource_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='userpic',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.parent'),
        ),
        migrations.AlterField(
            model_name='student',
            name='userpic',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]