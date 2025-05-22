{
    'name': 'Teslimat Uygulaması',
    'version': '1.0',
    'category': 'Delivery',
    'summary': 'Satış siparişlerinden teslimat planlaması',
    'description': """
        Bu modül, onaylanmış ve transferleri oluşturulmuş satış siparişlerinden
        teslimat planlaması yapmanızı sağlar.
        
        Özellikler:
        - Bölge bazlı teslimat planlaması
        - Günlük maksimum teslimat sayısı kontrolü
        - Teslimat durumu takibi (Yüklendi, Yolda, Tamamlandı)
        - SMS ve Email bildirimleri
        - QR kod ile teslimat onayı
        - Tahmini teslimat zamanı
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'sale', 'stock', 'point_of_sale', 'mail', 'sms'],
    'data': [
        'security/ir.model.access.csv',
        'data/delivery_config.py',
        'data/mail_template.xml',
        'views/delivery_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
} 