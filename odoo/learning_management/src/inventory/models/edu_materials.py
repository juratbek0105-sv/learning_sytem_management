from odoo import models, fields, api


class EduMaterials(models.Model):
     _name = 'inventory.edu.materials'
     _description = 'Education Materials'

     name = fields.Char()
     condition = fields.Selection([
         ('new', 'New'),
         ('used', 'Used'),
         ('broken', 'Broken'),
         ('expired', 'Expired')
     ], default='new')
     branch_id = fields.Many2one("res.branch", string="Branch")




