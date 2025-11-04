from odoo import models, fields, api



class BranchCeo(models.Model):
    _name = "user.branch.ceo"
    _inherits = {"res.users": 'user_id'}
    _inherit = ['user.worker.info']


    user_id = fields.Many2one("res.users", required=True, ondelete="cascade")
    company_id = fields.Many2one('res.company', required=True)

    @api.model_create_multi
    def create(self, vals):
        record = super(BranchCeo, self).create(vals)
        if record.user_id:
            record.user_id.user_type = 'branch_ceo'
        return record
