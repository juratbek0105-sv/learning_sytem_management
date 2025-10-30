from odoo import models, fields, api


class Task(models.Model):
     _name = 'edu.task'
     _description = 'Task'


     name = fields.Char(string="Assignment", required=True)
     description = fields.Text(string="Task Description")
     deadline = fields.Datetime(string="Deadline")

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")
     lesson_id = fields.Many2one("edu.lesson")
     student_ids = fields.Many2many("lms.student", string="Assigned Students")




