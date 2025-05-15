import base64

from odoo import http
from odoo.http import request


class WebsiteContract(http.Controller):
    @http.route(
        ["/contract-application",],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def display_page(self, **kwargs):
        values = self.fill_values()
        return request.render("energetica_website_sale_order.contract_template", values)

    def fill_values(self):
        partner = request.env.user.partner_id
        values = {}
        if partner.street:
            values["service_address"] = partner.street
            values["invoice_address"] = partner.street
        if partner.city:
            values["service_city"] = partner.city
            values["invoice_city"] = partner.city
        if partner.zip:
            values["service_zip_code"] = partner.zip
            values["invoice_zip_code"] = partner.zip
        values["service_states"] = self.get_states()
        values["invoice_states"] = self.get_states()
        return values

    @http.route(
        ["/contract-application-created"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )  
    def create_contract(self, **kwargs):
        partner = request.env.user.partner_id
        SaleOrder = request.env["sale.order"]
        IrAttachment = request.env["ir.attachment"]

        # List of file to add to ir_attachment once we have the ID
        post_file = []
        # Info to add after the message
        post_description = []

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, "filename") and field_value:
                post_file.append(field_value)
        
        values = {
            "partner_id": partner.id,
            "service_address": kwargs.get("service_address"),
            "service_state_id": kwargs.get("service_state_id"),
            "service_city": kwargs.get("service_city"),
            "service_zip_code": kwargs.get("service_zip_code"),
            "invoice_address": kwargs.get("invoice_address"),
            "invoice_state_id": kwargs.get("invoice_state_id"),
            "invoice_city": kwargs.get("invoice_city"),
            "invoice_zip_code": kwargs.get("invoice_zip_code"),
            "is_home": kwargs.get("is_home"),
            "cnae": kwargs.get("cnae"),
            "cadastral_reference": kwargs.get("cadastral_reference"),
            "current_power": kwargs.get("current_power"),
            "tariff": kwargs.get("tariff"),
        }
        sale_order_id = SaleOrder.sudo().create(values)

        for field_value in post_file:
            attachment_value = {
                "name": field_value.filename,
                "res_model": "sale.order",
                "res_id": sale_order_id,
                "datas": base64.encodebytes(field_value.read()),
            }
            IrAttachment.sudo().create(attachment_value)

        return request.render("energetica_website_sale_order.energetica_thanks", values)

    def get_states(self):
        # Show only spanish provinces
        states = (
            request.env["res.country.state"].sudo().search([("country_id", "=", 68)])
        )
        return states
