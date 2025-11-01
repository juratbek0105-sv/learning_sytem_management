from odoo import models, fields, api


class Assignment(models.Model):
    _name = 'edu.assignment'
    _description = 'Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Assignment", required=True)
    description = fields.Text(string="Task Description")
    deadline = fields.Datetime(string="Deadline")
    max_score = fields.Float(default=100)
    pass_score = fields.Float()
    exam_date = fields.Datetime(string="Exam Date", required=True, tracking=True)
    duration = fields.Float()(required=True, tracking=True)
    exam_type = fields.Selection([
        ('written', 'Written'),
        ('oral', 'Oral'),
        ('practical', 'Practical'),
        ('online', 'Online'),
    ], default='written', tracking=True)

    course_id = fields.Many2one("edu.course", tracking=True)
    group_id = fields.Many2one("edu.group", tracking=True)
    subject_id = fields.Many2one("edu.subject", string="Subject", required=True, tracking=True)
    student_ids = fields.Many2many("lms.student", string="Assigned Students", tracking=True)

    result_ids = fields.One2many("edu.performance", "assignment_id")

