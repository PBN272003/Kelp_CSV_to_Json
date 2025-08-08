from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.JSONField(null=True, blank=True)
    additional_info = models.JSONField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.name} - {self.age}"
    
class UserReportData(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_users = models.IntegerField(default=0)
    under_20 = models.FloatField(default=0.0)
    between_20_40 = models.FloatField(default=0.0)
    between_40_60 = models.FloatField(default=0.0)
    over_60 = models.FloatField(default=0.0)

    def __str__(self):
        return f"Report at {self.uploaded_at}"
    
    