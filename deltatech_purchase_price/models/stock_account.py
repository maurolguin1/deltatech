# -*- coding: utf-8 -*-

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def get_price_unit(self):
        """ Returns the unit price to store on the quant """

        print (self.date)
        if self.purchase_line_id:

            price_unit = self.purchase_line_id.with_context(date=self.date)._get_stock_move_price_unit()
            self.write({'price_unit': price_unit}) #mai trebuie sa pun o conditie de status ?
            # update price form last receipt
            for seller in self.product_id.seller_ids:
                if seller.name == self.purchase_line_id.order_id.partner_id:
                    if seller.min_qty == 0.0 and seller.date_start is False and seller.date_end is False:
                        if seller.currency_id:
                            if seller.currency_id == self.purchase_line_id.order_id.currency_id:
                                seller_price_unit = self.purchase_line_id.price_unit
                            else:
                                from_currency = self.env.user.company_id.currency_id.with_context(date=self.date)
                                seller_price_unit = from_currency.compute(price_unit, seller.currency)
                        else:
                            seller_price_unit = price_unit
                        seller.write({'price': seller_price_unit})

            return price_unit

        return super(StockMove, self.with_context(date=self.date)).get_price_unit()


    """
    Dupa ce intra in stoc la pretul din data receptiei cum sa 
    """