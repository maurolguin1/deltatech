# -*- coding: utf-8 -*-


from odoo import api, fields, models, _

class MrpProduction(models.Model):

    _inherit = 'mrp.production'


    @api.multi
    def action_assign(self):
        super(MrpProduction, self).action_assign()
        products = self.env['product.product']
        for production in self:
            for move in production.move_raw_ids:
                products |= move.product_id
        self.env["procurement.order"].supply(products)
        return True

