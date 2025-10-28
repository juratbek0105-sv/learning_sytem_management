from odoo import models, fields, api

class Users(models.Model):
    _inherit = "res.users"

    experience_year = fields.Float()
    work_place_ids = fields.Many2many("control.work.places")
    passport = fields.Char()
    language_ids = fields.Many2many("edu.language")
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
    subjects = fields.Many2many("edu.subject")
