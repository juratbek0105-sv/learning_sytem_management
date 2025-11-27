from odoo import models, fields, api


class ScheduleStudentLesson(models.Model):
    _name = "edu.schedule.student.lesson"


    schedule_lesson_id = fields.Many2one('edu.schedule.lesson')
    student_id = fields.Many2one('user.student')
    payment_id = fields.Many2one('payment.edu.payment',string="Payment")
    price = fields.Float(related="schedule_lesson_id.group_id.course_id.price_per_lesson", string="Price of lesson")