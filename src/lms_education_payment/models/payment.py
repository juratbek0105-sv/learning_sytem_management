from odoo import models, fields


class Payment(models.Model):
    _inherit = 'payment.edu.payment'

    course_id = fields.Many2one("edu.course", string="Course", ondelete="set null")
    detailed_type = fields.Selection(selection_add=[
        ("lesson_payment", "Lesson Payment"),
    ], ondelete={"lesson_payment": "cascade"}, required=True, string='Payment Category')
    schedule_student_lesson_id = fields.Many2one("edu.schedule.student.lesson", string="ScheduleStudentLesson")