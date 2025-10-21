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
def auto_delete_skema_on_delete(sender, instance, **kwargs):
    if instance.file_skema and os.path.isfile(instance.file_skema.path):
        os.remove(instance.file_skema.path)

    if instance.preview_skema and os.path.isfile(instance.preview_skema.path):
        os.remove(instance.preview_skema.path)


@receiver(pre_save, sender=SkemaModel)
def auto_delete_skema_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = SkemaModel.objects.get(pk=instance.pk)
    except SkemaModel.DoesNotExist:
        return False

    new_file = instance.file_skema
    if old_file.file_skema and old_file.file_skema != new_file:
        if os.path.isfile(old_file.file_skema.path):
            os.remove(old_file.file_skema.path)

    # if instance.file_skema and (
    #     not old_file or old_file.file_skema != instance.file_skema
    # ):
    #     if (
    #         old_file
    #         and old_file.file_skema
    #         and os.path.isfile(old_file.preview_skema.path)
    #     ):
    #         os.remove(old_file.preview_skema.path)
