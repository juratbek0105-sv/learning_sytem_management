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
     branch_id = fields.Many2one("building.branch")



