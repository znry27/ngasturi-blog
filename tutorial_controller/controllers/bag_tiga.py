# -*- coding: utf-8 -*-
import odoo

from odoo import http, models, fields, _
from odoo.http import request
import json
import unicodedata
import base64
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):
    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        if not product.can_access_from_current_website():
            raise NotFound()

        product_context = dict(request.env.context,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency._convert(price, to_currency, request.env.user.company_id, fields.Date.today())

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'optional_product_ids': [p.with_context({'active_id': p.id}) for p in product.optional_product_ids],
            'get_attribute_exclusions': self._get_attribute_exclusions,
            'available_qty': product.sudo().qty_available, # tambahan tidak ada di source code asli odoo
            'product_uom_name': product.sudo().uom_id.display_name # tambahan tidak ada di source code asli odoo
        }
        return request.render("website_sale.product", values)

class LatihanControllerTiga(http.Controller):

    @http.route('/upload', type='http', website=True)
    def render_upload_form(self, **kwargs):

        return request.render('tutorial_controller.upload_form')

    @http.route('/process/upload', type='http', website=True)
    def process_upload_form(self, **kwargs):
        data = {
            'message': 'Thank you !! We will prosess your Sale Order soon'
        }

        # mendapatkan sale order, berdasarkan input user dengan input name so_id 
        order = request.env['sale.order'].sudo().search([('name','=', kwargs['so_id'])], limit=1)

        # mendapatkan daftar file yang diupload oleh user dengan input name so_file
        files = request.httprequest.files.getlist('so_file')        

        # jika sale order tidak ada karena user memasukkan nomor dokumen yang salah tampilkan pesan
        if not order:
            data['message'] = 'Please input your valid Sale Order number !!!'

        # jika user tidak upload file tampilkan pesan
        if not files:
            data['message'] = 'Please upload your payment form'

        # jika sale order valid dan ada file, simpan file tersebut kedalam model attachment
        # jika res_model dan res_id di isi file yang baru diupload akan tampil di form yang sesuai

        if order and files:
            for ufile in files:
                filename = ufile.filename
                if request.httprequest.user_agent.browser == 'safari':
                    filename = unicodedata.normalize('NFD', ufile.filename)

                try:
                    attachment = request.env['ir.attachment'].sudo().create({
                        'name': filename,
                        'datas': base64.encodestring(ufile.read()),
                        'datas_fname': filename,
                        'res_model': 'sale.order',
                        'res_id': order.id
                    })
                except Exception:
                    data['message'] = 'Sorry something bad happen. Please try again !!!'

        return request.render('tutorial_controller.upload_message', data)