# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char()
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

    name = fields.Char()


class Level(models.Model):
    _name = 'openacademy.level'
    _description = 'Level'

    name = fields.Char()
    level = fields.Integer()


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'

    name = fields.Char()
    start = fields.Datetime()
    end = fields.Datetime()
    level = fields.Many2one(comodel_name='openacademy.level')
    attendees = fields.Many2many(comodel_name='res.partner')
    course = fields.Many2one(comodel_name='openacademy.course', on_delete='cascade')

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
