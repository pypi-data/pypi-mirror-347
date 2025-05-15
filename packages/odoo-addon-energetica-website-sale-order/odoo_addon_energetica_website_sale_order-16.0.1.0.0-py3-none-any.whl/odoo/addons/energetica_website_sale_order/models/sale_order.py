from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    service_address = fields.Char()
    service_state_id = fields.Many2one("res.country.state", string="Service Province")
    service_city = fields.Char()
    service_zip_code = fields.Char()
    invoice_address = fields.Char()
    invoice_state_id = fields.Many2one("res.country.state", string="Invoice Province")
    invoice_city = fields.Char()
    invoice_zip_code = fields.Char()
    is_home = fields.Boolean()
    cnae = fields.Char()
    cadastral_reference = fields.Char()
    statement = fields.Boolean()
    current_power = fields.Char()
    tariff = fields.Selection(
        selection=[
            ("periodic","Periodic"),
            ("indexed", "Indexed")
        ]
    )