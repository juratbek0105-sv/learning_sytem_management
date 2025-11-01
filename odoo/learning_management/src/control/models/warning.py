from odoo import models, fields, api


class ControlWarning(models.Model):
     _name = 'control.warning'
     _description = 'Warning'

     name = fields.Char(required=True)
     employee_id = fields.Many2one("res.users", string="Employee", required=True)
     date = fields.Date(string="Warning Date", default=fields.Date.today)
     reason = fields.Text(string="Warning Reason", required=True)
     active = fields.Boolean(string="Active", default=True)
     status = fields.Selection([
         ("draft", "Draft"),
         ("reviewed", "Reviewed"),
         ("cancelled", "Cancelled"),
         ],default="draft",required=True,)

     def action_review(self):
         for record in self:
             record.status = "reviewed"

     def action_cancel(self):
         for record in self:
             record.status = "cancelled"


