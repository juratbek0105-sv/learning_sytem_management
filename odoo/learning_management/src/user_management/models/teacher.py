from odoo import models, fields, api

class Teacher(models.Model):
    _name = "lms.teacher"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    subjects = fields.Many2many("edu.subject")
    group_ids = fields.Many2many("edu.group", string="Groups")
    course_ids = fields.Many2many("edu.course", string="Courses")

    @api.model_create_multi
    def create(self, vals):
        record = super(Teacher, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'teacher'
        return record
