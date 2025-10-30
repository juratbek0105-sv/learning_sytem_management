from odoo import models, fields, api


class Lesson(models.Model):
     _name = 'edu.lesson'
     _description = 'Lesson'

     name = fields.Char(string="Lesson", required=True)
     date = fields.Date(string="Lesson Date")
     duration = fields.Float(string="Duration (hours)")
     description = fields.Text(string="Lesson Description")
     is_demo = fields.Boolean(string="Demo Lesson")

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")
     task_ids = fields.One2many("edu.task", "lesson_id")
     subject_id = fields.Many2one("edu.subject")
     teacher_id = fields.Many2one("lms.teacher")





