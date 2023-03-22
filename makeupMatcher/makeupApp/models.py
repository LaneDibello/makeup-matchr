from django.db import models

# auto generated products 
class Product(models.Model):
    name = models.CharField(max_length=128)
    vendor = models.CharField(max_length=128)
    red = models.SmallIntegerField()
    green = models.SmallIntegerField()
    blue = models.SmallIntegerField()
    url = models.CharField(max_length=2048)
    brand = models.CharField(max_length=256, blank=True, null=True)
    colorcode = models.CharField(max_length=128, blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'products'

# Create your models here.
class imgModel(models.Model):
	title = models.CharField(max_length = 200)
	img = models.ImageField(null=True, blank = True, upload_to = "images/")

	def __str__(self):
		return self.title
