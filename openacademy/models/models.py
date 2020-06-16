# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(required=True)
    # value = fields.Integer()
    # value2 = fields.Float(compute='_value_pc', store=True)
    # description = fields.Text()

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100


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

    name = fields.Char(required=True)
    start = fields.Datetime(required=True)
    end = fields.Datetime(required=True)
    level = fields.Many2one(comodel_name='openacademy.level', required=True)
    attendees = fields.Many2many(comodel_name='res.partner', required=True)
    course = fields.Many2one(comodel_name='openacademy.course', on_delete='cascade', required=True)
    room_size = fields.Integer(required=True)

    status = fields.Char(compute='_compute_status')

    @api.depends('start', 'end')
    def _compute_status(self):
        now = datetime.now()
        for record in self:
            if record.start > now:
                record.status = 'Planned'
            elif record.end < now:
                record.status = "In Preparation"
            else:
                record.status = "In Progress"
