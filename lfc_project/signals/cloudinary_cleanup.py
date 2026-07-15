from django.db.models.signals import pre_save, post_delete

from lfc_project.utils.cloudinary_utils import delete_cloudinary_file


_registered_models = set()


def register_cloudinary_cleanup(model, image_fields):
    """
    Register automatic Cloudinary cleanup for the given model.

    Args:
        model: Django model class.
        image_fields: A string or list of ImageField/FileField names.
    """

    if model in _registered_models:
        return

    _registered_models.add(model)

    if isinstance(image_fields, str):
        image_fields = [image_fields]

    def pre_save_handler(sender, instance, **kwargs):
        if not instance.pk:
            return

        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        for field_name in image_fields:
            old_file = getattr(old_instance, field_name, None)
            new_file = getattr(instance, field_name, None)

            if old_file and old_file != new_file:
                delete_cloudinary_file(old_file)

    def post_delete_handler(sender, instance, **kwargs):
        for field_name in image_fields:
            file_field = getattr(instance, field_name, None)
            if file_field:
                delete_cloudinary_file(file_field)

    pre_save.connect(
        pre_save_handler,
        sender=model,
        weak=False,
        dispatch_uid=f"cloudinary_pre_save_{model._meta.label}",
    )

    post_delete.connect(
        post_delete_handler,
        sender=model,
        weak=False,
        dispatch_uid=f"cloudinary_post_delete_{model._meta.label}",
    )
