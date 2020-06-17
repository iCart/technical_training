# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(required=True)
    session_ids = fields.One2many(comodel_name='openacademy.session', inverse_name="course_id")


class Maester(models.Model):
    _name = 'openacademy.maester'
    _description = 'Maester'

    name = fields.Char(required=True)


class Level(models.Model):
    _name = 'openacademy.level'
    _description = 'Level'

    name = fields.Char(required=True)
    level = fields.Integer(required=True)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    start = fields.Datetime(required=True)
    end = fields.Datetime(required=True)
    level_id = fields.Many2one(comodel_name='openacademy.level', required=True)
    maester_id = fields.Many2one(comodel_name='openacademy.maester')
    attendee_ids = fields.Many2many(comodel_name='res.partner', required=True)
    course_id = fields.Many2one(comodel_name='openacademy.course', on_delete='cascade', required=True)
    room_size = fields.Integer(required=True)
    number_of_attendees = fields.Integer(computed='_count_attendees', readonly=True)
    course_name = fields.Char(related='course_id.name', store=True)

    states = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")],
                              default='draft', )

    @api.depends('attendee_ids')
    def _count_attendees(self):
        for record in self:
            record.number_of_attendees = len(record.attendee_ids)

    @api.constrains('attendee_ids')
    def _check_attendee_limit(self):
        for record in self:
            if len(record.attendee_ids) > record.room_size:
                raise ValidationError("Room can only accommodate %s attendees" % record.room_size)
