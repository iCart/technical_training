# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddAttendees(models.TransientModel):
    _name = 'openacademy.add_attendees_wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session',
                                   string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def subscribe(self):
        # TODO: check here that we don't add more attendees than seats
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
