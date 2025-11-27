from odoo import models, fields, api


class EducationPayment(models.Model):
    _inherit = 'payment.edu.payment'

    group_id = fields.Many2one('edu.group')
    course_id = fields.Many2one("edu.course")




class ScheduleStudentLesson(models.Model):
    _inherit = "edu.schedule.student.lesson"

    payment_id = fields.Many2one('edu.payment', default=False)



class EducationStudent(models.Model):
    _inherit = 'user.student'

    balance = fields.Float()

    def action_balance(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': ' Balance',
            'res_model': 'payment.refuel.balance',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('student_id', '=', self.id)],
            'context': {
                'default_student_id': self.id,
            }
        }



