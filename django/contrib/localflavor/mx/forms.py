# -*- coding: utf-8 -*-
"""
Mexican-specific form helpers.
"""

from django.forms.fields import Select, RegexField, CharField
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.mx.mx_states import STATE_CHOICES
from datetime.datetime import date
import re

DATE_RE = r'\d{2}((01|03|05|07|08|10|12)(0[1-9]|[12]\d|3[01])|02(0[1-9]|[12]\d)|(04|06|09|11)(0[1-9]|[12]\d|30))'

"""
This is the list of inconvenient words according to the `Anexo IV` of the
document described in the next link:
    www.sisi.org.mx/jspsi/documentos/2005/seguimiento/06101/0610100162005_065.doc
"""
RFC_INCONVENIENT_WORDS = [
    u'BUEI', u'BUEY', u'CACA', u'CACO', u'CAGA', u'CAGO', u'CAKA', u'CAKO', u'COGE',
    u'COJA', u'COJE', u'COJI', u'COJO', u'CULO', u'FETO', u'GUEY', u'JOTO', u'KACA',
    u'KACO', u'KAGA', u'KAGO', u'KOGE', u'KOJO', u'KAKA', u'KULO', u'MAME', u'MAMO',
    u'MEAR', u'MEAS', u'MEON', u'MION', u'MOCO', u'MULA', u'PEDA', u'PEDO', u'PENE',
    u'PUTA', u'PUTO', u'QULO', u'RATA', u'RUIN'
]

"""
This is the list of inconvenient words according to the `Anexo 2` of the
document described in the next link:
    http://portal.veracruz.gob.mx/pls/portal/url/ITEM/444112558A57C6E0E040A8C02E00695C
"""
CURP_INCONVENIENT_WORDS = [
   u'BACA', u'BAKA', u'BUEI', u'BUEY', u'CACA', u'CACO', u'CAGA', u'CAGO', u'CAKA',
   u'CAKO', u'COGE', u'COGI', u'COJA', u'COJE', u'COJI', u'COJO', u'COLA', u'CULO',
   u'FALO', u'FETO', u'GETA', u'GUEI', u'GUEY', u'JETA', u'JOTO', u'KACA', u'KACO',
   u'KAGA', u'KAGO', u'KAKA', u'KAKO', u'KOGE', u'KOGI', u'KOJA', u'KOJE', u'KOJI',
   u'KOJO', u'KOLA', u'KULO', u'LILO', u'LOCA', u'LOCO', u'LOKA', u'LOKO', u'MAME',
   u'MAMO', u'MEAR', u'MEAS', u'MEON', u'MIAR', u'MION', u'MOCO', u'MOKO', u'MULA',
   u'MULO', u'NACA', u'NACO', u'PEDA', u'PEDO', u'PENE', u'PIPI', u'PITO', u'POPO',
   u'PUTA', u'PUTO', u'QULO', u'RATA', u'ROBA', u'ROBE', u'ROBO', u'RUIN', u'SENO',
   u'TETA', u'VACA', u'VAGA', u'VAGO', u'VAKA', u'VUEI', u'VUEY', u'WUEI', u'WUEY'
]

class MXStateSelect(Select):
    """
    A Select widget that uses a list of Mexican states as its choices.
    """
    def __init__(self, attrs=None):
        super(MXStateSelect, self).__init__(attrs, choices=STATE_CHOICES)

class MXZipCodeField(RegexField):
    """
    A field that accepts a `classic` MX Zip Code.
    
    More info about this:
        http://en.wikipedia.org/wiki/List_of_postal_codes_in_Mexico
    """
    default_error_messages = {
        'invalid': _(u'Enter a valid zip code in the format XXXXX.'),
    }

    def __init__(self, *args, **kwargs):
        zip_code_re = ur'^(0[1-9]|[1][0-6]|[2-9]\d)(\d{3})$'
        super(MXZipCodeField, self).__init__(zip_code_re, *args, **kwargs)

class MXRFCField(RegexField):
    """
    A field that validates a `Registro Federal de Contribuyentes` for either
    `Persona física` or `Persona moral`.
    
    More info about this:
        http://es.wikipedia.org/wiki/Registro_Federal_de_Contribuyentes_(M%C3%A9xico)
    """
    default_error_messages = {
        'invalid': _(u'Enter a valid RFC.'),
        'inconvenient': _(u'Enter a RFC with no inconvenient business name.'),
    }
    
    def __init__(self, min_length=12, max_length=13, *args, **kwargs):
        rfc_re = re.compile(ur'^[A-Z&Ññ]{3,4}%s[A-Z0-9]{2}[0-9A]$' % DATE_RE,
                            re.IGNORECASE)
        super(MXRFCField, self).__init__(rfc_re, min_length=min_length,
                                         max_length=max_length, *args, **kwargs)

    def clean(self, value):
        value = super(MXRFCField, self).clean(value)
        value = value.upper()
        if not value[-1] == self._checksum(value[:-1]):
            raise ValidationError(self.default_error_messages['invalid'])
        if self._has_inconvenient_word(rfc):
            raise ValidationError(self.default_error_messages['inconvenient'])
        return value
    
    def _checksum(self, rfc):
        """
        More info about this procedure:
            www.sisi.org.mx/jspsi/documentos/2005/seguimiento/06101/0610100162005_065.doc
        """
        chars = u'0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ-Ñ'
        if len(rfc) is 11:
            rfc = '-' + rfc
            
        sum_ = sum(i * chars.index(c) for i, c in zip(reversed(xrange(14)), rfc))
        checksum = 11 - sum_ % 11
        
        if checksum == 10:
            return u'A'
        elif checksum == 11:
            return u'0'
        else:
            return unicode(checksum)
    
    def _has_inconvenient_word(self, rfc):
        if len(rfc) is 13:
            business_name = rfc[:4]
            return business_name in RFC_INCONVENIENT_WORDS
        return False

class MXCURPField(RegexField):
    """
    A field that validates a `Clave Única de Registro de Población`.
    
    More info about this:
        http://www.condusef.gob.mx/index.php/clave-unica-de-registro-de-poblacion-curp
    """
    default_error_messages = {
        'invalid': _('Enter a valid CURP.'),
        'inconvenient': _(u'Enter a CURP with no inconvenient name.'),
    }

    def __init__(self, min_length=18, max_length=18, *args, **kwargs):
        states_re = r'(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)'
        consonants_re = r'[B-DF-HJ-NP-TV-Z]'
        curp_re = ur'^[A-Z]{4}%s[HM]%s%s{3}[0-9A-Z]\d$' % (DATE_RE, states_re,
                                                      consonants_re)
        curp_re = re.compile(curp_re, re.IGNORECASE)
        super(MXCURPField, self).__init__(curp_re, min_length=min_length,
                                          max_length=max_length, *args, **kwargs)

    def clean(self, value):
        value = super(MXCURPField, self).clean(value)
        value = value.upper()
        if value[-1] != self._checksum(value[:-1]):
            raise ValidationError(self.default_error_messages['invalid'])
        if self._has_inconvenient_word(rfc):
            raise ValidationError(self.default_error_messages['inconvenient'])
        return value
    
    def _checksum(self, value):
        curp_chars = u'0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ'
        factor = 19
        sum_ = 0
        for i in range(factor):
            index = curp_chars.index(value[i:i+1])
            factor -= 1
            sum_ += index * factor
        checksum = 10 - sum_ % 10
        if checksum == 10:
          return u'0'
        return unicode(checksum)
    
    def _has_inconvenient_word(self, curp):
        name = curp[:4]
        return name in CURP_INCONVENIENT_WORDS
