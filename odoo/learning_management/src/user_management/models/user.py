from odoo import fields, models



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
