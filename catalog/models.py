from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

def cover_upload_path(instance, filename):
    return f"covers/{filename}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    language = models.CharField(max_length=50, blank=True, null=True)
    cover_image = models.ImageField(upload_to=cover_upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

    def clean(self):
        
        if self.published_date > date.today():
            from django.core.exceptions import ValidationError
            raise ValidationError("Published date cannot be in the future.")
