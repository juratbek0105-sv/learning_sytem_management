from datetime import date, datetime
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ScheduleStudentLesson(models.Model):
    _inherit = "edu.schedule.student.lesson"

    payment_id = fields.Many2one('payment.edu.payment', default=False)
    price = fields.Float(string="Price", compute="_compute_price", store=True)

    @api.depends('schedule_lesson_id.schedule_table_id.payment_for_lesson',
                 'schedule_lesson_id.schedule_table_id.per_lesson',
                 'schedule_lesson_id.schedule_table_id.per_month')
    def _compute_price(self):
        for record in self:
            # Add safety checks
            if not record.schedule_lesson_id or not record.schedule_lesson_id.schedule_table_id:
                record.price = 0.0
                continue

            schedule_table_id = record.schedule_lesson_id.schedule_table_id
            option = schedule_table_id.payment_for_lesson

            if option == 'per_lesson':
                record.price = schedule_table_id.per_lesson or 0.0
            elif option == 'per_month':
                record.price = schedule_table_id.per_month or 0.0
            else:
                record.price = 0.0

    @api.model
    def cron_auto_withdraw_lesson(self):
        today = date.today()
        today_str = today.strftime('%Y-%m-%d')

        lessons = self.search([
            ('schedule_lesson_id.date', '<=', today_str),
            ('payment_id', '=', False),
            ('schedule_lesson_id.schedule_table_id.payment_for_lesson', '=', 'per_lesson')
        ])

        _logger.info(f"Found {len(lessons)} lessons to process for date <= {today_str}")

        for lesson in lessons:
            # Force recompute price to ensure it's up to date
            lesson._compute_price()

            lesson_date = lesson.schedule_lesson_id.date
            lesson_price = lesson.price

            # Skip if price is 0 or not set
            if not lesson_price or lesson_price <= 0:
                _logger.warning(
                    f"⚠️ Skipping lesson {lesson.schedule_lesson_id.name} - price is {lesson_price}"
                )
                continue

            _logger.info(
                f"Processing lesson: {lesson.schedule_lesson_id.name}, Date: {lesson_date}, Price: {lesson_price}")

            student = lesson.student_id

            if not student:
                _logger.error(f"❌ No student found for lesson {lesson.schedule_lesson_id.name}")
                continue

            # Always create payment, even if balance is insufficient
            payment = self.env['payment.edu.payment'].create({
                'user_id': self.env.user.id,
                'student_id': student.id,
                'amount': lesson_price,
                'payment_type': 'online',
                'detailed_type': 'lesson_payment',
                'status': 'paid',
                'schedule_student_lesson_id': lesson.id,
                'note': f"Auto payment for lesson {lesson.schedule_lesson_id.name} on {lesson_date}"
            })
            lesson.payment_id = payment.id

            # Log based on balance status
            if student.balance >= lesson_price:
                _logger.info(
                    f"✔ Auto payment of {lesson_price} made for student {student.name} for lesson {lesson.schedule_lesson_id.name} (Date: {lesson_date}). "
                    f"Previous balance: {student.balance + lesson_price}, New balance: {student.balance}")
            else:
                new_balance = student.balance - lesson_price
                _logger.info(
                    f"⚠️ Payment of {lesson_price} created for student {student.name} with insufficient balance. "
                    f"Lesson: {lesson.schedule_lesson_id.name} (Date: {lesson_date}). "
                    f"Previous balance: {student.balance}, New balance: {new_balance} (NEGATIVE)")

    @api.model
    def cron_withdraw_per_month(self):
        today = date.today()
        target_day = today.replace(day=5)

        if today != target_day:
            _logger.info(f"Skipping monthly withdraw - today is {today}, waiting for day 5")
            return

        _logger.info(f"Running monthly withdraw on {today}")

        tables = self.env['edu.schedule.table'].search([
            ('payment_for_lesson', '=', 'per_month'),
        ])

        _logger.info(f"Found {len(tables)} schedule tables with monthly payment")

        for table in tables:
            price = table.per_month

            # Skip if price is not set
            if not price or price <= 0:
                _logger.warning(f"⚠️ Skipping table {table.name} - price is {price}")
                continue

            for student in table.group_id.student_ids:
                # Always create payment, even if balance is insufficient
                payment = self.env['payment.edu.payment'].create({
                    'user_id': self.env.user.id,
                    'student_id': student.id,
                    'amount': price,
                    'payment_type': 'online',
                    'detailed_type': 'lesson_payment',
                    'status': 'paid',
                    'note': f"Monthly auto-withdraw for group {table.group_id.name} - {today.strftime('%B %Y')}"
                })

                # Log based on balance status
                if student.balance >= price:
                    _logger.info(
                        f"✔ Monthly withdraw: {student.name} / {price} / Group: {table.group_id.name}. "
                        f"Previous balance: {student.balance + price}, New balance: {student.balance}")
                else:
                    new_balance = student.balance - price
                    _logger.info(
                        f"⚠️ Monthly payment of {price} created for {student.name} with insufficient balance. "
                        f"Group: {table.group_id.name}. "
                        f"Previous balance: {student.balance}, New balance: {new_balance} (NEGATIVE)")
