from django.db import models

# Create your models here.
class CSVData(models.Model):
	data_name = models.CharField(max_length=300)
	data_file = models.FileField()
	data_items = models.PositiveIntegerField()
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.data_name