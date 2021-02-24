# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'montaje.mueble.category'

    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one(
        'montaje.mueble.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        'montaje.mueble.category', 'parent_id',
        string='Child Categories')
    parent_path = fields.Char(index=True)

    furniture_ids = fields.One2many('montaje.mueble', 'category_id','Mueble')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
