# Generated by Django 5.1 on 2024-10-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bank', '0003_submitedanswer_mark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitedanswer',
            name='submited_text',
        ),
        migrations.AlterField(
            model_name='submitedanswer',
            name='submited_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
