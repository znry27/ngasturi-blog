# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # jika partner tidak diblacklist panggil super, artinya sale order bisa di confirm
        # jika ada context approve_blacklisted_customer_order artinya method ini
        # dipanggil dari transient model sale.trust.wizard dan user memiliki
        # hak akses 'Approve sale order of blacklisted customer' sehingga sale order bisa di confirm
        if self.partner_id.trust_state == 'trusted' or 'approve_blacklisted_customer_order' in self._context:
            super(SaleOrder, self).action_confirm()

        else:
            # partner di blacklist
            # buat record transient model dengan nilai order_id adalah sale order saat ini
            # dengan memasukkan order_id nantinya di transient model sale.trust.wizard
            # kita bisa memanggil method action_confirm hanya untuk sale order saat ini
            wizard_id = self.env['sale.trust.wizard'].create({'order_id': self.id})
            return {
                'name': _('Blacklisted Customer'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.trust.wizard',
                'res_id': wizard_id.id,
                'target': 'new',
            }