from odoo import models, fields, api


class WorkPlaces(models.Model):
     _name = 'user.work.places'
     _description = 'Work Places'

     name = fields.Char(required=True)
     worked_years = fields.Float()
     user_id = fields.Many2one("res.users")





