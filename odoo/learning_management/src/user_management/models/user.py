from odoo import fields, models



class Users(models.Model):
    _inherit = "res.users"


    passport = fields.Char()
    language_ids = fields.Many2many("edu.language")
    date_of_birth = fields.Date()
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced')
    ], default="single")
    children_count = fields.Integer()

    user_type = fields.Selection([
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('operator', 'Operator (Reception)'),
        ('ceo', 'CEO'),
        ('branch_ceo', 'Branch CEO'),
        ('accountant', 'Accountant'),
        ('hr', 'HR'),
        ('other', 'Other'),
    ], string="User Type", default='other')
