from odoo import models, fields, api


class Coworking(models.Model):
    _name = 'building.coworking'
    _description = 'Coworking'

    name = fields.Char(string="Name", required=True)
    building_id = fields.Many2one("building.building", required=True)
    capacity = fields.Integer(string="Capacity")
    active = fields.Boolean(string="Active", default=True)

    def action_toggle_active(self):
        for record in self:
            record.active = not record.active