# -*- coding: utf-8 -*-

from odoo import models, fields


class res_partner(models.Model):
    _inherit = 'res.partner'

    is_manufacturer = fields.Boolean(string='Is manufacturer')
