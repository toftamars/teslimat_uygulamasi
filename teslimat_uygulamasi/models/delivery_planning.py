from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TeslimatPlanlama(models.Model):
    _name = 'teslimat.planlama'
    _description = 'Teslimat Planlaması'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'teslimat_tarihi asc'

    name = fields.Char(string='Teslimat No', required=True, copy=False, readonly=True, default=lambda self: _('Yeni'))
    sale_order_id = fields.Many2one('sale.order', string='Satış Siparişi', tracking=True)
    pos_order_id = fields.Many2one('pos.order', string='POS Siparişi', tracking=True)
    picking_id = fields.Many2one('stock.picking', string='Sevkiyat', tracking=True)
    musteri = fields.Many2one('res.partner', string='Müşteri', required=True, tracking=True)
    ilce = fields.Selection([
        ('adalar', 'Adalar'),
        ('arnavutkoy', 'Arnavutköy'),
        ('atasehir', 'Ataşehir'),
        ('avcilar', 'Avcılar'),
        ('bagcilar', 'Bağcılar'),
        ('bahcelievler', 'Bahçelievler'),
        ('bakirkoy', 'Bakırköy'),
        ('basaksehir', 'Başakşehir'),
        ('bayrampasa', 'Bayrampaşa'),
        ('besiktas', 'Beşiktaş'),
        ('beykoz', 'Beykoz'),
        ('beylikduzu', 'Beylikdüzü'),
        ('beyoglu', 'Beyoğlu'),
        ('buyukcekmece', 'Büyükçekmece'),
        ('catalca', 'Çatalca'),
        ('cekmekoy', 'Çekmeköy'),
        ('esenler', 'Esenler'),
        ('esenyurt', 'Esenyurt'),
        ('eyup', 'Eyüp'),
        ('fatih', 'Fatih'),
        ('gaziosmanpasa', 'Gaziosmanpaşa'),
        ('gungoren', 'Güngören'),
        ('kadikoy', 'Kadıköy'),
        ('kagithane', 'Kağıthane'),
        ('kartal', 'Kartal'),
        ('kucukcekmece', 'Küçükçekmece'),
        ('maltepe', 'Maltepe'),
        ('pendik', 'Pendik'),
        ('sariyer', 'Sarıyer'),
        ('silivri', 'Silivri'),
        ('sultanbeyli', 'Sultanbeyli'),
        ('sultangazi', 'Sultangazi'),
        ('sile', 'Şile'),
        ('sisli', 'Şişli'),
        ('tuzla', 'Tuzla'),
        ('umraniye', 'Ümraniye'),
        ('uskudar', 'Üsküdar'),
        ('zeytinburnu', 'Zeytinburnu')
    ], string='İlçe', required=True, tracking=True)
    adres = fields.Char(string='Adres', tracking=True)
    telefon = fields.Char(string='Telefon', tracking=True)
    ek_telefon = fields.Char(string='Ek Telefon', tracking=True)
    teslimat_tarihi = fields.Date(string='Teslimat Tarihi', required=True, tracking=True)
    durum = fields.Selection([
        ('beklemede', 'Beklemede'),
        ('yolda', 'Yolda'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal')
    ], string='Durum', default='beklemede', tracking=True)
    notlar = fields.Text(string='Notlar', tracking=True)
    urun_ids = fields.One2many('teslimat.planlama.urun', 'teslimat_id', string='Ürünler', readonly=True)
    teslimat_sira = fields.Integer(string='Teslimat Sırası', default=0)
    teslimat_grubu = fields.Char(string='Teslimat Grubu')
    teslimat_bolgesi = fields.Char(string='Teslimat Bölgesi')
    teslimat_rota = fields.Char(string='Teslimat Rotası')
    teslimat_km = fields.Float(string='Teslimat KM', digits=(10,2))
    teslimat_suresi = fields.Float(string='Teslimat Süresi (dk)', digits=(10,2))
    teslimat_maliyeti = fields.Float(string='Teslimat Maliyeti', digits=(10,2))
    teslimat_personeli = fields.Many2one('res.users', string='Teslimat Personeli')
    teslimat_araci = fields.Char(string='Teslimat Aracı')
    teslimat_plaka = fields.Char(string='Teslimat Plaka')
    teslimat_baslangic = fields.Datetime(string='Teslimat Başlangıç')
    teslimat_bitis = fields.Datetime(string='Teslimat Bitiş')
    teslimat_guncelleme = fields.Datetime(string='Son Güncelleme')
    teslimat_konum = fields.Char(string='Teslimat Konumu')
    teslimat_koordinat = fields.Char(string='Teslimat Koordinat')
    teslimat_resim = fields.Binary(string='Teslimat Resmi')
    teslimat_imza = fields.Binary(string='Teslimat İmza')
    teslimat_belge = fields.Binary(string='Teslimat Belgesi')
    teslimat_fatura = fields.Binary(string='Teslimat Fatura')
    teslimat_irsaliye = fields.Binary(string='Teslimat İrsaliye')
    teslimat_rapor = fields.Binary(string='Teslimat Rapor')
    teslimat_log = fields.Text(string='Teslimat Log')
    teslimat_uyari = fields.Text(string='Teslimat Uyarı')
    teslimat_hata = fields.Text(string='Teslimat Hata')
    teslimat_bilgi = fields.Text(string='Teslimat Bilgi')
    teslimat_detay = fields.Text(string='Teslimat Detay')
    teslimat_ozet = fields.Text(string='Teslimat Özet')
    teslimat_istatistik = fields.Text(string='Teslimat İstatistik')
    teslimat_analiz = fields.Text(string='Teslimat Analiz')
    teslimat_raporlama = fields.Text(string='Teslimat Raporlama')
    teslimat_optimizasyon = fields.Text(string='Teslimat Optimizasyon')
    teslimat_planlama = fields.Text(string='Teslimat Planlama')
    teslimat_takip = fields.Text(string='Teslimat Takip')
    teslimat_yonetim = fields.Text(string='Teslimat Yönetim')
    teslimat_sistem = fields.Text(string='Teslimat Sistem')
    teslimat_entegrasyon = fields.Text(string='Teslimat Entegrasyon')
    teslimat_api = fields.Text(string='Teslimat API')
    teslimat_web = fields.Text(string='Teslimat Web')
    teslimat_mobil = fields.Text(string='Teslimat Mobil')
    teslimat_sms = fields.Text(string='Teslimat SMS')
    teslimat_email = fields.Text(string='Teslimat Email')
    teslimat_bildirim = fields.Text(string='Teslimat Bildirim')
    teslimat_uyari_bildirim = fields.Text(string='Teslimat Uyarı Bildirim')
    teslimat_hata_bildirim = fields.Text(string='Teslimat Hata Bildirim')
    teslimat_bilgi_bildirim = fields.Text(string='Teslimat Bilgi Bildirim')
    teslimat_detay_bildirim = fields.Text(string='Teslimat Detay Bildirim')
    teslimat_ozet_bildirim = fields.Text(string='Teslimat Özet Bildirim')
    teslimat_istatistik_bildirim = fields.Text(string='Teslimat İstatistik Bildirim')
    teslimat_analiz_bildirim = fields.Text(string='Teslimat Analiz Bildirim')
    teslimat_raporlama_bildirim = fields.Text(string='Teslimat Raporlama Bildirim')
    teslimat_optimizasyon_bildirim = fields.Text(string='Teslimat Optimizasyon Bildirim')
    teslimat_planlama_bildirim = fields.Text(string='Teslimat Planlama Bildirim')
    teslimat_takip_bildirim = fields.Text(string='Teslimat Takip Bildirim')
    teslimat_yonetim_bildirim = fields.Text(string='Teslimat Yönetim Bildirim')
    teslimat_sistem_bildirim = fields.Text(string='Teslimat Sistem Bildirim')
    teslimat_entegrasyon_bildirim = fields.Text(string='Teslimat Entegrasyon Bildirim')
    teslimat_api_bildirim = fields.Text(string='Teslimat API Bildirim')
    teslimat_web_bildirim = fields.Text(string='Teslimat Web Bildirim')
    teslimat_mobil_bildirim = fields.Text(string='Teslimat Mobil Bildirim')
    teslimat_sms_bildirim = fields.Text(string='Teslimat SMS Bildirim')
    teslimat_email_bildirim = fields.Text(string='Teslimat Email Bildirim')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Yeni')) == _('Yeni'):
                vals['name'] = self.env['ir.sequence'].next_by_code('teslimat.planlama') or _('Yeni')
        return super().create(vals_list)

    @api.onchange('musteri')
    def _onchange_musteri(self):
        if self.musteri:
            self.adres = self.musteri.street
            self.telefon = self.musteri.phone
            self.ek_telefon = self.musteri.mobile

    @api.onchange('sale_order_id')
    def _onchange_sale_order(self):
        if self.sale_order_id:
            self.musteri = self.sale_order_id.partner_id
            self.picking_id = self.sale_order_id.picking_ids.filtered(lambda p: p.picking_type_code == 'outgoing')[:1]
            self._onchange_musteri()

    @api.onchange('pos_order_id')
    def _onchange_pos_order(self):
        if self.pos_order_id:
            self.musteri = self.pos_order_id.partner_id
            self._onchange_musteri()

    def action_tamamlandi(self):
        self.write({'durum': 'tamamlandi'})

    def action_iptal(self):
        self.write({'durum': 'iptal'})

    def action_yolda(self):
        self.write({'durum': 'yolda'})

    def action_beklemede(self):
        self.write({'durum': 'beklemede'})

    def action_yeniden_planla(self):
        self.write({'durum': 'beklemede'})

    def action_teslimat_raporu(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Raporu',
            'res_model': 'teslimat.rapor',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_takip(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Takip',
            'res_model': 'teslimat.takip',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_yonetim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Yönetim',
            'res_model': 'teslimat.yonetim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_sistem(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Sistem',
            'res_model': 'teslimat.sistem',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_entegrasyon(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Entegrasyon',
            'res_model': 'teslimat.entegrasyon',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_api(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat API',
            'res_model': 'teslimat.api',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_web(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Web',
            'res_model': 'teslimat.web',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_mobil(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Mobil',
            'res_model': 'teslimat.mobil',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_sms(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat SMS',
            'res_model': 'teslimat.sms',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_email(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Email',
            'res_model': 'teslimat.email',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Bildirim',
            'res_model': 'teslimat.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_uyari_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Uyarı Bildirim',
            'res_model': 'teslimat.uyari.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_hata_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Hata Bildirim',
            'res_model': 'teslimat.hata.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_bilgi_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Bilgi Bildirim',
            'res_model': 'teslimat.bilgi.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_detay_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Detay Bildirim',
            'res_model': 'teslimat.detay.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_ozet_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Özet Bildirim',
            'res_model': 'teslimat.ozet.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_istatistik_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat İstatistik Bildirim',
            'res_model': 'teslimat.istatistik.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_analiz_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Analiz Bildirim',
            'res_model': 'teslimat.analiz.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_raporlama_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Raporlama Bildirim',
            'res_model': 'teslimat.raporlama.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_optimizasyon_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Optimizasyon Bildirim',
            'res_model': 'teslimat.optimizasyon.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_planlama_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Planlama Bildirim',
            'res_model': 'teslimat.planlama.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_takip_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Takip Bildirim',
            'res_model': 'teslimat.takip.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_yonetim_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Yönetim Bildirim',
            'res_model': 'teslimat.yonetim.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_sistem_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Sistem Bildirim',
            'res_model': 'teslimat.sistem.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_entegrasyon_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Entegrasyon Bildirim',
            'res_model': 'teslimat.entegrasyon.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_api_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat API Bildirim',
            'res_model': 'teslimat.api.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_web_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Web Bildirim',
            'res_model': 'teslimat.web.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_mobil_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Mobil Bildirim',
            'res_model': 'teslimat.mobil.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_sms_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat SMS Bildirim',
            'res_model': 'teslimat.sms.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

    def action_teslimat_email_bildirim(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teslimat Email Bildirim',
            'res_model': 'teslimat.email.bildirim',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_teslimat_id': self.id,
            }
        }

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