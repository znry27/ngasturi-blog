# -*- coding: utf-8 -*-
import odoo

from odoo import http, models, fields, _
from odoo.http import request
import json

class LatihanController(http.Controller):

    @http.route('/sale')
    def get_sale(self, **kwargs):
        value = {
            'order_id': 'S0001',
            'customer': 'Agus Budianto',
            'total': 4000000
        }

        return json.dumps(value)

    @http.route([
            '/sale2', #routing 1
            '/sale2/<int:order_id>', #routing 2
            '/sale2/<int:order_id>/<int:show_detail>' # routing 3
        ])
    def get_sale2(self,order_id=None,show_detail=None, **kwargs):
        """
            Perhatikan kode <int:order_id>. Kode ini disebut placeholder
            Placeholder adalah bagian yang dinamis dari suatu routing
            User bisa memasukkan data apa saja asalkan sesuai rule
            Misal jika rule-nya adalah interger jika dimasukkan string maka akan error 404
                    
            Jika user mengakses http://localhost:8069/sale2 artinya routing 1 yang dipanggil
            Maka nilai order_id dan show_detail tidak terisi atau None

            Jika user mengakses http://localhost:8069/sale2/5 artinya routing 2 yang dipanggil
            Nilai 5 akan dimasukkan sebagai argumen order_id pada method get_sale2
            Jadi nilai order_id akan jadi 5 dan show_detail tetap None

            Jika user mengakses http://localhost:8069/sale2/S0001 akan error 404
            Karena tipe data yang dibutuhkan oleh placeholder order_id adalah interger bukan string

            Jika user mengakses http://localhost:8069/sale2/5/1 artinya routing 3 yang dipanggil
            Jadi nila argumen order_id = 5 dan show_detail = 1
        """        

        # return value ini jika dipanggil http://localhost:8069/sale2
        value = [
            {
                'order_id': 'S0001',
                'customer': 'Agus Budianto',
                'total': 4000000
            },
                {
                'order_id': 'S0002',
                'customer': 'Dani',
                'total': 5000000
            }
        ]

        if order_id:
            # return value ini jika dipanggil http://localhost:8069/sale2/5
            value = {
                'order_id': order_id,
                'customer': 'Customer with order id' + str(order_id),
                'total': 4000000
            }

            if show_detail:
                # return value ini jika dipanggil http://localhost:8069/sale2/5/1
                value['details'] = [
                    {'product': 'Indomie Goreng', 'qty': 2},
                    {'product': 'Kecap Bango', 'qty': 1}
                ]

        return json.dumps(value)

    @http.route([
            '/sale3', #routing 1
            '/sale3/<int:order_id>', #routing 2
            '/sale3/<int:order_id>/<int:show_detail>' # routing 3
        ])
    def get_sale3(self,order_id=None,show_detail=None, **kwargs):
        
        value = []

        if not order_id and not show_detail:
            # jika order_id dan show_detail = None (panggil routing 1)
            # kita return semua SO dari database
            orders = request.env['sale.order'].search([])
            for order in orders:
                value.append({
                        'order_id' : order.name,
                        'customer': order.partner_id.name,
                        'total': order.amount_total
                    })
        else:
            # jika ada order_id (panggil routing 2) 
            # kita tampilkan hanya satu SO sesuai id yang direquest
            order = request.env['sale.order'].search([('id','=',order_id)])
            if order:
                value = {
                        'order_id' : order.name,
                        'customer': order.partner_id.name,
                        'total': order.amount_total
                    }

                if show_detail:
                    # jika ada show_detail (panggil routing 3) 
                    # kita tampilkan detail product pada SO
                    details = []
                    for line in order.order_line:
                        details.append({
                                'product': line.product_id.name,
                                'qty': line.product_uom_qty
                            })

                    value.update({'details': details})


        return json.dumps(value)


    @http.route([
            '''/sale4''', #routing 1
            '''/sale4/<model("sale.order", "[('state', 'not in', ('cancel'))]"):order_id>''', #routing 2
            '''/sale4/<model("sale.order", "[('state', 'not in', ('cancel'))]"):order_id>/<int:show_detail>''' # routing 3
        ], type='http', auth='public')
    def get_sale4(self,order_id=None,show_detail=None, **kwargs):
        
        value = []

        if not order_id and not show_detail:
            # jika order_id dan show_detail = None (panggil routing 1)
            # kita return semua SO dari database
            orders = request.env['sale.order'].search([])
            for order in orders:
                value.append({
                        'order_id' : order.name,
                        'customer': order.partner_id.name,
                        'total': order.amount_total
                    })
        else:
            # jika ada order_id (panggil routing 2) 
            # kita tampilkan hanya satu SO sesuai id yang direquest

            # karena sudah menggunakan placeholder model, kita tidak perlu melakukan search
            # order_id sudah merupakan object mode yang merupakan representasi data dari database
            
            if order_id:
                value = {
                        'order_id' : order_id.name,
                        'customer': order_id.partner_id.name,
                        'total': order_id.amount_total
                    }

                if show_detail:
                    # jika ada show_detail (panggil routing 3) 
                    # kita tampilkan detail product pada SO
                    details = []
                    for line in order_id.order_line:
                        details.append({
                                'product': line.product_id.name,
                                'qtys': line.product_uom_qty
                            })

                    value.update({'details': details})


        return json.dumps(value)



    @http.route([
            '/sale5', #routing 1
            '/sale5/<int:order_id>', #routing 2
            '/sale5/<int:order_id>/<int:show_detail>' # routing 3
        ], 
        type="http", # tipe request bisa diisi http / json
        auth="public", # Authentication bisa diisi user, public atau none
        csrf=False, # True atau False
        )
    def get_sale5(self,order_id=None,show_detail=None, **kwargs):
        
        value = []

        if not order_id and not show_detail:
            # jika order_id dan show_detail = None (panggil routing 1)
            # kita return semua SO dari database

            # karena kita belum set hak akses untuk public user kita gunakan perintah sudo
            orders = request.env['sale.order'].sudo().search([])
            for order in orders:
                value.append({
                        'order_id' : order.name,
                        'customer': order.partner_id.name,
                        'total': order.amount_total
                    })
        else:
            # jika ada order_id (panggil routing 2) 
            # kita tampilkan hanya satu SO sesuai id yang direquest
            order = request.env['sale.order'].sudo().search([('id','=',order_id)])
            if order:
                value = {
                        'order_id' : order.name,
                        'customer': order.partner_id.name,
                        'total': order.amount_total
                    }

                if show_detail:
                    # jika ada show_detail (panggil routing 3) 
                    # kita tampilkan detail product pada SO
                    details = []
                    for line in order.order_line:
                        details.append({
                                'product': line.product_id.name,
                                'qty': line.product_uom_qty
                            })

                    value.update({'details': details})


        return json.dumps(value)
