from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'edu.course'
    _description = 'Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Course Name", required=True)
    description = fields.Html(string="Course Description")
    duration = fields.Float(required=True)
    price = fields.Float(required=True)
    active = fields.Boolean(string="Active", default=True)

    subject_ids = fields.Many2many("edu.subject")
    group_ids = fields.One2many("edu.group", "course_id")
    teacher_ids = fields.Many2many("edu.teacher", tracking=True)


    @api.constrains('duration')
    def _check_duration(self):
        for rec in self:
            if rec.duration <= 0:
                raise ValidationError(_("Duration must be greater than zero."))



    def action_toggle_course(self):
        for record in self:
            record.active = not record.active