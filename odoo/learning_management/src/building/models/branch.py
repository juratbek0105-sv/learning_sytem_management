from odoo import models, fields


class Branch(models.Model):
    _inherit = 'res.branch'

    ceo_id = fields.Many2one('res.users')
