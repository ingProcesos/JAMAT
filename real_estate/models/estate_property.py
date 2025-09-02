from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    estate_property_description = fields.Text()

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer", store=True, readonly=True)
    
    # Relación existente
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    expected_price = fields.Float(string="Expected Price", required=True, default=1.0)

    # Áreas (ejercicio previo)
    living_area = fields.Float(string="Living Area")
    garden_area = fields.Float(string="Garden Area")

    # >>> NUEVO: jardín y orientación <<<
    garden = fields.Boolean(string="Garden")
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

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

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            prices = rec.offer_ids.mapped('price')
            rec.best_offer = max(prices) if prices else 0.0


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

    # >>> ONCHANGE requerido por el ejercicio <<<
    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10.0
                rec.garden_orientation = "north"
            else:
                rec.garden_area = 0.0
                rec.garden_orientation = False


    def write(self, vals):
        # impide modificar registros bloqueados
        locked = self.filtered(lambda r: r.state in ('sold', 'cancelled'))
        if locked:
            raise UserError("You cannot modify a property that is Sold or Cancelled.")
        return super().write(vals)

    def unlink(self):
        # impide borrar registros bloqueados
        if any(r.state in ('sold', 'cancelled') for r in self):
            raise UserError("You cannot delete a property that is Sold or Cancelled.")
        return super().unlink()
  
    # >>> SQL CONSTRAINTS <<<
    _sql_constraints = [
        ('check_expected_price_positive',
         'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_selling_price_positive',
         'CHECK(selling_price >= 0)',
         'The selling price must be positive.'),
    ]
