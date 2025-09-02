from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    estate_property_description = fields.Text()

    # Relación existente
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Áreas (ejercicio previo)
    living_area = fields.Float(string="Living Area")
    garden_area = fields.Float(string="Garden Area")

    total_area = fields.Float(
        string="Total Area",
        compute="_compute_total_area",
        store=True,
        readonly=True,
    )

    # Estado del inmueble
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        readonly=True,
        copy=False,
    )

    # Se llenan cuando se acepta una oferta
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0.0) + (rec.garden_area or 0.0)

    # Botón: Sold
    def action_sold(self):
        for rec in self:
            if rec.state == "cancelled":
                raise UserError("A cancelled property cannot be set as sold.")
            rec.state = "sold"
        return True

    # Botón: Cancel
    def action_cancel(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            rec.state = "cancelled"
        return True
