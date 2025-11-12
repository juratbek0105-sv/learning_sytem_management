from odoo import models, fields, api



class Student(models.Model):
    _name = "user.student"
    _inherits = {"res.users": 'user_id'}

    student_number = fields.Char()
    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")
    teacher_ids = fields.Many2many("user.teacher")


    @api.model_create_multi
    def create(self, vals):
        record = super(Student, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'student'
        return record





