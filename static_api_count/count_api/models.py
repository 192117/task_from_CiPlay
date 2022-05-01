from django.db import models

class Event(models.Model):
    date = models.DateField()
    views = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cpc = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cpm = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('-date',) # Старые ниже (дальше)

    def save(self, *args, **kwargs):

        if self.cost and self.clicks:
            self.cpc = float(self.cost) / float(self.clicks)
        if self.cost and self.views:
            self.cpm = float(self.cost) / float(self.views) * 1000

        super().save(*args, **kwargs)