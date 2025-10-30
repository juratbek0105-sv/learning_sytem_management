from odoo import models, fields, api


class Building(models.Model):
    _name = 'building.building'
    _description = 'Building'

    name = fields.Char()
    address = fields.Char()
    active = fields.Boolean(default=True)

    manager_id = fields.Many2one("res.users", string="Building Manager")
    room_ids = fields.One2many("building.room", "building_id")
    floor_ids = fields.One2many('building.floor', "building_id", string="Floor")
    branch_id = fields.Many2one("building.branch")
