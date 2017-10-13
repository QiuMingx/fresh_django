from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
	ttitle = models.CharField(max_length=20)
	isDelete = models.BooleanField(default=False)
	def __str__(self):
		return self.ttitle.encode('utf-8')
class GoodsInfo(models.Model):
	gtitle = models.CharField(max_length=20)
	gprice = models.DecimalField(max_digits=5,decimal_places=2)
	gunit = models.CharField(max_length=20,default='500g')
	ginfo = models.CharField(max_length=200)
	gpic = models.ImageField(upload_to='df_goods')
	gclick = models.IntegerField()
	gcontent = HTMLField()
	gstore = models.IntegerField()
	isDelete = models.BooleanField(default=False)
	#gtop = models.BooleanField(default=False)
	gtype = models.ForeignKey(TypeInfo)

	def __str__(self):

		return self.gtitle.encode('utf-8')
