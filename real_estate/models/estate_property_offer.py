from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    deadline = fields.Date(string="Deadline", compute="_compute_deadline",
                           inverse="_inverse_deadline", store=True)

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )

    # ---- DEADLINE ----
    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for rec in self:
            # base = fecha de creación (si existe) o hoy
            base = (rec.create_date or fields.Datetime.now()).date()
            rec.deadline = fields.Date.add(base, days=int(rec.validity or 0))

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline:
                base = (rec.create_date or fields.Datetime.now()).date()
                rec.validity = (rec.deadline - base).days
            else:
                rec.validity = 0

    # ---- STATE FLOW ----
    @api.model
    def create(self, vals):
        offer = super().create(vals)
        prop = offer.property_id
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
            # Actualiza propiedad y pasa a Offer Accepted
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
