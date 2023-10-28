from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TaggedItemMnager(models.Manager):
    def get_tags_for(self,obj_type, obj_id ):
        # this will get the content type id for the Product model from the django_contetnt_type
        content_type = ContentType.objects.get_for_model(obj_type)
        queryset = TaggedItem.objects\
            .select_related('tag')\
            .filter(content_type=content_type,
                object_id = obj_id # product id whose tags we want to query 
                ) 
        return queryset

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    objects = TaggedItemMnager()
    # What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    '''
    product = models.ForeignKey(Product), if we make this, then the Tags app
    will be dependent on the Product model, however to remove this dependency we would use 
    GenericModels, and in order to implement it we need to peace of information
    [1] the Type of an object (Product,  Video, ...)
    [2] ID of the object 
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() # if the id of an object isn't an integer this solution will not work
    content_object = GenericForeignKey() # we can read the actual object that the particular tag is applied to
    