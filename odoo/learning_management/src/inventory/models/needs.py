from odoo import models, fields, api


class Needs(models.Model):
     _name = 'inventory.needs'
     _description = 'Needs'

     name = fields.Char()
     requester_id = fields.Many2one("res.users", string="Requested By", required=True)
     request_date = fields.Date(string="Request Date", default=fields.Date.today)
     quantity = fields.Integer(string="Quantity", default=1)





