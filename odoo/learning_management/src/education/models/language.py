from odoo import models, fields, api


class Language(models.Model):
    _name = 'edu.language'
    _description = 'Languages'


    user_id = fields.Many2one("res.users")






