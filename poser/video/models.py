from django.db import models

# Create your models here.
from django.db import models

class Session(models.Model):
    session_id = models.CharField(max_length=256)
    sesh_date = models.DateTimeField('Session Date',auto_now_add=True)
    score = models.FloatField(default=0.0)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.session_id
