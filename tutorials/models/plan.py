from odoo import models, fields, _, api
from odoo.tools import create_index


class InspectionPlan(models.Model):
    _name = 'optimus.kpi.plan'
    _description = 'Inspection Plan'
    _order = 'date_plan asc, id desc'


    name = fields.Char('Ref.', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    date_plan = fields.Datetime('Date Plan', required=True, default=fields.Datetime.now)
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        default='draft')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="User",
        default=lambda self: self.env.user.id,
        readonly=False, index=True
    )
    plan_line = fields.One2many(
        comodel_name='optimus.kpi.plan.line',
        inverse_name='plan_id',
        string="Plan Lines",
        copy=True)

    def init(self):
        create_index(self._cr, 'plan_date_order_id_idx', 'optimus_kpi_plan',
                     ["date_plan asc", "id desc"])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('plan.number')

        return super(InspectionPlan, self).create(vals_list)

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})


class InspectionPlanLine(models.Model):
    _name = 'optimus.kpi.plan.line'
    _description = 'Inspection Plan Line'

    plan_id = fields.Many2one(
        comodel_name='optimus.kpi.plan',
        string="Inspection Plan Reference",
        required=True, ondelete='cascade', index=True, copy=False)
    state = fields.Selection(
        related='plan_id.state',
        string="Plan Status",
        copy=False, store=True, precompute=True)
    date = fields.Datetime(related='plan_id.date_plan', string="Move Data", store=True, precompute=True)
    salesman_id = fields.Many2one(
        related='plan_id.user_id',
        string="User",
        store=True, precompute=True)
    device_id = fields.Many2one(comodel_name='optimus.kpi.devices',string="Device", required=True)
    inventory_number = fields.Char(related='device_id.inventory_number', string='Inventory Number', store=True, precompute=True)