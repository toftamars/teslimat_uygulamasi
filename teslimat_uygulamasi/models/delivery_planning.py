from odoo import models, fields, api

class TeslimatPlanlama(models.Model):
    _name = 'teslimat.planlama'
    _description = 'Teslimat Planlamasi'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'teslimat_tarihi desc'

    name = fields.Char(string='Teslimat No', required=True, copy=False, 
                      readonly=True, default=lambda self: ('Yeni'))
    siparis_no = fields.Char(string='Sipariş No', required=True, tracking=True)
    musteri = fields.Char(string='Müşteri', required=True, tracking=True)
    teslimat_tarihi = fields.Date(string='Teslimat Tarihi', required=True, tracking=True)
    adres = fields.Text(string='Adres', required=True)
    telefon = fields.Char(string='Telefon')
    email = fields.Char(string='E-posta')
    notlar = fields.Text(string='Notlar')
    
    durum = fields.Selection([
        ('beklemede', 'Beklemede'),
        ('yolda', 'Yolda'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal')
    ], string='Durum', default='beklemede', tracking=True)
    
    urun_ids = fields.One2many('teslimat.planlama.urun', 'teslimat_id', string='Ürünler')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', ('Yeni')) == ('Yeni'):
                vals['name'] = self.env['ir.sequence'].next_by_code('teslimat.planlama') or ('Yeni')
        return super().create(vals_list)

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