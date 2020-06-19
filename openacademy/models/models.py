# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(required=True)
    session_ids = fields.One2many(comodel_name='openacademy.session', inverse_name="course_id")


class Level(models.Model):
    _name = 'openacademy.level'
    _description = 'Level'

    name = fields.Char(required=True)
    level = fields.Integer(required=True)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    _rec_name = 'course_name'

    start = fields.Datetime(required=True)
    end = fields.Datetime(required=True)
    level_id = fields.Many2one(comodel_name='openacademy.level', required=True)
    instructor_id = fields.Many2one(comodel_name='res.partner')
    attendee_ids = fields.Many2many(comodel_name='res.partner', required=True)
    course_id = fields.Many2one(comodel_name='openacademy.course', on_delete='cascade', required=True)
    room_size = fields.Integer(required=True)
    number_of_attendees = fields.Integer(computed='_compute_capacity', readonly=True)
    course_name = fields.Char(related='course_id.name', store=True)
    taken_seats = fields.Float(computed='_compute_capacity')

    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")],
                             default='draft', )

    @api.onchange('attendee_ids', 'room_size')
    def _compute_capacity(self):
        for record in self:
            if record.room_size == 0:
                return 0

            n_attendees = len(record.attendee_ids)
            record.taken_seats = (n_attendees / record.room_size) * 100
            record.number_of_attendees = n_attendees

    @api.constrains('attendee_ids')
    def _check_attendee_limit(self):
        for record in self:
            if len(record.attendee_ids) > record.room_size:
                raise ValidationError("Room can only accommodate %s attendees" % record.room_size)
