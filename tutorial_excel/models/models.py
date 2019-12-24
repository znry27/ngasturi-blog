# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

class SaleWizard(models.TransientModel):
    _name = 'ng.sale.wizard'


    user_id = fields.Many2many('res.users', string='Sales Person')
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")


    def get_excel_report(self):
        # redirect ke controller /sale/excel_report untuk generate file excel
        return {
            'type': 'ir.actions.act_url',
            'url': '/sale/excel_report/%s' % (self.id),
            'target': 'new',
        }