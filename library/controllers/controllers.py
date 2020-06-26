# -*- coding: utf-8 -*-
import json
from datetime import date, timedelta

from odoo import http


class Library(http.Controller):
    @http.route('/library/library/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/library/books/', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('library.listing', {
            'root': '/library/library',
            'books': http.request.env['product.product'].search([('is_book', '=', True), ('copy_ids.book_state', '=', 'available')]),
        })

    @http.route('/library/rent/<model("product.product"):book>/', auth='user')
    def object(self, book, **kw):
        first_available_copy = book.copy_ids.search([('book_state', '=', 'available')])[0]
        http.request.env['library.rental'].create([{
            'customer_id': http.request.uid,
            'copy_id': first_available_copy.id,
            'rental_date': date.today(),
            'return_date': date.today() + timedelta(days=7),
            'state': 'rented'
        }])
        first_available_copy.book_state = 'rented'
        return "Thank you for renting %s" % book.name
