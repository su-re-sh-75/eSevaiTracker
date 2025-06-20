# Generated by Django 5.2.3 on 2025-06-15 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_num', models.CharField(max_length=15, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Docs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhaar_num', models.CharField(blank=True, max_length=20, null=True)),
                ('pan_num', models.CharField(blank=True, max_length=20, null=True)),
                ('voter_id', models.CharField(blank=True, max_length=20, null=True)),
                ('aadhaar_file', models.FileField(blank=True, null=True, upload_to='docs/aadhaar/')),
                ('pan_file', models.FileField(blank=True, null=True, upload_to='docs/pan/')),
                ('voterid_file', models.FileField(blank=True, null=True, upload_to='docs/voterid/')),
                ('driving_license_file', models.FileField(blank=True, null=True, upload_to='docs/driving_license/')),
                ('ration_card_file', models.FileField(blank=True, null=True, upload_to='docs/ration_card/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
