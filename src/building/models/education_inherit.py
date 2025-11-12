from odoo import models, fields, api


class Timetable(models.Model):
     _inherit = 'edu.timetable'

     room_id = fields.Many2one("building.room", string="Room")
     building_id = fields.Many2one("building.building", string="Building")



class EducationCourse(models.Model):
    _inherit = 'edu.course'

    room_id = fields.Many2one('building.room', string="Classroom / Room")
    building_id = fields.Many2one('building.building', string="Building")
