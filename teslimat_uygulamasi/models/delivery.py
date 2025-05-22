from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import qrcode
import base64
from io import BytesIO

class DeliveryPlan(models.Model):
    _name = 'delivery.plan'
    _description = 'Teslimat Planı'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Teslimat Referansı', required=True, copy=False, 
                      readonly=True, default=lambda self: _('New'))
    date = fields.Date(string='Teslimat Tarihi', required=True, tracking=True)
    region = fields.Selection([
        ('anadolu', 'Anadolu Yakası'),
        ('avrupa', 'Avrupa Yakası')
    ], string='Bölge', required=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Taslak'),
        ('confirmed', 'Onaylandı'),
        ('in_progress', 'Teslimatta'),
        ('done', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi')
    ], string='Durum', default='draft', tracking=True)
    
    max_deliveries = fields.Integer(string='Maksimum Teslimat Sayısı', default=7,
                                  help='Günlük maksimum teslimat sayısı')
    
    sale_order_ids = fields.Many2many('sale.order', string='Satış Siparişleri',
                                    domain="[('state', 'in', ['sale', 'done']), "
                                          "('picking_ids.state', '=', 'assigned')]")
    
    delivery_line_ids = fields.One2many('delivery.plan.line', 'delivery_plan_id', 
                                      string='Teslimat Satırları')
    
    notes = fields.Text(string='Notlar')
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('delivery.plan') or _('New')
        return super().create(vals_list)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
        # SMS ve Email bildirimi gönder
        self._send_notifications('confirmed')
    
    def action_start_delivery(self):
        self.write({'state': 'in_progress'})
        # SMS ve Email bildirimi gönder
        self._send_notifications('in_progress')
    
    def action_done(self):
        self.write({'state': 'done'})
        # SMS ve Email bildirimi gönder
        self._send_notifications('done')
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
        # SMS ve Email bildirimi gönder
        self._send_notifications('cancelled')
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def _send_notifications(self, state):
        for line in self.delivery_line_ids:
            partner = line.partner_id
            if partner.email:
                template = self.env.ref('teslimat_uygulamasi.email_template_delivery_status')
                template.with_context(status=state).send_mail(line.id, force_send=True)
            if partner.mobile:
                self.env['sms.sms'].create({
                    'partner_id': partner.id,
                    'number': partner.mobile,
                    'body': self._get_sms_body(state, line)
                })

    def _get_sms_body(self, state, line):
        status_text = {
            'confirmed': 'Teslimatınız onaylandı',
            'in_progress': 'Teslimatınız yolda',
            'done': 'Teslimatınız tamamlandı',
            'cancelled': 'Teslimatınız iptal edildi'
        }
        return f"{status_text.get(state, '')} - Sipariş No: {line.sale_order_id.name}"

class DeliveryPlanLine(models.Model):
    _name = 'delivery.plan.line'
    _description = 'Teslimat Planı Satırı'

    delivery_plan_id = fields.Many2one('delivery.plan', string='Teslimat Planı', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Satış Siparişi', required=True)
    partner_id = fields.Many2one('res.partner', string='Müşteri', related='sale_order_id.partner_id')
    picking_id = fields.Many2one('stock.picking', string='Transfer', 
                                domain="[('sale_id', '=', sale_order_id)]")
    
    delivery_status = fields.Selection([
        ('loaded', 'Yüklendi'),
        ('on_way', 'Yolda'),
        ('completed', 'Tamamlandı')
    ], string='Teslimat Durumu', default='loaded', tracking=True)
    
    estimated_delivery_time = fields.Datetime(string='Tahmini Teslimat Zamanı')
    actual_delivery_time = fields.Datetime(string='Gerçekleşen Teslimat Zamanı')
    
    qr_code = fields.Binary(string='QR Kod', compute='_generate_qr_code')
    qr_code_string = fields.Char(string='QR Kod Metni', compute='_generate_qr_code')
    
    state = fields.Selection(related='delivery_plan_id.state', string='Durum')
    notes = fields.Text(string='Notlar')
    
    @api.depends('sale_order_id', 'delivery_plan_id')
    def _generate_qr_code(self):
        for record in self:
            qr_string = f"DELIVERY:{record.delivery_plan_id.name}:{record.sale_order_id.name}"
            record.qr_code_string = qr_string
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_string)
            qr.make(fit=True)
            
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            record.qr_code = qr_image
    
    def action_update_status(self, new_status):
        self.write({'delivery_status': new_status})
        if new_status == 'completed':
            self.write({'actual_delivery_time': fields.Datetime.now()})
            # SMS ve Email bildirimi gönder
            self.delivery_plan_id._send_notifications('done') 