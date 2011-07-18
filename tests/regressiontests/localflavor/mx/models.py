from django.db import models
from django.contrib.localflavor.mx.models import (MXStateField,
                        MXRFCField, MXCURPField, MXZipCodeField)

# When creating models you need to remember to add a app_label as
# 'localflavor', so your model can be found

class MXPersonProfile(models.Model):
    state = MXStateField()
    rfc = MXRFCField()
    curp = MXCURPField()
    zip_code = MXZipCodeField()
    class Meta:
        app_label = 'localflavor'
