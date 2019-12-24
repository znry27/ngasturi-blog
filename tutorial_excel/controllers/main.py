# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
    


class SaleExcelReportController(http.Controller):
    @http.route([
        '/sale/excel_report/<model("ng.sale.wizard"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_sale_excel_report(self,wizard=None,**args):
        # wizard ini adalah model yang dikirim dengan method get_excel_report
        # pada model ng.sale.wizard
        # berisi data sales person, tanggal mulai dan tanggal akhir

        # buat response dengan header berupa file excel
        # agar browser segera mendownload response
        # header Content-Disposition ini adalah nama file
        # isi sesuai kebutuhan

        response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition('Sales Report in Excel Format' + '.xlsx'))
                    ]
                )

        # buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # buat style untuk mengatur jenis font, ukuran font, border dan alligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 14, 'bold': True, 'align': 'center'})
        header_style = workbook.add_format({'font_name': 'Times', 'bold': True, 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'center'})
        text_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'left'})
        number_style = workbook.add_format({'font_name': 'Times', 'left': 1, 'bottom':1, 'right':1, 'top':1, 'align': 'right'})

        # loop user / sales person yang dipilih
        for user in wizard.user_id:
            # buat worksheet / tab per user 
            sheet = workbook.add_worksheet(user.name)
            # set orientation jadi landscape
            sheet.set_landscape()
            # set ukuran kertas, 9 artinya kertas A4
            sheet.set_paper(9)
            # set margin kertas dalam satuan inchi
            sheet.set_margins(0.5,0.5,0.5,0.5)

            # set lebar kolom
            sheet.set_column('A:A', 5)
            sheet.set_column('B:E', 15)

            # judul report
            # merge cell A1 sampai E1 dengan ukuran font 14 dan bold
            sheet.merge_range('A1:E1', 'Sales Report in Excel Format', title_style)
            
            # judul tabel
            sheet.write(1, 0, 'No.', header_style)
            sheet.write(1, 1, 'No. Dokumen', header_style)
            sheet.write(1, 2, 'Tanggal', header_style)
            sheet.write(1, 3, 'Pelanggan', header_style)
            sheet.write(1, 4, 'Total', header_style)

            row = 2
            number = 1

            # cari sale order untuk sales person terpilih pada rentang tanggal yang dipilih user
            orders = request.env['sale.order'].search([('user_id','=',user.id), ('date_order','>=', wizard.start_date), ('date_order','<=', wizard.end_date)])
            for order in orders:
                # content / isi report
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, order.name, text_style)
                sheet.write(row, 2, str(order.date_order), text_style)
                sheet.write(row, 3, order.partner_id.name, text_style)
                sheet.write(row, 4, order.amount_total, number_style)

                row += 1
                number += 1

            # buat formula untuk men-sum / mentotal sales per user
            sheet.merge_range('A' + str(row+1) + ':D' + str(row+1), 'Total', text_style)
            sheet.write_formula(row, 4, '=SUM(E3:E' + str(row) + ')', number_style)

        # masukkan file excel yang sudah digenerate ke response dan return 
        # sehingga browser bisa menerima response dan mendownload file yang sudah digenerate
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response