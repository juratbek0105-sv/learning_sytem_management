from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import logging
_logger = logging.getLogger(__name__)



class RefuelBalance(models.Model):
    _name = "payment.refuel.balance"


    student_id = fields.Many2one('user.student')
    amount = fields.Float()
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.student_id:
                record.student_id.balance += record.amount
        return records

    def unlink(self):
        for record in self:
            if record.student_id:
                if record.student_id.balance < record.amount:
                    raise ValidationError("Student balance is less than the refuel amount!")
                record.student_id.balance -= record.amount
        return super(RefuelBalance, self).unlink()



class WithdrawalBalance(models.Model):
    _name = "payment.withdrawal.balance"
    _description = "Withdrawal Balance"

    student_id = fields.Many2one('user.student', string="Student", required=True)
    amount = fields.Float(string="Amount")
    payment_id = fields.Many2one("payment.edu.payment", string="Payment")
    active = fields.Boolean(default=True)

    @api.model
    def cron_auto_withdraw(self):
        today = date.today()
        students = self.env['user.student'].search([])

        for student in students:
            lessons = self.env['edu.schedule.student.lesson'].search([
                ('student_id', '=', student.id),
                ('schedule_lesson_id.date', '<', today),
                ('payment_id', '=', False)
            ])
            if not lessons:
                continue

            for lesson in lessons:
                lesson_price = lesson.price
                if student.balance >= lesson_price:
                    # Create payment
                    payment = self.env['payment.edu.payment'].create({
                        'user_id': student.user_id.id,
                        'amount': lesson_price,
                        'payment_type': 'online',
                        'status': 'paid',
                        'note': f"Auto payment for lesson {lesson.schedule_lesson_id.name}"
                    })
                    lesson.payment_id = payment.id
                    student.balance -= lesson_price

                    self.env['payment.withdrawal.balance'].create({
                        'student_id': student.id,
                        'amount': lesson_price,
                        'payment_id': payment.id
                    })
                    _logger.info(f"Auto payment of {lesson_price} made for student {student.name} for lesson {lesson.schedule_lesson_id.name}.")
                else:
                    # Log insufficient balance
                    _logger.warning(
                        f"Insufficient balance for student {student.name} for lesson '{lesson.schedule_lesson_id.name}'. "
                        f"Student balance: {student.balance}, Lesson price: {lesson_price}"
                    )
