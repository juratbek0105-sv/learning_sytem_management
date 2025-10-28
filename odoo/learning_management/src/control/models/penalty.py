from odoo import models, fields, api


class Penalty(models.Model):
     _name = 'control.penalty'
     _description = 'Penalty'

     user_id = fields.Many2one("res.users")
     reason = fields.Char()
     amount = fields.Float()
     active = fields.Boolean(default=True)



