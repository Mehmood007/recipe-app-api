import os

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Delete attachments if exists
    def delete(self, *args, **kwargs) -> None:
        attachments = self._attachments()
        for _, attachment in attachments:
            if (
                attachment
                and hasattr(attachment, 'path')
                and os.path.isfile(attachment.path)
            ):
                os.remove(attachment.path)
        super(BaseModel, self).delete(*args, **kwargs)

    # Delete old attachments
    def save(self, *args, **kwargs) -> None:
        try:
            original_obj = self.__class__.objects.get(pk=self.pk)
        except self.__class__.DoesNotExist:
            original_obj = None

        if original_obj:
            attachments = original_obj._attachments()
            for field, attachment in attachments:
                if original_obj.__getattribute__(
                    field,
                ) and original_obj.__getattribute__(
                    field,
                ) != self.__getattribute__(
                    field
                ):
                    if os.path.isfile(attachment.path):
                        os.remove(attachment.path)

        super(BaseModel, self).save(*args, **kwargs)

    def _attachments(self) -> list:
        return [
            (field.name, getattr(self, field.attname))
            for field in self._meta.fields
            if isinstance(field, models.FileField)
        ]

    class Meta:
        abstract = True
        ordering = ["-updated_at"]
