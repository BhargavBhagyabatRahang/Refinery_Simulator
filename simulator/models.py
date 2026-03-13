from django.db import models

class Pipeline(models.Model):

    name=models.CharField(max_length=100)
    unit=models.CharField(max_length=100)
    initial_thickness=models.FloatField()

class SensorThickness(models.Model):

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    thickness = models.FloatField()
    anomaly_type = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

class DCSData(models.Model):
    unit = models.CharField(max_length=100)
    temperature = models.FloatField()
    pressure = models.FloatField()
    flow_rate = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class LABData(models.Model):

    unit=models.CharField(max_length=100)
    sulfur_content=models.FloatField()
    acidity=models.FloatField()
    viscosity=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)


