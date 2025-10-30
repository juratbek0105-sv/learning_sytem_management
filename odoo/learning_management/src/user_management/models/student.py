from odoo import models, fields, api



class Student(models.Model):
    _name = "lms.student"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    teacher_ids = fields.Many2many("lms.teacher")
    group_ids = fields.Many2many("edu.group")
    course_ids = fields.Many2many("edu.course")

    @api.model_create_multi
    def create(self, vals):
        record = super(Student, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'student'
        return record





