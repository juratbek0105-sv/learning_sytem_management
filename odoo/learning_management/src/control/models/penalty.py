from odoo import models, fields, api


class Penalty(models.Model):
     _name = 'control.penalty'
     _description = 'Penalty'

     user_id = fields.Many2one("res.users")
     amount = fields.Float(required=True)
     reason = fields.Text(string="Reason", required=True)
     active = fields.Boolean(default=True)
     status = fields.Selection([
         ("draft", "Draft"),
         ("paid", "Paid"),
         ("cancelled", "Cancelled"),
     ], default="draft")



