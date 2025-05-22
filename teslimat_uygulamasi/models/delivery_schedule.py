from odoo import models, fields, api

class DeliverySchedule(models.Model):
    _name = 'delivery.schedule'
    _description = 'Teslimat Programı'

    region = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası')
    ], string='Bölge', required=True)
    
    day = fields.Selection([
        ('pazartesi', 'Pazartesi'),
        ('sali', 'Salı'),
        ('carsamba', 'Çarşamba'),
        ('persembe', 'Perşembe'),
        ('cuma', 'Cuma'),
        ('cumartesi', 'Cumartesi'),
        ('pazar', 'Pazar')
    ], string='Gün', required=True)
    
    districts = fields.Char(string='İlçeler', required=True,
        help='Virgülle ayrılmış ilçe listesi') 