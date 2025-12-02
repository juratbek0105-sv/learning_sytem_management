from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class Group(models.Model):
    _inherit = "edu.group"

    balance = fields.Float(string="Group Balance", compute="_compute_balance")
    teacher_portion_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], string='Portion Type', default='percentage', required=True)

    teacher_portion_fixed = fields.Monetary(string='Teacher Portion in amount', currency_field='currency_id')
    teacher_portion_percentage = fields.Float(string='Teacher Portion in %')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    total_paid_students_amount = fields.Monetary(currency_field='currency_id',
                                                 compute='_compute_total_paid_students_amount')
    teacher_salary_amount = fields.Monetary(string="Teacher Salary", currency_field='currency_id',
                                            compute='_compute_teacher_salary', store=True)

    def _compute_total_paid_students_amount(self):
        for record in self:
            lesson_payments = self.env["payment.edu.payment"].search([
                ('detailed_type', '=', 'lesson_payment'),
                ('schedule_student_lesson_id.group_id', '=', record.id),
                ('status', '=', 'paid')
            ])
            record.total_paid_students_amount = sum(lesson_payments.mapped('amount'))

    @api.depends('teacher_portion_type', 'total_paid_students_amount', 'teacher_portion_fixed',
                 'teacher_portion_percentage')
    def _compute_teacher_salary(self):
        for record in self:
            if record.teacher_portion_type == 'fixed':
                record.teacher_salary_amount = record.teacher_portion_fixed
            else:
                record.teacher_salary_amount = (record.total_paid_students_amount * record.teacher_portion_percentage) / 100

    @api.depends('teacher_portion_type')
    def _compute_balance(self):
        for record in self:
            record.balance = record.total_paid_students_amount - record.teacher_salary_amount

    def action_view_balance(self):
        self.ensure_one()
        return {
            'name': f'Balance Details for {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'payment.edu.payment',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('schedule_student_lesson_id.group_id', '=', self.id)],
            'context': {'default_detailed_type': 'lesson_payment'}
        }

    def cron_pay_teacher_salary_monthly(self):
        today = date.today()
        target_day = 5
        if today.day != target_day:
            _logger.info(f"Skipping monthly salary cron - today is {today}, waiting for day {target_day}")
            return

        groups = self.search([('teacher_id', '!=', False),
                              ('schedule_table_ids.payment_for_lesson', '=', 'per_month')])
        _logger.info(f"Processing monthly teacher salaries for {len(groups)} groups on {today}")

        for group in groups:
            salary = group.teacher_salary_amount
            teacher = group.teacher_id
            if not teacher or salary <= 0:
                _logger.warning(f"Skipping group {group.name} - no teacher or salary=0")
                continue

            payment = self.env["payment.edu.payment"].create({
                'user_id': self.env.user.id,            # system user
                'teacher_id': teacher.id,               # real teacher
                'amount': salary,
                'payment_type': 'online',
                'detailed_type': 'teacher_salary',
                'status': 'paid',
                'note': f"Teacher salary for group {group.name} for {today.strftime('%B %Y')}",
                'name': f"Teacher salary for {teacher.name} ({group.name}) - {today.strftime('%B %Y')}"
            })
            _logger.info(f"Paid {salary} to teacher {teacher.name} for group {group.name} (Payment ID: {payment.id})")

    def cron_pay_teacher_salary_per_lesson(self):
        today = date.today()
        lessons = self.env["edu.schedule.student.lesson"].search([
            ('schedule_lesson_id.schedule_table_id.payment_for_lesson', '=', 'per_lesson'),
            ('schedule_lesson_id.date', '<=', today),
            ('teacher_salary_paid', '=', False)
        ])
        _logger.info(f"Processing per-lesson teacher salaries for {len(lessons)} lessons on {today}")

        for lesson in lessons:
            group = lesson.schedule_lesson_id.group_id
            teacher = group.teacher_id
            if not teacher:
                _logger.warning(f"Skipping lesson {lesson.id} - no teacher for group {group.name}")
                continue

            # Calculate salary
            if group.teacher_portion_type == 'fixed':
                salary_amount = group.teacher_portion_fixed
            else:
                lesson._compute_price()
                salary_amount = (lesson.price * group.teacher_portion_percentage) / 100

            if salary_amount <= 0:
                _logger.warning(f"Skipping lesson {lesson.id} - salary amount = 0")
                continue

            payment = self.env['payment.edu.payment'].create({
                'user_id': self.env.user.id,             # system user
                'teacher_id': teacher.id,                # real teacher
                'amount': salary_amount,
                'payment_type': 'online',
                'detailed_type': 'teacher_salary',
                'status': 'paid',
                'note': f"Teacher salary for lesson {lesson.schedule_lesson_id.name} (Group: {group.name})",
                'name': f"Teacher salary for {teacher.name} for lesson {lesson.schedule_lesson_id.name}"
            })

            lesson.teacher_salary_paid = True
            _logger.info(f"Paid {salary_amount} to teacher {teacher.name} for lesson {lesson.schedule_lesson_id.name} (Payment ID: {payment.id})")
