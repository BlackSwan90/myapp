from django.db import models
# from .utils import load_symbols
# Create your models here.


class myProduct(models.Model):

	COLOR = (
		('WHITE','white'),
		('BLUE','blue'),
		('BLACK','black'),
		('GREEN','green'),
	)

	name = models.CharField(max_length=100)
	color = models.CharField(max_length=10, choices=COLOR)
	price = models.IntegerField()

	#for viewing the table in backend mode
	def __str__(self):
		return '{} - {} - {}'.format(self.name,self.color, self.price)

class mycolors(models.Model):
	somecolor = models.CharField(max_length=100)
	class Meta:
		db_table = "mytable"

# class mysymbols_cl(models.Model):
# 	mysymbols_df = load_symbols()
# 	mysymbols_ls = mysymbols_df.to_list()
# 	aa = list(zip(mysymbols_ls,mysymbols_ls))
# 	mysymbols_doubled = tuple(aa)
# 	mysymbols_charfield = models.CharField(max_length=6, choices=mysymbols_doubled)
	