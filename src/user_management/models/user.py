from odoo import fields, models



class Users(models.Model):
    _inherit = "res.users"


    passport = fields.Char(string="Passport")
    date_of_birth = fields.Date("Birthday")
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
    experience_year = fields.Float()
    work_place_ids = fields.Many2many("user.work.places")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])

    student_number = fields.Char()
    teacher_ids = fields.Many2many("user.teacher")

