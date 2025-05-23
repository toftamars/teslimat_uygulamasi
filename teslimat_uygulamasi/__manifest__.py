{
    'name': 'Teslimat Uygulaması',
    'version': '1.0',
    'category': 'Delivery',
    'summary': 'Teslimat planlama ve takip uygulaması',
    'description': """
        Teslimat planlama ve takip uygulaması
        - Teslimat planlaması
        - Teslimat takibi
        - Teslimat ekibi yönetimi
        - Teslimat raporları
    """,
    'author': 'Alper',
    'website': 'https://www.example.com',
    'depends': [
        'base',
        'mail',
        'web',
        'stock',
        'sale',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/delivery_planning_views.xml',
        'views/delivery_team_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'teslimat_uygulamasi/static/src/css/delivery.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
} 