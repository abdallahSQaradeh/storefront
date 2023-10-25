from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
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
    