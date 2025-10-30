from odoo import models, fields, api



class Operator(models.Model):
    _name = "lms.operator"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")

    @api.model_create_multi
    def create(self, vals):
        record = super(Operator, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'operator'
        return record


