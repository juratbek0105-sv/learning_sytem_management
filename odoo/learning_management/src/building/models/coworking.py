from odoo import models, fields, api


class Coworking(models.Model):
    _name = 'building.coworking'
    _description = 'Coworking'

    name = fields.Char(string="Coworking Name", required=True)
    building_id = fields.Many2one("build.building", required=True)
    capacity = fields.Integer(string="Capacity")
