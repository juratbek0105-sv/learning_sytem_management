from odoo import models, fields, api



class Accountant(models.Model):
    _name = "user.accountant"
    _inherits = {"res.users": 'user_id'}


    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")

    @api.model_create_multi
    def create(self, vals):
        record = super(Accountant, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'accountant'
        return record


