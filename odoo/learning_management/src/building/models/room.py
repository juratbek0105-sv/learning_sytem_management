from odoo import models, fields, api


class Room(models.Model):
     _name = 'building.room'
     _description = 'Room'

     name = fields.Char()
     active = fields.Boolean()

     floor_id = fields.Many2one('building.floor', string="Floor")
     building_id = fields.Many2one("building.building")
     is_under_repair = fields.Boolean(default=False)



