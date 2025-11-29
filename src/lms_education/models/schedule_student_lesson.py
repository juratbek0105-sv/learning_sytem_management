from odoo import models, fields, api


class ScheduleStudentLesson(models.Model):
    _name = "edu.schedule.student.lesson"


    schedule_lesson_id = fields.Many2one('edu.schedule.lesson')
    student_id = fields.Many2one('res.users')
