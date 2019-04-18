# Generated by Django 2.2 on 2019-04-18 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Group name', max_length=150, unique=True, verbose_name='name')),
                ('is_primary', models.BooleanField(default=False, help_text='Indicates is the group primary', verbose_name='is_primary')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, help_text='Account first name', max_length=40, verbose_name='first_name')),
                ('middle_name', models.CharField(blank=True, help_text='Account middle name', max_length=40, verbose_name='middle_name')),
                ('last_name', models.CharField(blank=True, help_text='Account last name', max_length=40, verbose_name='middle_name')),
                ('is_verified', models.BooleanField(default=False, help_text='Indicates account has been verified for identity', verbose_name='is_verified')),
                ('is_admin', models.BooleanField(default=False, help_text='Indicates account has been admin for identity', verbose_name='is_admin')),
                ('kind', models.CharField(choices=[('teacher', 'Teacher'), ('student', 'Student'), ('client', 'Client')], default='student', help_text='Indicates account type student or teacher', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('name', models.CharField(help_text='university name', max_length=150, unique=True, verbose_name='university name')),
                ('english_name', models.CharField(help_text='university english name', max_length=150, primary_key=True, serialize=False, unique=True, verbose_name='university english name')),
                ('description', models.CharField(blank=True, help_text='university description', max_length=5000, verbose_name='university description')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='profiles.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('name', models.CharField(help_text='building name', max_length=150, primary_key=True, serialize=False, unique=True, verbose_name='building name')),
                ('address', models.CharField(blank=True, help_text='building address', max_length=5000, verbose_name='building address')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.University')),
            ],
        ),
        migrations.CreateModel(
            name='Auditory',
            fields=[
                ('name', models.CharField(help_text='auditory name', max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='auditory name')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Building')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Student')),
            ],
            options={
                'unique_together': {('group', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='lesson name', max_length=150, verbose_name='lesson name')),
                ('type', models.CharField(choices=[('class', 'class'), ('lecture', 'lecture')], default='class', max_length=7)),
                ('primary_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='primary_teacher', to='profiles.Teacher')),
                ('secondary_teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_teacher', to='profiles.Teacher')),
            ],
            options={
                'unique_together': {('name', 'type', 'primary_teacher')},
            },
        ),
    ]