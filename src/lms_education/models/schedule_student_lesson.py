from odoo import models, fields, api


class ScheduleStudentLesson(models.Model):
    _name = "edu.schedule.student.lesson"

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    schedule_lesson_id = fields.Many2one('edu.schedule.lesson')
    student_id = fields.Many2one('res.users', domain=[("user_type", "=", "teacher")])
    group_id = fields.Many2one('edu.group', related="schedule_lesson_id.group_id")


    @api.depends('student_id', 'schedule_lesson_id')
    def _compute_name(self):
        for rec in self:
            student = rec.student_id.name or "No Student"
            lesson = rec.schedule_lesson_id.name or "No Lesson"
            rec.name = f"{student} - {lesson}"