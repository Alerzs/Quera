# Generated by Django 5.1 on 2024-10-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Soal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('category', models.CharField(max_length=20)),
                ('level', models.CharField(choices=[('E', 'easy'), ('M', 'medium'), ('H', 'hard')], max_length=1)),
                ('soorat', models.TextField()),
                ('answer_type', models.CharField(choices=[('F', 'file'), ('C', 'code'), ('T', 'text')], default='C', max_length=1)),
                ('test_case', models.TextField(blank=True, null=True)),
                ('test_case_answer', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmitedAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submited_file', models.FileField(blank=True, null=True, upload_to='')),
                ('submited_code', models.TextField(blank=True, null=True)),
                ('submited_text', models.TextField(blank=True, null=True)),
                ('result', models.TextField(blank=True, editable=False, null=True)),
            ],
        ),
    ]
