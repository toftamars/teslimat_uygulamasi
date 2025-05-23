{
    'name': 'Teslimat Uygulamasi',
    'version': '1.0',
    'category': 'Operations/Delivery',
    'summary': 'Teslimat planlama ve takip uygulamasidir',
    'description': """
        Bu modul, Odoo ERP sistemi icin teslimat planlama ve takip uygulamasidir.
        Ozellikler:
        - Onaylanmis satis siparislerine gore teslimat planlamasi
        - Transfer olusturma
        - Teslimat takibi
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_planning_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'teslimat_uygulamasi/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': '/teslimat_uygulamasi/static/description/Kamyonikon.png',
} 