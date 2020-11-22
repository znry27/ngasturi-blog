# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime, timedelta

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def cancel_old_sales_order(self, force_limit=None):
        # batas hari
        limit = 7

        # cek apakah user mengisi nilai force_limit atau tidak
        if force_limit:
            limit = force_limit

        # tanggal hari ini
        date_today = datetime.today()

        # tanggal yang seharusnya sudah boleh dicancel
        cancel_date = date_today - timedelta(days = limit)

        # cari sales order yang tanggalnya sesuai dan belum di confirm
        old_order = self.env['sale.order'].search([('date_order', '<', cancel_date), ('state','in', ['draft','sent'])])
        # cancel sales order yang sesuai kriteria
        old_order.action_cancel()
        print(date_today)
        print(cancel_date)
        print(old_order)
