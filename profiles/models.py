from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from google_calendar import main as gcal

# ACCOUNTS BLOCK


class Profile(models.Model):
    """Профиль пользователя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, created, instance, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    first_name = models.CharField('first_name', max_length=40, blank=True,
                                  help_text='Account first name')
    middle_name = models.CharField('middle_name', max_length=40, blank=True,
                                   help_text='Account middle name')
    last_name = models.CharField('middle_name', max_length=40, blank=True,
                                 help_text='Account last name')
    is_verified = models.BooleanField('is_verified', default=False,
                                      help_text='Indicates account has been verified for identity')
    is_admin = models.BooleanField('is_admin', default=False,
                                   help_text='Indicates account has been admin for identity')

    # def __str__(self):
    #     return self.user.username + '  –  ' + self.kind


class Student(models.Model):
    """Профиль студента."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Teacher(models.Model):
    """Профиль учителя."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Client(models.Model):
    """Профиль клиента."""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


# OBJECTS BLOCK


class Group(models.Model):
    """Группа."""
    name = models.CharField('name', max_length=150, help_text='Group name', unique=True)
    is_primary = models.BooleanField('is_primary', default=False,
                                     help_text='Indicates is the group primary')

    def __str__(self):
        return 'Group: ' + self.name + '; verified: ' + str(self.is_primary)


class Lesson(models.Model):
    """Занятие."""
    name = models.CharField('lesson_name', max_length=150, blank=False,
                            help_text='lesson name')

    TYPE_CHOICES = (
        ('class', 'class'),
        ('lecture', 'lecture')
    )
    type = models.CharField(choices=TYPE_CHOICES, default='class', max_length=7)
    primary_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=False, related_name='primary_teacher')
    secondary_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name='secondary_teacher')

    class Meta:
        unique_together = (('name', 'type', 'primary_teacher'),)

    def __str__(self):
        return self.name + ' - ' + self.type


class University(models.Model):
    """Университет."""
    name = models.CharField('university name', max_length=150, blank=False, unique=True,
                            help_text='university name')

    english_name = models.CharField('university english name', max_length=150, blank=False, unique=True,
                                    help_text='university english name')  # нужно, потом придумаю зачем

    description = models.CharField('university description', max_length=5000, blank=True,
                                   help_text='university description')

    def __str__(self):
        return self.name


@receiver(pre_save, sender=University)
def create_google_calendar(sender, instance, **kwargs):
    gcal.create_calendar(instance.name)


class Building(models.Model):
    """Строение."""
    name = models.CharField('building name', max_length=150, blank=False, unique=True, help_text='building name')

    address = models.CharField('building address', max_length=5000, blank=True, help_text='building address')

    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Auditory(models.Model):
    """Аудитория."""
    name = models.CharField('auditory name', max_length=50, blank=False, unique=True, help_text='auditory name')

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# OBJECTS TRASH BLOCK


class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("group", "student"),)

    def __str__(self):
        return 'Group: ' + self.group.name + '; Login: ' + self.student.profile.user.username
