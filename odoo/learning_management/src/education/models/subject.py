from odoo import models, fields, api


class Subject(models.Model):
    _name = 'edu.subject'
    _description = 'Subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Subject Name", required=True, tracking=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True, tracking=True)

    teacher_ids = fields.Many2many("user.teacher")
    course_ids = fields.Many2many("edu.course", string="Courses")


    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Subject code must be unique!'),
    ]

    def action_toggle_subject(self):
        for record in self:
            record.active = not record.active

