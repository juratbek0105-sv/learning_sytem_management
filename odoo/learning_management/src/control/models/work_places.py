from odoo import models, fields, api


class WorkPlaces(models.Model):
     _name = 'control.work.places'
     _description = 'Work Places'

     user_id = fields.Many2one("res.users")





