# -*- coding: utf-8 -*-
from datetime import date
from odoo import exceptions

from odoo import api, exceptions, fields, models


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.partner', ondelete='set null', string="Responsible")
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    level = fields.Selection([('1', 'Easy'), ('2', 'Medium'), ('3', 'Hard')], string="Difficulty Level")
    session_count = fields.Integer(compute="_compute_session_count")
    attendees_count = fields.Integer(compute="_compute_attendees_count")

    @api.depends('session_ids')
    def _compute_session_count(self):
        for course in self:
            course.session_count = len(course.session_ids)

    @api.depends('session_ids')
    def _compute_attendees_count(self):
        for course in self:
            course.attendees_count = sum(len(session.attendee_ids) for session in course.session_ids)

    def action_show_participants(self):
        return {
            'name': 'Attending %s' % self.name,
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'openacademy.session',
            'domain': [('course_id', '=', self.id)],
        }


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    description = fields.Html()
    active = fields.Boolean(default=True)
    state = fields.Selection([('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done")], default='draft')
    level = fields.Selection(related='course_id.level', readonly=True)
    responsible_id = fields.Many2one(related='course_id.responsible_id', readonly=True, store=True)

    start_date = fields.Date(default=fields.Date.context_today)
    end_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)

    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=[('instructor', '=', True)])
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees", groups='openacademy.group_maesters,openacademy.group_archmaesters')
    attendees_count = fields.Integer(compute='_get_attendees_count', store=True)
    seats = fields.Integer()
    taken_seats = fields.Float(compute='_compute_taken_seats', store=True)

    is_paid = fields.Boolean(default=False, string="Has been invoiced")

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for session in self:
            if not session.seats:
                session.taken_seats = 0.0
            else:
                session.taken_seats = 100.0 * len(session.attendee_ids) / session.seats

            if session.taken_seats > 50 and session.state == 'draft':
                session.state = 'confirmed'
                template = self.env.ref('openacademy.session_confirmed_template')
                session.message_post_with_template(template_id=template.id)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for session in self:
            session.attendees_count = len(session.attendee_ids)

    @api.onchange('start_date', 'end_date')
    def _compute_duration(self):
        if not (self.start_date and self.end_date):
            return
        if self.end_date < self.start_date:
            return {'warning': {
                'title': "Incorrect date value",
                'message': "End date is earlier then start date",
            }}
        delta = fields.Date.from_string(self.end_date) - fields.Date.from_string(self.start_date)
        self.duration = delta.days + 1

    def create_invoice(self):
        """
        date = today
        state =draft
        move_type out_invoice
        journal_id many2one
        currency_id many2one
        partner_id
        """

        for session_id in self.ids:
            session = self.env['openacademy.session'].browse(ids=[session_id])[0]

            # Shouldn't happen since we hide the button on the form
            # but it *might* happen
            if session.is_paid:
                raise exceptions.UserError("Creating an invoice for an already invoiced session")

            instructor_id = session.instructor_id
            previous_bill = self.env['account.move'].search([('partner_id', '=', instructor_id.id)])
            if previous_bill:
                bill = previous_bill[0]
            else:
                bill = self.env['account.move'].create([{
                    'date': date.today(),
                    'state': 'draft',
                    'type': 'in_invoice',
                    'partner_id': instructor_id.id,
                }])

            self.env['account.move.line'].create([{
                "move_id": bill.id,
                "name": session.name,
                "quantity": session.duration,
                "account_id": instructor_id.property_account_payable_id.id,
            }])
            session.is_paid = True
