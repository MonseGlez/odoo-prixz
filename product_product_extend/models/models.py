from odoo import models
import xlsxwriter
import base64
from io import BytesIO

class Product(models.Model):
    _inherit = 'product.template'

    def generate_product_report(self):
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Productos")
        headers = ['Product ID', 'Product Name', 'Barcode', 'Last Purchase Date', 'Last Sale Date']
        worksheet.write_row(0, 0, headers)

        query = """
            SELECT 
                pp.id AS product_id,
                pt.name AS product_name,
                pp.barcode AS barcode,
                MAX(po.date_order) AS last_purchase_date,
                MAX(s.date_order) AS last_sale_date
            FROM 
                product_product pp
            JOIN 
                product_template pt ON pp.product_tmpl_id = pt.id
            LEFT JOIN 
                purchase_order_line pol ON pol.product_id = pp.id
            LEFT JOIN 
                purchase_order po ON po.id = pol.order_id
            LEFT JOIN 
                sale_order_line sol ON sol.product_id = pp.id
            LEFT JOIN 
                sale_order s ON s.id = sol.order_id
            GROUP BY 
                pp.id, pt.name, pp.barcode
            ORDER BY 
                pt.name;
        """
        
        self.env.cr.execute(query)
        results = self.env.cr.fetchall()

        for row_idx, row in enumerate(results, start=1):
            if isinstance(row, tuple):
                worksheet.write_row(row_idx, 0, row)
            else:
                worksheet.write_row(row_idx, 0, list(row))

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        self.env['ir.attachment'].create({
            'name': 'product_report.xlsx',
            'type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'datas': file_data,
            'res_model': 'product.product',
            'res_id': self.id,
        })