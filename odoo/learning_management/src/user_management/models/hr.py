from odoo import models, fields, api



class HR(models.Model):
    _name = "user.hr"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")

    @api.model_create_multi
    def create(self, vals):
        record = super(HR, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'hr'
        return record


