from datetime import date
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ScheduleStudentLesson(models.Model):
    _inherit = "edu.schedule.student.lesson"

    payment_id = fields.Many2one('payment.edu.payment')
    price = fields.Float(string="Price", compute="_compute_price", store=True)
    teacher_salary_paid = fields.Boolean(default=False)

    # ---------------------------------------------
    # PRICE COMPUTE
    # ---------------------------------------------
    @api.depends(
        'schedule_lesson_id.schedule_table_id.payment_for_lesson',
        'schedule_lesson_id.schedule_table_id.per_lesson',
        'schedule_lesson_id.schedule_table_id.per_month'
    )
    def _compute_price(self):
        for record in self:
            schedule = record.schedule_lesson_id
            table = schedule.schedule_table_id if schedule else None

            if not table:
                record.price = 0
                continue

            if table.payment_for_lesson == 'per_lesson':
                record.price = table.per_lesson or 0
            elif table.payment_for_lesson == 'per_month':
                record.price = table.per_month or 0
            else:
                record.price = 0

    # ---------------------------------------------
    # CRON: PER LESSON AUTO PAYMENT FROM STUDENT
    # ---------------------------------------------
    @api.model
    def cron_auto_withdraw_lesson(self):
        today = date.today()

        lessons = self.search([
            ('schedule_lesson_id.date', '<=', today),
            ('payment_id', '=', False),
            ('schedule_lesson_id.schedule_table_id.payment_for_lesson', '=', 'per_lesson')
        ])

        _logger.info(f"[PER LESSON CRON] {len(lessons)} lessons need auto-payment.")

        for lesson in lessons:
            lesson._compute_price()

            if lesson.price <= 0:
                continue

            student = lesson.student_id
            if not student:
                continue

            payment = self.env['payment.edu.payment'].create({
                'user_id': self.env.user.id,
                'student_id': student.id,
                'amount': lesson.price,
                'payment_type': 'online',
                'detailed_type': 'lesson_payment',
                'status': 'paid',
                'schedule_student_lesson_id': lesson.id,
                'note': f"Auto payment for lesson {lesson.schedule_lesson_id.name}",
            })

            lesson.payment_id = payment.id
            _logger.info(f"[PER LESSON] Payment created for {student.name} → {lesson.price}")

    # ---------------------------------------------
    # CRON: PER MONTH AUTO PAYMENT FROM STUDENT
    # ---------------------------------------------
    @api.model
    def cron_withdraw_per_month(self):
        today = date.today()
        if today.day != 5:
            return

        tables = self.env['edu.schedule.table'].search([
            ('payment_for_lesson', '=', 'per_month')
        ])

        _logger.info(f"[MONTHLY CRON] Found {len(tables)} monthly payment tables.")

        for table in tables:

            if table.per_month <= 0:
                continue

            for student in table.group_id.student_ids:

                self.env['payment.edu.payment'].create({
                    'user_id': self.env.user.id,
                    'student_id': student.id,
                    'amount': table.per_month,
                    'payment_type': 'online',
                    'detailed_type': 'lesson_payment',
                    'status': 'paid',
                    'note': f"Monthly auto-withdraw for {table.group_id.name}",
                })

                _logger.info(f"[MONTHLY] {student.name} charged {table.per_month}")
