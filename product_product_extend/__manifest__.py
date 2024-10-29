{
    'name': 'Product Report Excel',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Generate product report in Excel format',
    'description': """
        This module adds a button to the product form to generate an Excel report
        with product details including last purchase and sale dates.
    """,
    'author': 'Monserrat',
    'depends': ['product', 'purchase', 'sale'],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
}
