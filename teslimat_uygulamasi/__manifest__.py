{
    'name': 'Teslimat Uygulamasi',
    'version': '1.0',
    'category': 'Delivery',
    'summary': 'Teslimat planlama ve takip uygulaması',
    'description': """
        Bu modül teslimat planlaması ve takibi için geliştirilmiştir.
        Özellikler:
        * Teslimat planlaması
        * Teslimat takibi
        * Rota optimizasyonu
        * Teslimat raporları
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'sale', 'stock', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_planning_views.xml',
        'views/menu_views.xml',
        'data/sequence.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': '/teslimat_uygulamasi/static/description/icon.png',
    'assets': {
        'web.assets_backend': [
            'teslimat_uygulamasi/static/src/css/delivery.css',
        ],
    },
    'license': 'LGPL-3',
} 