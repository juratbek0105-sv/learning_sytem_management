from odoo import models, fields, api


class Course(models.Model):
    _name = 'edu.course'
    _description = 'Course'

    name = fields.Char(string="Course Name", required=True)
    duration = fields.Float(required=True)
    group_ids = fields.One2many("edu.group", "course_id")
    assignment_ids = fields.One2many("edu.assignment", "course_id")
    lesson_ids = fields.One2many("edu.lesson", "course_id")
    task_ids = fields.One2many("edu.task", "course_id")
