from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def _send_order_confirmation_email(self):
        """Este método envía un correo electrónico al cliente cuando la orden de venta es confirmada."""

        template_id = self.env.ref('sale_order_notification.email_template_sale_order_confirmed').id
        if template_id:
            self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def action_confirm(self):
        # Llama a la función original para confirmar la orden
        res = super(SaleOrder, self).action_confirm()

        # Envía el correo al cliente después de confirmar la orden
        for order in self:
            if order.partner_id.email:
                order._send_order_confirmation_email()
        

        return res
