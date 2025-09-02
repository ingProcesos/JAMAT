from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Estate Property Name", required=True)
    estate_property_description = fields.Text()
    surface = fields.Float(required=True)

    # Many2one existente
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # >>> NUEVOS CAMPOS PARA EL EJERCICIO <<<
    living_area = fields.Float(string="Living Area")
    garden_area = fields.Float(string="Garden Area")

    total_area = fields.Float(
        string="Total Area",
        compute="_compute_total_area",
        store=True,          # para poder filtrar/ordenar
        readonly=True,       # (por defecto lo es, pero lo explicitamos)
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0.0) + (rec.garden_area or 0.0)
