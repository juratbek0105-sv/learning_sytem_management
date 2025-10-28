from odoo import models, fields, api


class Floor(models.Model):
     _name = 'building.floor'
     _description = 'Floor'

     building_id = fields.Many2one("building.building")
     room_ids = fields.One2many("building.room", "floor_id")
     branch_id = fields.Many2one("building.branch")




