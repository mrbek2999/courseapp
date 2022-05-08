from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser, Student, Teacher


@receiver(post_delete, sender=Student)
def delete_user_student(sender, instance, **kwargs):
    user = CustomUser.objects.get(id=instance.user.pk)
    user.delete()


@receiver(post_save, sender=Student)
def save_user_student(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        user = CustomUser.objects.create_user(
            username=username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.password,
            is_student=True,
            is_teacher=False
        )
        user.save()
        instance.user = user
        instance.save()

    else:
        user = CustomUser.objects.get(id=instance.user.pk)
        user.username = instance.username
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.set_password(instance.password)
        user.save()


@receiver(post_delete, sender=Teacher)
def delete_user_teacher(sender, instance, **kwargs):
    user = CustomUser.objects.get(id=instance.user.pk)
    user.delete()


@receiver(post_save, sender=Teacher)
def save_user_teacher(sender, instance, created, **kwargs):
    if created:
        user = CustomUser.objects.create_user(
            username=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.password,
            is_student=False,
            is_teacher=True
        )
        instance.user = user
        instance.save()

    else:
        user = CustomUser.objects.get(id=instance.user.pk)
        user.username = instance.username
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.set_password(instance.password)
        user.save()
