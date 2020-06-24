# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    _rec_name = 'book_copy_id'

    customer_id = fields.Many2one('res.partner', string='Customer')
    book_id = fields.Many2one('library.book', string='Book')
    book_copy_id = fields.Many2one('library.book_copy', string='Book Copy')
    currency_id = fields.Many2one(related='book_copy_id.currency_id')

    rental_date = fields.Date()
    return_date = fields.Date()
    is_lost = fields.Boolean(string='Lost or Never Returned')

    customer_address = fields.Text(related='customer_id.address')
    customer_email = fields.Char(related='customer_id.email')

    book_authors = fields.Many2many(related='book_id.author_ids')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_publisher = fields.Many2one(related='book_id.publisher_id')

    amount_owed = fields.Monetary(compute='_compute_rental_cost', readonly=True)
    total_owed = fields.Monetary(related='customer_id.total_owed', readonly=True)
    paid = fields.Boolean(string='Rental Paid')

    @api.depends('rental_date', 'return_date', 'is_lost')
    def _compute_rental_cost(self):
        for rental in self:
            if rental.is_lost:
                rental.amount_owed = 100.0  # 100€ lost fee TODO: find a way to make this, and late fee, a setting
            elif rental.rental_date and rental.return_date:
                days_rented = (rental.return_date - rental.rental_date).days
                rental.amount_owed = rental.book_copy_id.list_price * days_rented
                if days_rented > 7:
                    rental.amount_owed += 10.0  # 10€ delay fee
            else:
                rental.amount_owed = 0
