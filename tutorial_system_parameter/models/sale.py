# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        # baca system parameter dengan key 'allowed_warehouse'
        # jika tidak ada akan return string kosong
        # kemudian kita split berdasarkan karakter koma agar jadi list

        allowed_warehouse = self.env['ir.config_parameter'].get_param('allowed_warehouse', '').split(',')
        
        # karena system parameter disimpan dalam bentuk teks kita ubah jadi integer dulu
        allowed_warehouse = list(map(lambda x: int(x), allowed_warehouse))

        # kita cek field warehouse yang di pilih user ada di daftar warehouse yang diperbolehkan atau tidak

        if vals.get('warehouse_id', False) and vals.get('warehouse_id', False) not in allowed_warehouse:
            raise exceptions.ValidationError('Anda tidak boleh membuat Sale Order dengan warehouse ini !')


        return super(SaleOrder, self).create(vals)


    def write(self, vals):
        # baca system parameter dengan key 'allowed_warehouse'
        # jika tidak ada akan return string kosong
        # kemudian kita split berdasarkan karakter koma agar jadi list

        allowed_warehouse = self.env['ir.config_parameter'].get_param('allowed_warehouse', '').split(',')

        # karena system parameter disimpan dalam bentuk teks kita ubah jadi integer dulu
        allowed_warehouse = list(map(lambda x: int(x), allowed_warehouse))

        # kita cek field warehouse yang di pilih user ada di daftar warehouse yang diperbolehkan atau tidak

        if vals.get('warehouse_id', False) and vals.get('warehouse_id', False) not in allowed_warehouse:
            raise exceptions.ValidationError('Anda tidak boleh membuat Sale Order dengan warehouse ini !')


        return super(SaleOrder, self).write(vals)

    def unlink(self):        
        for rec in self:
            deleted = int(self.env['ir.config_parameter'].get_param('deleted_sale_order', '0')) + 1
            self.env['ir.config_parameter'].set_param('deleted_sale_order', deleted)

        return super(SaleOrder, self).unlink()