from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Estate Property Name", required=True)
    estate_property_description = fields.Text()
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Áreas
    living_area = fields.Float(string="Living Area")
    garden_area = fields.Float(string="Garden Area")

    # Nuevo: jardín y orientación
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

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0.0) + (rec.garden_area or 0.0)

    # >>> ONCHANGE requerido por el ejercicio <<<
    @api.onchange("garden")
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                # Al marcar: fija valores
                rec.garden_area = 10.0
                rec.garden_orientation = "north"
            else:
                # Al desmarcar: limpia campos
                rec.garden_area = 0.0
                rec.garden_orientation = False
