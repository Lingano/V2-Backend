from django.db import models

# Create your models here.


# Add an example model of a simple company with a name, description, country of origin and a economic sector.
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    country_of_origin = models.CharField(max_length=100)
    economic_sector = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]
