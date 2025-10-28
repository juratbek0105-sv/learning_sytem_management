from odoo import models, fields, api

class Teacher(models.Model):
    _name = "lms.teacher"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    subjects = fields.Many2many("edu.subject")
