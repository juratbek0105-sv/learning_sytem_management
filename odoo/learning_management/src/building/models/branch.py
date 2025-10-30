from odoo import models, fields, api


class Branch(models.Model):
     _name = 'building.branch'
     _description = 'Branch'

     name = fields.Char()
     address = fields.Char()
     active = fields.Boolean(default=True)


     building_id = fields.Many2one("building.building", "branch_id")
     room_ids = fields.One2many("building.room", "branch_id")
     ceo_id = fields.Many2one("lms.ceo")
     branch_ceo_ids = fields.One2many("lms.branch.ceo", "branch_ceo_id")







