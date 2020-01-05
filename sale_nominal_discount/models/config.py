# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Config(models.TransientModel):
    _inherit = 'res.config.settings'

    # jika field group_discount_nominal ini bernilai True
    # maka semua user akan masuk group sale_nominal_discount.group_discount_nominal
    # sehingga field diskon nominal bisa tampil di form Sale Order
    group_discount_nominal = fields.Boolean("Discount Nominal", implied_group='sale_nominal_discount.group_discount_nominal')