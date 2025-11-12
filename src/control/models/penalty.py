from odoo import models, fields, api


class Penalty(models.Model):
     _name = 'control.penalty'
     _description = 'Penalty'

     name = fields.Char(required=True, default="New")
     user_id = fields.Many2one("res.users")
     amount = fields.Float(required=True)
     reason = fields.Text(string="Reason", required=True)
     date = fields.Date(default=fields.Date.context_today)
     active = fields.Boolean(default=True)
     status = fields.Selection([
         ("draft", "Draft"),
         ("paid", "Paid"),
         ("cancelled", "Cancelled"),
     ], default="draft")

     def action_paid(self):
         for record in self:
             record.status = "paid"

     def action_cancel(self):
         for record in self:
             record.status = "cancelled"

     @api.model_create_multi
     def create(self, vals):
         if vals.get("name", "New") == "New":
             vals["name"] = self.env["ir.sequence"].next_by_code("control.penalty") or "New"
         return super(Penalty, self).create(vals)



