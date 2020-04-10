# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ConfirmSaleTrust(models.TransientModel):
    _name = 'sale.trust.wizard'

    order_id = fields.Many2one('sale.order', string='Sale Order')
    partner_id = fields.Many2one('res.partner', string='Customer', related='order_id.partner_id')

    def approve_blacklisted_customer_order(self):
        # panggil method action_confirm pada sale order saat ini
        # sertakan context agar bisa mencegah infinite loop
        self.order_id.with_context({'approve_blacklisted_customer_order': 1}).action_confirm()