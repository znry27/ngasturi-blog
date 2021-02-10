# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions, _

class MyService(models.Model):    
    _name = 'my.service'

    # sebaiknya _description anda isi
    # isi dengan nama yang pantas, agar saat dibaca di chatter juga enak
    _description = 'Service'

    # bagian ini wajib, jika anda menginginkan fungsi chatter
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    # perhatikan pada bagian track_visibility
    name = fields.Char('Nomor Service', track_visibility='onchange')
    pelanggan = fields.Many2one('res.partner','Pelanggan', track_visibility='onchange')
    tanggal = fields.Date('Tanggal')
    service_detail = fields.One2many('my.service.detail', 'service_id')


class MyServiceDetail(models.Model):    
    _name = 'my.service.detail'

    # sebaiknya _description anda isi
    # isi dengan nama yang pantas, agar saat dibaca di chatter juga enak
    _description = 'Service Detail'

    # bagian ini wajib, jika anda menginginkan fungsi chatter
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    # perhatikan pada bagian track_visibility
    product = fields.Many2one('product.product', 'Product', track_visibility='onchange')
    keluhan = fields.Char('Keluhan', track_visibility='onchange')
    garansi = fields.Boolean('Garansi')
    service_id = fields.Many2one('my.service')



