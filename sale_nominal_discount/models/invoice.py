# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class Invoice(models.Model):
    _inherit = 'account.invoice'

    # hitung tax / pajak
    # override total perhitungan dari odoo
    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.invoice_line_ids:
            if not line.account_id:
                continue

            # potong harga setelah dikurangi diskon persentase dengan diskon nominal
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0) - line.discount_nominal
            
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
        return tax_grouped

class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # tambah field Diskon Nominal
    discount_nominal = fields.Float(string='Discount Nominal', digits=dp.get_precision('Discount'), default=0.0)

    # hitung diskon nominal
    # override total perhitungan dari odoo
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date', 'discount_nominal')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        # potong harga setelah dikurangi diskon persentase dengan diskon nominal
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0) - self.discount_nominal
        # selanjutanya adalah kode asli odoo
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

