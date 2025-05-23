from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class TeslimatPlanlama(models.Model):
    _name = 'teslimat.planlama'
    _description = 'Teslimat Planlaması'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'teslimat_tarihi asc'

    # İlçe-Teslimat Günü Eşleştirmesi
    ILCE_TESLIMAT_GUNLERI = {
        'kadikoy': [1, 3, 5],  # Pazartesi, Çarşamba, Cuma
        'uskudar': [2, 4, 6],  # Salı, Perşembe, Cumartesi
        'atasehir': [1, 4],    # Pazartesi, Perşembe
        'umraniye': [2, 5],    # Salı, Cuma
        'maltepe': [3, 6],     # Çarşamba, Cumartesi
        'kartal': [1, 4],      # Pazartesi, Perşembe
        'pendik': [2, 5],      # Salı, Cuma
        'tuzla': [3, 6],       # Çarşamba, Cumartesi
        'sultanbeyli': [1, 4], # Pazartesi, Perşembe
        'sile': [2, 5],        # Salı, Cuma
        'catalca': [3, 6],     # Çarşamba, Cumartesi
        'silivri': [1, 4],     # Pazartesi, Perşembe
        'buyukcekmece': [2, 5],# Salı, Cuma
        'kucukcekmece': [3, 6],# Çarşamba, Cumartesi
        'avcilar': [1, 4],     # Pazartesi, Perşembe
        'bakirkoy': [2, 5],    # Salı, Cuma
        'bahcelievler': [3, 6],# Çarşamba, Cumartesi
        'besiktas': [1, 4],    # Pazartesi, Perşembe
        'beyoglu': [2, 5],     # Salı, Cuma
        'fatih': [3, 6],       # Çarşamba, Cumartesi
        'bayrampasa': [1, 4],  # Pazartesi, Perşembe
        'eyup': [2, 5],        # Salı, Cuma
        'kagithane': [3, 6],   # Çarşamba, Cumartesi
        'sisli': [1, 4],       # Pazartesi, Perşembe
        'sariyer': [2, 5],     # Salı, Cuma
        'beykoz': [3, 6],      # Çarşamba, Cumartesi
        'umraniye': [1, 4],    # Pazartesi, Perşembe
        'uskudar': [2, 5],     # Salı, Cuma
        'kadikoy': [3, 6],     # Çarşamba, Cumartesi
        'atasehir': [1, 4],    # Pazartesi, Perşembe
        'umraniye': [2, 5],    # Salı, Cuma
        'maltepe': [3, 6],     # Çarşamba, Cumartesi
        'kartal': [1, 4],      # Pazartesi, Perşembe
        'pendik': [2, 5],      # Salı, Cuma
        'tuzla': [3, 6],       # Çarşamba, Cumartesi
        'sultanbeyli': [1, 4], # Pazartesi, Perşembe
        'sile': [2, 5],        # Salı, Cuma
        'catalca': [3, 6],     # Çarşamba, Cumartesi
        'silivri': [1, 4],     # Pazartesi, Perşembe
        'buyukcekmece': [2, 5],# Salı, Cuma
        'kucukcekmece': [3, 6],# Çarşamba, Cumartesi
        'avcilar': [1, 4],     # Pazartesi, Perşembe
        'bakirkoy': [2, 5],    # Salı, Cuma
        'bahcelievler': [3, 6],# Çarşamba, Cumartesi
        'besiktas': [1, 4],    # Pazartesi, Perşembe
        'beyoglu': [2, 5],     # Salı, Cuma
        'fatih': [3, 6],       # Çarşamba, Cumartesi
        'bayrampasa': [1, 4],  # Pazartesi, Perşembe
        'eyup': [2, 5],        # Salı, Cuma
        'kagithane': [3, 6],   # Çarşamba, Cumartesi
        'sisli': [1, 4],       # Pazartesi, Perşembe
        'sariyer': [2, 5],     # Salı, Cuma
        'beykoz': [3, 6],      # Çarşamba, Cumartesi
    }

    name = fields.Char(string='Teslimat No', required=True, copy=False, readonly=True, default=lambda self: _('Yeni'))
    siparis_turu = fields.Selection([
        ('sale', 'Satış Siparişi'),
        ('pos', 'POS Siparişi')
    ], string='Sipariş Türü', required=True, default='sale')
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
    adres = fields.Many2one('res.partner', string='Adres', tracking=True, domain="[('parent_id', '=', musteri)]")
    telefon = fields.Char(string='Telefon', tracking=True, readonly=True)
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
            self._check_delivery_limits(vals)
            if vals.get('name', _('Yeni')) == _('Yeni'):
                vals['name'] = self.env['ir.sequence'].next_by_code('teslimat.planlama') or _('Yeni')
        return super().create(vals_list)

    def write(self, vals):
        self._check_delivery_limits(vals)
        return super().write(vals)

    def _check_delivery_limits(self, vals):
        teslimat_tarihi = vals.get('teslimat_tarihi') or self.teslimat_tarihi
        ilce = vals.get('ilce') or self.ilce
        # 1. Gün ve ilçe için 7 sınırı (herkes için geçerli)
        if teslimat_tarihi and ilce:
            count = self.env['teslimat.planlama'].search_count([
                ('teslimat_tarihi', '=', teslimat_tarihi),
                ('ilce', '=', ilce)
            ])
            if count >= 7:
                raise UserError(_('Bu gün ve ilçe için en fazla 7 teslimat oluşturabilirsiniz.'))
        # 2. İlçe ve gün uygun değilse kimse teslimat oluşturamaz
        if teslimat_tarihi and ilce:
            gun = fields.Date.from_string(teslimat_tarihi).isoweekday()
            uygun_gunler = self.ILCE_TESLIMAT_GUNLERI.get(ilce, [])
            if gun not in uygun_gunler:
                raise UserError(_(f'{ilce.title()} ilçesi için {self._get_gun_adi(gun)} günü teslimat yapılamaz.'))

    @api.onchange('siparis_turu')
    def _onchange_siparis_turu(self):
        self.sale_order_id = False
        self.pos_order_id = False
        self.picking_id = False
        self.urun_ids = False

    @api.onchange('musteri')
    def _onchange_musteri(self):
        if self.musteri:
            self.telefon = self.musteri.phone
            self.ek_telefon = self.musteri.mobile
            # Adres alanını temizle
            self.adres = False

    @api.onchange('adres')
    def _onchange_adres(self):
        if self.adres:
            self.ilce = self.adres.state_id.name.lower()

    @api.onchange('picking_id')
    def _onchange_picking(self):
        if self.picking_id:
            # Ürünleri transfer belgesinden otomatik olarak ekle
            urunler = []
            for line in self.picking_id.move_lines:
                # Aynı ürünü tekrar eklememek için kontrol et
                if not any(u[2]['urun_adi'] == line.product_id.name for u in urunler):
                    urunler.append((0, 0, {
                        'urun_adi': line.product_id.name,
                        'miktar': line.product_uom_qty,
                        'birim': 'adet'
                    }))
            self.urun_ids = urunler

            # Partner ve adres bilgisi
            if self.picking_id.partner_id:
                self.musteri = self.picking_id.partner_id
                
                # Önce teslimat adresini bul
                delivery_address = self.picking_id.partner_id.child_ids.filtered(
                    lambda a: a.type == 'delivery' and a.street
                )
                
                if delivery_address:
                    # Teslimat adresi varsa onu kullan
                    self.adres = delivery_address[0].id
                    if delivery_address[0].state_id:
                        ilce = delivery_address[0].state_id.name.lower()
                        ilce = ilce.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
                        if ilce in dict(self._fields['ilce'].selection).keys():
                            self.ilce = ilce
                else:
                    # Teslimat adresi yoksa, partner'ın kendi adresini kullan
                    self.adres = self.picking_id.partner_id.id
                    if self.picking_id.partner_id.state_id:
                        ilce = self.picking_id.partner_id.state_id.name.lower()
                        ilce = ilce.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
                        if ilce in dict(self._fields['ilce'].selection).keys():
                            self.ilce = ilce

            # Telefon bilgilerini güncelle
            if self.musteri:
                self.telefon = self.musteri.phone
                self.ek_telefon = self.musteri.mobile

    @api.onchange('sale_order_id')
    def _onchange_sale_order(self):
        if self.sale_order_id:
            self.musteri = self.sale_order_id.partner_id
            self.picking_id = self.sale_order_id.picking_ids.filtered(lambda p: p.picking_type_code == 'outgoing')[:1]
            self._onchange_musteri()
            self._onchange_picking()

    @api.onchange('pos_order_id')
    def _onchange_pos_order(self):
        if self.pos_order_id:
            self.musteri = self.pos_order_id.partner_id
            self._onchange_musteri()

    @api.onchange('ilce', 'teslimat_tarihi')
    def _onchange_teslimat_tarihi(self):
        if self.ilce and self.teslimat_tarihi:
            gun = self.teslimat_tarihi.isoweekday()
            teslimat_gunleri = self.ILCE_TESLIMAT_GUNLERI.get(self.ilce, [])
            if gun not in teslimat_gunleri:
                self.teslimat_tarihi = False
                return {
                    'warning': {
                        'title': 'Geçersiz Teslimat Günü',
                        'message': f'{self.ilce.title()} ilçesi için teslimat günü {self._get_gun_adi(gun)} günü yapılamaz. Sadece {", ".join([self._get_gun_adi(g) for g in teslimat_gunleri])} günlerinden birini seçebilirsiniz.'
                    }
                }

    def _get_gun_adi(self, gun_no):
        gunler = {
            1: 'Pazartesi',
            2: 'Salı',
            3: 'Çarşamba',
            4: 'Perşembe',
            5: 'Cuma',
            6: 'Cumartesi',
            7: 'Pazar'
        }
        return gunler.get(gun_no, '')

    def action_tamamlandi(self):
        self.write({'durum': 'tamamlandi'})

    def action_iptal(self):
        self.write({'durum': 'iptal'})

    def action_yolda(self):
        self.write({'durum': 'yolda'})
        # SMS gönder
        self._send_delivery_sms()

    def _send_delivery_sms(self):
        """Teslimat durumu SMS'ini gönder"""
        if not self.musteri or not self.musteri.mobile:
            return False

        # SMS içeriğini hazırla
        message = f"""
        Sayın {self.musteri.name},
        Siparişiniz yola çıktı. Tahmini teslimat saatiniz: {self._get_estimated_delivery_time()}
        Teslimat No: {self.name}
        İyi günler dileriz.
        """
        
        try:
            # SMS API'si ile entegrasyon
            # Örnek: Twilio, Nexmo, Netgsm vb.
            # self.env['sms.api'].send_sms(self.musteri.mobile, message)
            
            # Şimdilik sadece log tutalım
            _logger.info(f"SMS gönderildi: {self.musteri.mobile} - {message}")
            
            # SMS gönderim kaydı
            self.message_post(
                body=f"SMS gönderildi: {message}",
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            return True
        except Exception as e:
            _logger.error(f"SMS gönderilemedi: {str(e)}")
            return False

    def _get_estimated_delivery_time(self):
        """Tahmini teslimat saatini hesapla"""
        if not self.teslimat_baslangic:
            return "Belirlenemedi"
            
        # Varsayılan teslimat süresi (dakika)
        default_duration = 30
        
        # Eğer teslimat süresi belirtilmişse onu kullan
        duration = self.teslimat_suresi or default_duration
        
        # Başlangıç zamanına süreyi ekle
        delivery_time = self.teslimat_baslangic + timedelta(minutes=duration)
        
        # Saati formatla
        return delivery_time.strftime("%H:%M")

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

    def action_haritada_ac(self):
        self.ensure_one()
        if not self.adres:
            raise UserError(_('Teslimat adresi bulunamadı.'))
            
        # Adres bilgilerini al
        street = self.adres.street or ''
        city = self.adres.city or ''
        state = self.adres.state_id.name or ''
        zip_code = self.adres.zip or ''
        
        # Adresi URL formatına dönüştür
        address = f"{street}, {city}, {state} {zip_code}"
        address = address.replace(' ', '+')
        
        # Android ve iOS için farklı URL'ler
        android_url = f"https://www.google.com/maps/dir/?api=1&destination={address}"
        ios_url = f"maps://maps.apple.com/?daddr={address}"
        
        # Kullanıcının cihaz tipini kontrol et (bu kısmı Odoo'nun mobil uygulaması ile entegre etmek gerekebilir)
        # Şimdilik her iki URL'yi de döndürelim
        return {
            'type': 'ir.actions.act_url',
            'url': android_url,  # Varsayılan olarak Android URL'sini kullan
            'target': 'new',
        }

    @api.constrains('adres')
    def _check_teslimat_gunu(self):
        for record in self:
            if record.adres and record.adres.city == 'İstanbul' and record.adres.state_id.name == 'Arnavutköy':
                izin_verilen_gunler = ['Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi']
                gun = fields.Date.from_string(record.teslimat_tarihi).isoweekday()
                gun_adi = self._get_gun_adi(gun)
                if gun_adi not in izin_verilen_gunler:
                    raise ValidationError(_('Arnavutköy ilçesi için teslimat günü %s günü yapılamaz. Sadece %s günlerinden birini seçebilirsiniz.') % 
                        (gun_adi, ', '.join(izin_verilen_gunler)))

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