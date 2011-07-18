# -*- coding: utf-8 -*-
"""
Mexican-specific form helpers.
"""

from django.forms.fields import Select, RegexField
from django.utils.translation import ugettext_lazy as _
import re

date_re = r'\d{2}((01|03|05|07|08|10|12)(0[1-9]|[12]\d|3[01])|02(0[1-9]|[12]\d)|(04|06|09|11)(0[1-9]|[12]\d|30))'

class MXStateSelect(Select):
    """
    A Select widget that uses a list of Mexican states as its choices.
    """
    def __init__(self, attrs=None):
        from mx_states import STATE_CHOICES
        super(MXStateSelect, self).__init__(attrs, choices=STATE_CHOICES)

class MXZipCodeField(RegexField):
    """
    A field that accepts a `classic` MX Zip Code.
    
    More info about this:
        http://en.wikipedia.org/wiki/List_of_postal_codes_in_Mexico
    """
    default_error_messages = {
        'invalid': _('Enter a valid zip code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        regex = r'^(0[1-9]|[1][0-6]|[2-9]\d)(\d{3})$'
        super(MXZipCodeField, self).__init__(regex, *args, **kwargs)

class MXRFCField(RegexField):
    """
    A field that validates a `Registro Federal de Contribuyentes` string for
    either `Persona física` or `Persona moral`.
    
    More info about this:
        http://es.wikipedia.org/wiki/Registro_Federal_de_Contribuyentes_(M%C3%A9xico)
    """
    default_error_messages = {
        'invalid': _('Enter a valid RFC.'),
    }

    def __init__(self, *args, **kwargs):
        rfc_re = re.compile(ur'^[A-Z&Ññ]{3,4}%s[A-Z0-9]{3}$' % date_re, re.IGNORECASE)
        super(MXRFCField, self).__init__(rfc_re, *args, **kwargs)

    def clean(self, value):
        value = super(MXRFCField, self).clean(value)
        value = value.upper()
        return value

class MXCURPField(RegexField):
    """
    A field that validates a `Clave Única de Registro de Población`.
    
    More info about this:
        http://www.condusef.gob.mx/index.php/clave-unica-de-registro-de-poblacion-curp
    """
    default_error_messages = {
        'invalid': _('Enter a valid CURP.'),
    }

    def __init__(self, *args, **kwargs):
        states_re = r'(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)'
        consonants_re = r'[B-DF-HJ-NP-TV-Z]'
        curp_re = ur'^[A-Z]{4}%s[HM]%s%s{3}\d{2}$' % (date_re, states_re, consonants_re)
        curp_re = re.compile(curp_re, re.IGNORECASE)
        super(MXCURPField, self).__init__(curp_re, *args, **kwargs)

    def clean(self, value):
        value = super(MXCURPField, self).clean(value)
        value = value.upper()
        return value
