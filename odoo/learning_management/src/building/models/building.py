from odoo import models, fields, api


class Building(models.Model):
    _name = 'building.building'
    _description = 'Building'

    name = fields.Char(reqired=True)
    address = fields.Char()
    active = fields.Boolean(default=True)

    manager_id = fields.Many2one("res.users", string="Building Manager")
    room_ids = fields.One2many("building.room", "building_id")
    floor_ids = fields.One2many('building.floor', "building_id", string="Floor")
    company_id = fields.Many2one('res.company',required=True)

    def action_toggle_building(self):
        for record in self:
            record.active = not record.active
