# Generated by Django 5.1.1 on 2024-10-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='newscategory/'),
        ),
    ]
