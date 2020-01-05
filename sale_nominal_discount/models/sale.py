# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    # tambah field Diskon Nominal
    discount_nominal = fields.Float(string='Discount Nominal', digits=dp.get_precision('Discount'), default=0.0)

    # hitung diskon nominal
    # override total perhitungan dari odoo
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'discount_nominal')
    def _compute_amount(self):
        for line in self:
            # potong harga setelah dikurangi diskon persentase dengan diskon nominal
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) - line.discount_nominal
            # selanjutanya adalah kode asli odoo
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    # menambah field discount_nominal agar nilainya dibawa ke invoice
    @api.multi
    def _prepare_invoice_line(self, qty):
        # panggil method super untuk mendapatkan field-field yang dibawa ke invoice beserta nilainya
        res = super(SaleLine, self)._prepare_invoice_line(qty)
        # tambahkan field discount_nominal agar nilainya dibawa ke invoice
        res['discount_nominal'] = self.discount_nominal
        return res
