# -*- coding: utf-8 -*-
from odoo import api, fields, models


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
    readers_count = fields.Integer(compute="_compute_readers_count")
    rental_ids = fields.One2many('library.rental', 'book_copy_id', string='Rentals')

    @api.depends('rental_ids.customer_id')
    def _compute_readers_count(self):
        for book_copy in self:
            book_copy.readers_count = len(book_copy.mapped('rental_ids').mapped('customer_id'))

    def open_readers(self):
        reader_ids = self.rental_ids.mapped('customer_id')
        return {
            'name': 'Readers',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'view_type': 'form',
            'target': 'new',
            'domain': [('id', 'in', reader_ids.ids)]
        }
