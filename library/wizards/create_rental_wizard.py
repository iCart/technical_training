from datetime import date

from odoo import api, models, fields


class CreateRentalWizard(models.TransientModel):
    _name = 'library.create_rental_wizard'
    _description = 'Wizard: Create Rental'

    def _default_book_copy(self):
        return self.env['library.book_copy'].browse(self._context.get('active_ids'))

    book_copy_ids = fields.Many2many(comodel_name='library.book_copy', default=_default_book_copy)
    partner_id = fields.Many2one(comodel_name='res.partner')

    def create_rentals(self):
        self.ensure_one()
        rental_vals = [{
            'customer_id': self.partner_id.id,
            'book_id': book_copy_id.book.id,
            'book_copy_id': book_copy_id.id,
            'rental_date': date.today(),
            'is_lost': False,
        } for book_copy_id in self.book_copy_ids]

        self.env['library.rental'].create(rental_vals)

        return {
            'view_id': 'library.rental_form',
            'res_model': 'library.rental'
        }
