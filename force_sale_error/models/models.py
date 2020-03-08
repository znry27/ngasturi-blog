# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)

        raise exceptions.ValidationError('Dibuat error. Cek Sale Order Sequence')