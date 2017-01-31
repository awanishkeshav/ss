from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# Create your models here.
class TxnCategory(models.Model):
    name = models.CharField(max_length=20, blank=False, default='Food')
    mccCode = models.SmallIntegerField(default=1000)

    class Meta:
        db_table = "ss_txn_category"

class Location(models.Model):
    name =  models.CharField(max_length=100, blank=False)
    international = models.SmallIntegerField(default=1)
    class Meta:
        ordering = ('name',)
        db_table = "ss_location"