from odoo import models, fields, api


class Lesson(models.Model):
     _name = 'edu.lesson'
     _description = 'Lesson'

     name = fields.Char(string="Name", required=True)
     date = fields.Date(string="Date")
     duration = fields.Float(string="Duration")
     duration_uom = fields.Many2one("uom.uom", required=True, domain=[("category_id.name", "=", "Time")])
     description = fields.Text(string="Description")
     is_demo = fields.Boolean(string="Is Demo")

     course_id = fields.Many2one("edu.course")
     group_id = fields.Many2one("edu.group")
     task_ids = fields.One2many("edu.task", "lesson_id")
     teacher_id = fields.Many2one("user.teacher")

     schedule_lesson_ids = fields.One2many(
         "edu.schedule.lesson",
         "lesson_id",
         string="Scheduled Lessons",
     )









