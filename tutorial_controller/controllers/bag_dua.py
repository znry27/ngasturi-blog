# -*- coding: utf-8 -*-
import odoo

from odoo import http, models, fields, _
from odoo.http import request
import json

class LatihanControllerDua(http.Controller):

    @http.route('/sale/list', type='http')
    def get_sale_list(self, **kwargs):

        orders = request.env['sale.order'].sudo().search([])

        data = {
            'orders' : orders 
        }
        
        return request.render('tutorial_controller.sale_list', data)


    @http.route('/web/sale/list', type='http', website=True)
    def get_web_sale_list(self, **kwargs):

        orders = request.env['sale.order'].sudo().search([])

        data = {
            'orders' : orders 
        }
        
        return request.render('tutorial_controller.website_sale_list', data)

    @http.route('/sale/support', type='http', website=True)
    def sale_support(self, **kwargs):
        # controller ini hanya untuk merender form
        return request.render('tutorial_controller.sale_support')

    @http.route('/sale/support/response', type='http', website=True)
    def sale_support_response(self, **kwargs):
        # controller ini untuk menerima input user
        # input user disimpan di parameter kwargs singkatan dari keyword argument
        # kwargs ini bisa diganti dengan nama lain misal post atau data
        # kwargs bertipe distionary

        data = {
            'name' : kwargs.get('name',''),
            'email' : kwargs.get('email',''),
            'issue' : kwargs.get('issue','')
        }
        
        return request.render('tutorial_controller.sale_support_response', data)