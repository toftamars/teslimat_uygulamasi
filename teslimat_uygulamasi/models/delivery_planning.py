from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class TeslimatPlanlama(models.Model):
    _name = 'teslimat.planlama'
    _description = 'Teslimat Planlamasi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'teslimat_tarihi desc'

    name = fields.Char(string='Teslimat No', required=True, copy=False, 
                      readonly=True, default=lambda self: ('Yeni'))
    
    sale_order_id = fields.Many2one('sale.order', string='Satış Siparişi', required=True, tracking=True,
                                   domain="[('state', 'in', ['sale', 'done'])]")
    
    picking_id = fields.Many2one('stock.picking', string='Transfer', required=True, tracking=True,
                                domain="[('sale_id', '=', sale_order_id)]")
    
    musteri = fields.Many2one('res.partner', string='Müşteri', related='sale_order_id.partner_id', store=True)
    adres = fields.Char(string='Adres', related='picking_id.partner_id.street', store=True)
    telefon = fields.Char(string='Telefon', related='picking_id.partner_id.phone', store=True)
    ek_telefon = fields.Char(string='Ek Telefon')
    
    ilce = fields.Char(string='İlçe', required=True)
    teslimat_tarihi = fields.Date(string='Teslimat Tarihi', required=True, tracking=True)
    
    durum = fields.Selection([
        ('beklemede', 'Beklemede'),
        ('yolda', 'Yolda'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal')
    ], string='Durum', default='beklemede', tracking=True)
    
    urun_ids = fields.One2many('teslimat.planlama.urun', 'teslimat_id', string='Ürünler')
    notlar = fields.Text(string='Notlar')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', ('Yeni')) == ('Yeni'):
                vals['name'] = self.env['ir.sequence'].next_by_code('teslimat.planlama') or ('Yeni')
            
            # Teslimat tarihi kontrolü
            if vals.get('teslimat_tarihi') and vals.get('ilce'):
                self._check_delivery_date(vals['teslimat_tarihi'], vals['ilce'])
                
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('teslimat_tarihi') and vals.get('ilce'):
            self._check_delivery_date(vals['teslimat_tarihi'], vals['ilce'])
        return super().write(vals)

    def _check_delivery_date(self, teslimat_tarihi, ilce):
        # Günlük teslimat limiti kontrolü
        teslimat_sayisi = self.search_count([
            ('teslimat_tarihi', '=', teslimat_tarihi),
            ('ilce', '=', ilce),
            ('durum', 'not in', ['iptal'])
        ])
        
        # Yönetici kontrolü
        is_manager = self.env.user.has_group('stock.group_stock_manager')
        max_delivery = self.env['delivery.limit'].search([('region', '=', ilce)], limit=1)
        max_delivery_count = max_delivery.max_deliveries if max_delivery else 7
        
        if teslimat_sayisi >= max_delivery_count and not is_manager:
            raise UserError(_('Bu ilçe için günlük teslimat limiti (%s) aşıldı. Lütfen başka bir tarih seçin veya yönetici ile iletişime geçin.') % max_delivery_count)
        
        # İlçe kontrolü
        schedule = self.env['delivery.schedule'].search([
            ('region', '=', ilce),
            ('day', '=', teslimat_tarihi.strftime('%A').lower())
        ])
        
        if not schedule and not is_manager:
            raise UserError(_('Bu ilçe için seçilen günde teslimat yapılamaz. Lütfen başka bir tarih seçin veya yönetici ile iletişime geçin.'))

    def action_tamamlandi(self):
        self.write({'durum': 'tamamlandi'})

    def action_iptal(self):
        self.write({'durum': 'iptal'})

class TeslimatPlanlamaUrun(models.Model):
    _name = 'teslimat.planlama.urun'
    _description = 'Teslimat Planlama Ürünleri'

    teslimat_id = fields.Many2one('teslimat.planlama', string='Teslimat', required=True, ondelete='cascade')
    urun_adi = fields.Char(string='Ürün Adı', required=True)
    miktar = fields.Float(string='Miktar', required=True, default=1.0)
    birim = fields.Selection([
        ('adet', 'Adet'),
        ('kg', 'KG'),
        ('lt', 'Litre')
    ], string='Birim', required=True, default='adet')
    notlar = fields.Text(string='Notlar') 