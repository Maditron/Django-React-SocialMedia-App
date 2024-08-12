from django.db import models
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404



class AbstractManager(models.Manager):

    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ValueError, TypeError, ObjectDoesNotExist):
            return Http404
    


class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, editable=False, unique=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager

    class Meta:
        abstract = True 