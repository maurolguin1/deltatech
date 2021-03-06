# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        journal = self.env['account.journal'].browse(invoice_vals['journal_id'])
        currency_id = journal.currency_id or self.env.user.company_id.currency_id
        invoice_vals['price_currency_id'] = self.pricelist_id.currency_id.id
        invoice_vals['currency_id'] = currency_id.id

        date_invoice = False
        for picking in self.picking_ids:
            if picking.state == 'done':
                if not date_invoice or date_invoice < picking.min_date[:10]:
                    date_invoice = picking.min_date[:10]

        date_invoice = date_invoice or fields.Date.context_today(self)
        invoice_vals['currency_rate'] = self.pricelist_id.currency_id.with_context(date=date_invoice).compute(1,
                                                                                                              currency_id,
                                                                                                              round=False)
        invoice_vals['date_invoice'] = date_invoice
        # cu obtin data ultimului aviz ?
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # se convertesc facturile in moneda jurnalului
    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        super(SaleOrderLine, self).invoice_line_create(invoice_id, qty)
        invoice = self.env['account.invoice'].browse(invoice_id)
        lines = self.env['account.invoice.line'].search([('invoice_id', '=', invoice_id)])
        to_currency = invoice.journal_id.currency_id or self.env.user.company_id.currency_id
        from_currency = self.order_id.pricelist_id.currency_id


        date_invoice = invoice.date_invoice or fields.Date.context_today(self)
        for line in lines:
            price_unit = from_currency.with_context(date=date_invoice).compute(line.price_unit, to_currency)
            line.write({'price_unit': price_unit})

    """
    @api.multi
    def _create_invoice(self, order, so_line, amount):
        print "trece pe aici"
        invoice = super(SaleAdvancePaymentInv,self)._create_invoice(order, so_line, amount)
        invoice.write({'price_currency_id':order.currency_id.id})
        currency_id = invoice.journal_id.currency_id or self.env.user.company.currency_id
        if invoice.currency_id != currency_id:
            print "Trebuie sa modific pretul"

        return invoice


    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
    """
