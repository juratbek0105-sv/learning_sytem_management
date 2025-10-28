from odoo import models, fields, api


class Lesson(models.Model):
     _name = 'edu.lesson'
     _description = 'Lesson'

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")
     task_ids = fields.One2many("edu.task", "lesson_id")



