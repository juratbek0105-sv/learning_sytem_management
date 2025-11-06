from odoo import models, fields

class EduWeekday(models.Model):
    _name = 'edu.weekday'
    _description = 'Weekday'

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Day Order", required=True)  # Monday=1 ... Sunday=7
