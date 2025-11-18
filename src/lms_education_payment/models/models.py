from odoo import models, fields, api


class EducationPayment(models.Model):
    _inherit = 'payment.edu.payment'

    group_id = fields.Many2one('edu.group')
    course_id = fields.Many2one("edu.course")


