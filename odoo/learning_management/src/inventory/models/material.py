from odoo import models, fields, api


class EduMaterials(models.Model):
    _name = 'inventory.edu.materials'
    _description = 'Education Materials'

    name = fields.Char()
    quantity = fields.Integer(string="Quantity", default=1)
    condition = fields.Selection([
        ('new', 'New'),
        ('used', 'Used'),
        ('broken', 'Broken'),
        ('expired', 'Expired')
    ], default='new')


    branch_id = fields.Many2one('res.company',required=True)
    responsible_id = fields.Many2one("res.users", string="Responsible Person")

    def action_material_broken(self):
        for record in self:
            record.condition = "broken"

    def action_material_expire(self):
        for record in self:
            record.condition = "expired"
