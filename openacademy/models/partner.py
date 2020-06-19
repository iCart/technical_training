# -*- coding: utf-8 -*-, api
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Partner'

    name = fields.Char()

    instructor = fields.Boolean(default=False)
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
