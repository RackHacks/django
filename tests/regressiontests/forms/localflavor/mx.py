# -*- coding: utf-8 -*-
from django.contrib.localflavor.mx.forms import (MXZipCodeField, MXRFCField,
    MXStateSelect, MXCURPField)

from utils import LocalFlavorTestCase


class MXLocalFlavorTests(LocalFlavorTestCase):
    def test_MXStateSelect(self):
        f = MXStateSelect()
        out = u'''<select name="state">
<option value="AGU">Aguascalientes</option>
<option value="BCN">Baja California</option>
<option value="BCS">Baja California Sur</option>
<option value="CAM">Campeche</option>
<option value="CHH">Chihuahua</option>
<option value="CHP">Chiapas</option>
<option value="COA">Coahuila</option>
<option value="COL">Colima</option>
<option value="DIF">Distrito Federal</option>
<option value="DUR">Durango</option>
<option value="GRO">Guerrero</option>
<option value="GUA">Guanajuato</option>
<option value="HID">Hidalgo</option>
<option value="JAL">Jalisco</option>
<option value="MEX">Estado de México</option>
<option value="MIC" selected="selected">Michoacán</option>
<option value="MOR">Morelos</option>
<option value="NAY">Nayarit</option>
<option value="NLE">Nuevo León</option>
<option value="OAX">Oaxaca</option>
<option value="PUE">Puebla</option>
<option value="QUE">Querétaro</option>
<option value="ROO">Quintana Roo</option>
<option value="SIN">Sinaloa</option>
<option value="SLP">San Luis Potosí</option>
<option value="SON">Sonora</option>
<option value="TAB">Tabasco</option>
<option value="TAM">Tamaulipas</option>
<option value="TLA">Tlaxcala</option>
<option value="VER">Veracruz</option>
<option value="YUC">Yucatán</option>
<option value="ZAC">Zacatecas</option>
</select>'''
        self.assertEqual(f.render('state', 'MIC'), out)

    def test_MXZipCodeField(self):
        error_format = [u'Enter a valid zip code in the format XXXXX.']
        valid = {
            '58120': u'58120',
            '58502': u'58502',
            '59310': u'59310',
            '99999': u'99999',
        }
        invalid = {
            '17000': error_format,
            '18000': error_format,
            '19000': error_format,
            '00000': error_format,
        }
        self.assertFieldOutput(MXZipCodeField, valid, invalid)

    def test_MXRFCField(self):
        error_format = [u'Enter a valid RFC.']
        valid = {
            'AA&000606I37': u'AA&000606I37',
            'MED0107173XA': u'MED0107173XA',
            'GAÑ070824GF4': u'GAÑ070824GF4',
            'MED0107173XA': u'MED0107173XA',
            '&A&121212123': u'&A&121212123',
            'MEDA0102293XA': u'MEDA0102293XA',
        }
        invalid = {
            'MED0000000XA': error_format,
            '0000000000XA': error_format,
            # Dates
            'XXX880002XXX': error_format,
            'XXX880200XXX': error_format,
            'XXX880132XXX': error_format,
            'XXX880230XXX': error_format,
            'XXX880431XXX': error_format,
        }
        self.assertFieldOutput(MXRFCField, valid, invalid)

    def test_MXCURPField(self):
        error_format = [u'Enter a valid CURP.']
        valid = {
            'AAMG890608HDFLJL00': u'AAMG890608HDFLJL00',
            'BAAD890419HMNRRV07': u'BAAD890419HMNRRV07',
            'VIAA900930MMNCLL08': u'VIAA900930MMNCLL08',
        }
        invalid = {
            'VIAA900930MMXCLL08': error_format,
        }
        self.assertFieldOutput(MXCURPField, valid, invalid)
