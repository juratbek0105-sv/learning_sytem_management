from odoo import models, fields, api


class ControlWarning(models.Model):
     _name = 'control.warning'
     _description = 'Warning'

     employee_id = fields.Many2one("res.users", string="Employee", required=True)
     date = fields.Date(string="Warning Date", default=fields.Date.today)
     reason = fields.Text(string="Warning Reason", required=True)
     active = fields.Boolean(string="Active", default=True)




