# -*- coding: utf-8 -*-
from odoo import fields, models


class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'
    _inherit = 'product.product'

    # name = fields.Char(string='Title')

    author_ids = fields.Many2many("res.partner", string="Authors")
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')

    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')


class BookCopy(models.Model):
    _name = 'library.book_copy'
    _description = 'Book Copy'
    _inherits = {'library.book': 'book'}

    internal_id = fields.Char()
