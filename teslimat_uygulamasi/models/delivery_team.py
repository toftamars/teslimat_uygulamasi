from odoo import models, fields, api, _

class DeliveryTeam(models.Model):
    _name = 'delivery.team'
    _description = 'Teslimat Ekibi'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Ekip Adı', required=True, tracking=True)
    code = fields.Char(string='Kod', tracking=True)
    active = fields.Boolean(string='Aktif', default=True, tracking=True)
    user_ids = fields.Many2many('res.users', string='Ekip Üyeleri', tracking=True)
    notes = fields.Text(string='Notlar', tracking=True) 