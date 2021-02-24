# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class MueblesMontaje(models.Model):
    _name = 'montaje.mueble'
    _description = 'For furniture assemblers'

    name = fields.Char('Name', required=True)
    montador = fields.Many2many('res.users', string='Assembler')
    fecha_inicio = fields.Date('Start date')
    fecha_final = fields.Date('Finish date')    
    cliente = fields.Many2many('res.partner', string='Client')
    category_id = fields.Many2one('montaje.mueble.category', string='Category')

    state = fields.Selection([
        ('por hacer', 'Peding'),
        ('en proceso', 'In the making'),
        ('terminado', 'Finished')],
        'State', default="por hacer")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('por hacer', 'en proceso'),
                   ('en proceso', 'terminado')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for montaje in self:
            if montaje.is_allowed_transition(montaje.state, new_state):
                montaje.state = new_state
            else:
                message = _('Changing from %s to %s not allowed') % (montaje.state, new_state)
                raise UserError(message)

    def make_porhacer(self):
        self.change_state('por hacer')

    def make_enproceso(self):
        self.change_state('en proceso')

    def make_terminado(self):
        self.change_state('terminado')
    #HACER ESTO
    def log_all_muebles_members(self):
        muebles_member_model = self.env['muebles.member']  # This is an empty recordset of model muebles.member
        all_members = muebles_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True

    #HACER ESTO
    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be craeted in montaje.mueble.category model
        record = self.env['montaje.mueble.category'].create(parent_category_val)
        return True
    #HACER
    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()
    #HACER
    def find_montaje(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'montaje Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'montaje Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        montajes = self.search(domain)
        logger.info('montajes found: %s', montajes)
        return True

class mueblesMember(models.Model):

    _name = 'muebles.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "muebles member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    authored_montaje_ids = fields.Many2many(
        'montaje.mueble',
        string='Authored montajes',
        # relation='muebles_montaje_res_partner_rel'  # optional
    )
