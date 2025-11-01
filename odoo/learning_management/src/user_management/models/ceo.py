from odoo import models, fields, api



class CEO(models.Model):
    _name = "user.ceo"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    branch_id = fields.One2many('res.branch', "ceo_id", required=True)


    @api.model_create_multi
    def create(self, vals):
        record = super(CEO, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'ceo'
        return record


