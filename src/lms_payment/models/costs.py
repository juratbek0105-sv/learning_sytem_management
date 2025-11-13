from odoo import models, fields, api


class Costs(models.Model):
     _name = 'payment.costs'
     _description = 'Costs '

     name = fields.Char(string="Expense Title", required=True)
     date = fields.Date(string="Date", default=fields.Date.today)
     amount = fields.Float(string="Amount", required=True)
     responsible_id = fields.Many2one("res.users", string="Responsible")
     active = fields.Boolean(string="Active", default=True)


     status = fields.Selection([
         ("draft", "Draft"),
         ("approved", "Approved"),
         ("paid", "Paid"),
     ], string="Status", default="draft")


     def action_toggle_active(self):
         for record in self:
             record.active = not record.active

     def action_approve(self):
         for record in self:
             record.status = "approved"

     def action_paid(self):
         for record in self:
             record.status = "paid"
