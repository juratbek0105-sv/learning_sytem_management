from odoo import models, fields, api



class BranchCeo(models.Model):
    _name = "lms.branch.ceo"
    _inherits = {"res.users": 'user_id'}

    user_id = fields.Many2one("res.users")
    branch_ceo_id = fields.One2many(
        "building.branch",
        "ceo_id",
        string="Branches"
    )

    @api.model_create_multi
    def create(self, vals):
        record = super(BranchCeo, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'branch_ceo'
        return record
