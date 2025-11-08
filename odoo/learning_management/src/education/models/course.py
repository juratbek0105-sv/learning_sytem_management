from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'edu.course'
    _description = 'Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string="Name", required=True)
    description = fields.Html(string="Description")
    duration = fields.Float(required=True, string="Duration")
    duration_uom_id = fields.Many2one("uom.uom", domain=[("category_id.name", "=", "Time")])
    price = fields.Float(required=True, string="Price")
    active = fields.Boolean(string="Active", default=True)

    group_ids = fields.One2many("edu.group", "course_id")
    teacher_ids = fields.Many2many("user.teacher", tracking=True)
    student_ids = fields.Many2many("user.student", string="Students")

    @api.constrains('duration')
    def _check_duration(self):
        for rec in self:
            if rec.duration <= 0:
                raise ValidationError(_("Duration must be greater than zero."))



    def action_toggle_course(self):
        for record in self:
            record.active = not record.active