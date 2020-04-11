# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import requests

class DinamicReport(models.AbstractModel):
    _name = 'report.tutorial_abstract_model.dinamyc_report_example'

    @api.model
    def _get_report_values(self, docids, data=None):
        # anggap saja ini adalah prose yang rumit atau ambil data dari server lain
        result = requests.get(url = 'https://kodepos-2d475.firebaseio.com/kota_kab/k69.json?print=pretty') 
        datas = result.json()

        # return data agar bisa dirender
        return {'datas': datas}
