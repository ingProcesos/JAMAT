from odoo import fields, models
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

    # Botón: Accept
    def action_accept(self):
        for offer in self:
            # Solo una oferta aceptada por propiedad
            other = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o.id != offer.id
            )
            if other:
                raise UserError("Only one offer can be accepted for a property.")

            offer.status = "accepted"
            offer.property_id.write({
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
                "state": "offer_accepted",
            })
        return True

    # Botón: Refuse
    def action_refuse(self):
        self.write({"status": "refused"})
        return True
    # ... action_accept / action_refuse que ya tienes ...

    _sql_constraints = [
        ('check_offer_price_positive',
         'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]