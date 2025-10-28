from odoo import models, fields, api



class HR(models.Model):
    _name = "lms.hr"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")

