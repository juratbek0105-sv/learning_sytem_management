from odoo import models, fields, api


class Task(models.Model):
     _name = 'edu.task'
     _description = 'Task'

     course_id = fields.Many2one("edu.course")
     lesson_id = fields.Many2one("edu.lesson")



