from odoo import models, fields, api


class Performance(models.Model):
    _name = 'edu.performance'
    _description = 'Performance'

    student_id = fields.Many2one("lms.student", string="Student", required=True)
    course_id = fields.Many2one("edu.course", string="Course", required=True)
