from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import *
import os


@receiver(post_delete, sender=PetaDIModel)
def auto_delete_peta_on_delete(sender, instance, **kwargs):

    if instance.file_peta and os.path.isfile(instance.file_peta.path):
        os.remove(instance.file_peta.path)


@receiver(pre_save, sender=PetaDIModel)
def auto_delete_peta_on_change(sender, instance, **kwargs):
    """
    Hapus File lama ketiga di update
    """

    if not instance.pk:
        return False
    try:
        old_file = PetaDIModel.objects.get(pk=instance.pk).file_peta
    except PetaDIModel.DoesNotExist:
        return False

    new_file = instance.file_peta
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=SkemaModel)
def auto_delete_skema_on_delete(sender, isntance, **kwargs):
    if isinstance.file_skema and os.path.isfile(isinstance.file_skema.path):
        os.remove(isinstance.file_skema.path)


@receiver(pre_save, sender=SkemaModel)
def auto_delete_skema_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = SkemaModel.objects.get(pk=instance.ph).file_skema
    except SkemaModel.DoesNotExist:
        return False

    new_file = instance.file_skema
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
