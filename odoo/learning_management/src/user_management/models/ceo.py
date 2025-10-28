from odoo import models, fields, api



class Student(models.Model):
    _name = "lms.ceo"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")

