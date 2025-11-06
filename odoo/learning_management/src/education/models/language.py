from odoo import models, fields, api


class Language(models.Model):
    _name = 'edu.language'
    _description = 'Languages'

    name = fields.Char(string="Name")
    user_id = fields.Many2one("res.users")






