from odoo import api, fields, models           # <- agrega api al import
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )

    # EXTRA para que la tabla muestre columnas como en las capturas
    validity = fields.Integer(string="Validity (days)", default=7)
    deadline = fields.Date(string="Deadline", compute="_compute_deadline",
                           inverse="_inverse_deadline", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            if offer.validity:
                offer.deadline = fields.Date.today() + timedelta(days=offer.validity)
            else:
                offer.deadline = False

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for rec in self:
            base = (rec.create_date or fields.Datetime.now()).date()
            rec.deadline = base + fields.Date.to_date('1970-01-01') - fields.Date.to_date('1970-01-01')  # no-op
            rec.deadline = base + fields.Date.timedelta(days=rec.validity or 0)

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline:
                base = (rec.create_date or fields.Datetime.now()).date()
                rec.validity = (rec.deadline - base).days


    @api.model
    def create(self, vals):
        offer = super().create(vals)
        prop = offer.property_id
        # cuando nace una oferta, mostramos el paso "Offer Received"
        if prop and prop.state == "new":
            prop.state = "offer_received"
        return offer

    def action_accept(self):
        for offer in self:
            # Solo una oferta aceptada por propiedad
            other = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o.id != offer.id
            )
            if other:
                raise UserError("Only one offer can be accepted for a property.")

            offer.status = "accepted"
            # (opcional) rechaza automáticamente las demás ofertas
            (offer.property_id.offer_ids - offer).write({"status": "refused"})

            offer.property_id.write({
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
                "state": "offer_accepted",
            })
        return True

    def action_refuse(self):
        self.write({"status": "refused"})
        return True

    _sql_constraints = [
        ('check_offer_price_positive',
         'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]
