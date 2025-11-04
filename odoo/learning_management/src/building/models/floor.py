from odoo import models, fields, api


class Floor(models.Model):
     _name = 'building.floor'
     _description = 'Floor'

     number = fields.Integer(string="Floor Number")
     active = fields.Boolean(default=True)

     building_id = fields.Many2one("building.building")
     room_ids = fields.One2many("building.room", "floor_id")
     total_rooms = fields.Integer(compute="_compute_total_rooms",store=True,)

     @api.depends("room_ids")
     def _compute_total_rooms(self):
         for record in self:
             record.total_rooms = len(record.room_ids)

     def action_toggle_floor(self):
         for record in self:
             record.active = not record.active

