from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class PrinterDataMixin(models.AbstractModel):
    _name = 'printer.data.mixin'

    printer_data = fields.Text("Printer Data", readonly=True)

    def action_refresh_printer_data(self, template_name):
        tmpl = self.env['mail.template'].search([('name', '=', template_name)])
        data = tmpl._render_template(tmpl.body_html, self._name, self.id)
        self.printer_data = data

    def dummy(self):
        pass

class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'printer.data.mixin']

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.action_refresh_printer_data('Dot Matrix PO')
        return res

class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'printer.data.mixin']

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.action_refresh_printer_data('Dot Matrix SO')
        return res
