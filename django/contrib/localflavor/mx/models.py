from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import CharField
from django.contrib.localflavor.mx.mx_states import STATE_CHOICES

class MXStateField(CharField):

    description = _("Mexico state (three uppercase letters)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = STATE_CHOICES
        kwargs['max_length'] = 3
        super(MXStateField, self).__init__(*args, **kwargs)

class MXZipCodeField(CharField):

    description = _("Mexico zip code")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super(MXZipCodeField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        from django.contrib.localflavor.mx.forms import MXZipCodeField as Field
        defaults = {'form_class': Field}
        defaults.update(kwargs)
        return super(MXZipCodeField, self).formfield(**defaults)

class MXRFCField(CharField):

    description = _("Mexican RFC")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(MXRFCField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        from django.contrib.localflavor.mx.forms import MXRFCField as Field
        defaults = {'form_class': Field}
        defaults.update(kwargs)
        return super(MXRFCField, self).formfield(**defaults)

class MXCURPField(CharField):

    description = _("Mexican CURP")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        super(MXCURPField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        from django.contrib.localflavor.mx.forms import MXCURPField as Field
        defaults = {'form_class': Field}
        defaults.update(kwargs)
        return super(MXCURPField, self).formfield(**defaults)