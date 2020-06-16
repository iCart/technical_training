# -*- coding: utf-8 -*-
from exceptions import ValidationError
from odoo import models, fields, api
from odoo import _


class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    title = fields.Char(required=True)
    authors = fields.Many2many(comodel_name='library.author', required=True)
    year_of_edition = fields.Integer(required=True)
    isbn = fields.Char(size=17)  # 13 digits for ISBN + 4 dashes
    language = fields.Many2one(comodel_name='res.lang')  # Assuming books are only ever in one language
    editor = fields.Many2one(comodel_name='library.editor', required=True)


class Author(models.Model):
    _name = 'library.author'
    _description = 'Author'

    name = fields.Char(required=True)


class Editor(models.Model):
    _name = 'library.editor'
    _description = 'Editor'

    name = fields.Char(required=True)


class Rental(models.Model):
    _name = 'library.rental'
    _description = 'Book Rental'

    books = fields.Many2many(comodel_name='library.book', required=True)
    customer = fields.Many2one(comodel_name='res.partner', required=True)
    rental_date = fields.Date(required=True)
    return_date = fields.Date()

    customer_name = fields.Char(related='customer.display_name', store=True)
    book_names = fields.Char(related='books.title', store=True)

    @api.constrains('rental_date', 'return_date')
    def _return_after_rental(self):
        for record in self:
            if record.return_date < record.rental_date:
                raise ValidationError(_("Return date must be after rental date"))
