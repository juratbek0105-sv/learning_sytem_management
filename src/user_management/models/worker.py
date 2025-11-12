from odoo import models, fields



class WorkerInfo(models.AbstractModel):
    _name = "user.worker.info"

    experience_year = fields.Float()
    work_place_ids = fields.Many2many("user.work.places")
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female')
    ])