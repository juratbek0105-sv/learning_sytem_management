from odoo import models, fields, api


class Device(models.Model):
     _name = 'inventory.device'
     _description = 'Device'

     name = fields.Char()
     status = fields.Selection([
         ("working", "Working"),
         ("repair", "Under Repair"),
         ("broken", "Broken"),
         ("moved", "Moved to Another Branch"),
     ], default="working")
     purchase_date = fields.Date(string="Purchase Date")
     purchase_cost = fields.Float(string="Purchase Cost")

     branch_id = fields.Many2one('res.company', required=True)

     def action_send_to_repair(self):
         for record in self:
             record.condition = 'repair'

     def action_mark_broken(self):
         for record in self:
             record.condition = 'broken'

     def action_mark_moved(self):
         for record in self:
             record.condition = 'moved'



