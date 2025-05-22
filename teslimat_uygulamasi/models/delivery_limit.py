from odoo import models, fields, api

class DeliveryLimit(models.Model):
    _name = 'delivery.limit'
    _description = 'Teslimat Limiti'

    region = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası')
    ], string='Bölge', required=True)
    
    max_deliveries = fields.Integer(string='Günlük Maksimum Teslimat', required=True,
        help='Bir günde yapılabilecek maksimum teslimat sayısı') 