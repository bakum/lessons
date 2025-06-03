from odoo import models, fields, api


class KpiDevices(models.Model):
    _name = 'optimus.kpi.devices'
    _description = 'Kpi Devices'

    name = fields.Char('Device Name', required=True, translate=True)
    accuracy_class = fields.Selection(
        selection=[
            ('0_5', "0.5"),
            ('1_0', "1.0"),
        ],
        string="Accuracy class", required=True,
        copy=False, index=True,
        default='1_0')
    inventory_number = fields.Char('Inventory Number')
    desc = fields.Char('Device Description')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['inventory_number'] = self.env['ir.sequence'].next_by_code('inventory.number')

        return super(KpiDevices, self).create(vals_list)
