from odoo import models, fields, api


class Assignment(models.Model):
    _name = 'edu.assignment'
    _description = 'Assignment'

    name = fields.Char(string="Assignment", required=True)
    description = fields.Text(string="Task Description")
    deadline = fields.Datetime(string="Deadline")
    max_score = fields.Float(default=100)
    pass_score = fields.Float()

    course_id = fields.Many2one("edu.course")
    group_id = fields.Many2one("edu.group")
    student_ids = fields.Many2many("lms.student", string="Assigned Students")

    result_ids = fields.One2many("edu.performance", "assignment_id")

