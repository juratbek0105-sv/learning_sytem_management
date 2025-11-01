from odoo import models, fields, api

class Teacher(models.Model):
    _name = "user.teacher"
    _inherits = {"res.users": 'user_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one("res.users", tracking=True)
    subjects = fields.Many2many("edu.subject")
    group_ids = fields.Many2many("edu.group", string="Groups")
    course_ids = fields.Many2many("edu.course", string="Courses")

    @api.model_create_multi
    def create(self, vals):
        record = super(Teacher, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'teacher'
        return record
