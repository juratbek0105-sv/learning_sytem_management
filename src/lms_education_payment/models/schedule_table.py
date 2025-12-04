from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class EduScheduleTable(models.Model):
    _inherit = 'edu.schedule.table'

    payment_for_lesson = fields.Selection([
        ('per_lesson', 'Per lesson'),
        ('per_month', 'Per month'),
    ], default='per_lesson', required=True)

    per_lesson = fields.Monetary(currency_field='currency_id')
    per_month = fields.Monetary(currency_field='currency_id')

    teacher_portion_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], default='percentage', required=True)

    teacher_portion_fixed = fields.Monetary(currency_field='currency_id')
    teacher_portion_percentage = fields.Float()

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    teacher_salary_amount = fields.Monetary(
        currency_field='currency_id',
        compute='_compute_teacher_salary',
        store=True
    )

    @api.depends('payment_for_lesson', 'per_month', 'teacher_portion_type',
                 'teacher_portion_fixed', 'teacher_portion_percentage')
    def _compute_teacher_salary(self):
        for table in self:
            if table.payment_for_lesson != "per_month":
                table.teacher_salary_amount = 0
                continue

            if table.teacher_portion_type == 'fixed':
                table.teacher_salary_amount = table.teacher_portion_fixed
            else:
                table.teacher_salary_amount = (table.per_month * table.teacher_portion_percentage / 100)


    def cron_pay_teacher_salary_monthly(self):
        today = date.today()
        if today.day != 5:
            return

        monthly_tables = self.search([('payment_for_lesson', '=', 'per_month')])
        for table in monthly_tables:
            group = table.group_id
            teacher = group.teacher_id

            if not teacher or table.teacher_salary_amount <= 0:
                continue

            payment = self.env["payment.edu.payment"].create({
                'user_id': self.env.user.id,
                'teacher_id': teacher.id,
                'amount': table.teacher_salary_amount,
                'payment_type': 'online',
                'detailed_type': 'teacher_salary',
                'status': 'paid',
                'note': f"Monthly teacher salary for {table.group_id.name}",
                'name': f"Teacher salary {teacher.name} ({table.group_id.name})",
            })

            _logger.info(f"Paid {payment.amount} to teacher {teacher.name}")


    def cron_pay_teacher_salary_per_lesson(self):
        today = date.today()
        lessons = self.env["edu.schedule.student.lesson"].search([
            ('schedule_lesson_id.schedule_table_id.payment_for_lesson', '=', 'per_lesson'),
            ('schedule_lesson_id.date', '<=', today),
            ('teacher_salary_paid', '=', False)
        ])

        for lesson in lessons:
            table = lesson.schedule_lesson_id.schedule_table_id
            group = table.group_id
            teacher = group.teacher_id

            if not teacher:
                continue

            # compute salary
            if table.teacher_portion_type == 'fixed':
                salary_amount = table.teacher_portion_fixed
            else:
                lesson._compute_price()
                salary_amount = (lesson.price * table.teacher_portion_percentage / 100)

            if salary_amount <= 0:
                continue

            self.env["payment.edu.payment"].create({
                'user_id': self.env.user.id,
                'teacher_id': teacher.id,
                'amount': salary_amount,
                'payment_type': 'online',
                'detailed_type': 'teacher_salary',
                'status': 'paid',
                'note': f"Salary per lesson for {group.name}",
            })

            lesson.teacher_salary_paid = True
