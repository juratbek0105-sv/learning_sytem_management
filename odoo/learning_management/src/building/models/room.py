from odoo import models, fields, api


class Room(models.Model):
    _name = 'building.room'
    _description = 'Room'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    capacity = fields.Integer(string="Capacity")

    floor_id = fields.Many2one('building.floor', string="Floor")
    building_id = fields.Many2one("building.building")
    is_under_repair = fields.Boolean(default=False)

    room_type = fields.Selection([
        ("classroom", "Classroom"),
        ("meeting", "Meeting Room"),
        ("office", "Office"),
        ("lab", "Lab"),
    ], string="Room Type")
    status = fields.Selection([
        ("available", "Available"),
        ("occupied", "Occupied"),
        ("repair", "Under Repair"),
    ], string="Status", default="available")

    def action_toggle_room(self):
        for record in self:
            record.active = not record.active
