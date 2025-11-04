from odoo import models, fields, api


class Teacher(models.Model):
    _name = "user.teacher"
    _inherits = {"res.users": 'user_id'}
    _inherit = ['user.worker.info']

    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Teacher, self).create(vals_list)
        for record in records:
            if record.user_id:
                record.user_id.user_type = 'teacher'
        return records
