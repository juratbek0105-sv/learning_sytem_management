from odoo import models, fields, api

class Users(models.Model):
    _inherit = "res.users"

    experience_year = fields.Float()
    work_places = fields.Char()
    passport_id = fields.Many2one()
    languages = fields.Many2many()
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced')
    ])
    children_count = fields.Integer()


class Teacher(models.Model):
    _name = "lms.teacher"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    subjects = fields.Many2many()
