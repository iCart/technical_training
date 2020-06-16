# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
