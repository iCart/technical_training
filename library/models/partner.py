# -*- coding: utf-8 -*-
import logging
from datetime import date

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _description = 'Partner'
    _inherit = 'res.partner'

    name = fields.Char()
    email = fields.Char()
    address = fields.Text()
    partner_type = fields.Selection([('customer', 'Customer'), ('author', 'Author')], default="customer")
    currency_id = fields.Many2one(related='company_id.currency_id')

    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
    total_owed = fields.Monetary(compute='_compute_total_owed', readonly=True, store=True)

    @api.depends('rental_ids')
    def _compute_total_owed(self):
        for record in self:
            record.total_owed = sum(rental.amount_owed for rental in record.rental_ids if not rental.paid)

    def _cron_return_reminder(self):
        for customer in self.env['res.partner'].search([]):
            unreturned_rentals = []
            for rental in customer.rental_ids:
                days_rented = (date.today() - rental.rental_date).days
                if not rental.return_date and days_rented >= 7:  # TODO move the value to settings
                    unreturned_rentals.append(rental)

            if unreturned_rentals:
                _logger.warning('Notifying unreturned rentals for %s: %s', customer, unreturned_rentals)
                template = self.env.ref('library.return_reminder_template')
                template.with_context({'late_rentals': unreturned_rentals}).send_mail(customer.id, force_send=True)
