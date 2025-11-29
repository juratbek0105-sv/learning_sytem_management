from odoo import models, fields, api


class EduScheduleTable(models.Model):
    _inherit = 'edu.schedule.table'


    payment_for_lesson = fields.Selection([
        ('per_lesson', 'Per lesson'),
        ('per_month', 'Per month'),
    ],default='per_lesson', string="Lesson Withdraw for", required=True)
    per_lesson = fields.Float(string="Price of per lesson")
    per_month = fields.Float(string="Price of per month")


