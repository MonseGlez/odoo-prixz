{
    'name': 'Sale Order Notification',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Send email notification when a sale order is confirmed',
    'author': 'Your Company',
    'depends': ['sale', 'mail'],
    'data': [
        'views/email_template_sale_order.xml',  # Incluyendo la plantilla de correo electrónico
    ],
    'installable': True,
    'application': False,
}
