from odoo import tools, models, fields, api, _
from datetime import datetime,date
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    deposit_move_id = fields.Many2one('account.move',string='Asiento Deposito')

    def deposit_check(self):
        self.ensure_one()
        if self.state not in ['posted']:
            raise ValidationError(_('Cheque en estado incorrecto'))
        vals = {
                'payment_id': self.id,
                }
        wizard_id = self.env['deposit.check.wizard'].create(vals)
        return {
            'name': _('Deposit Check'),
            'res_model': 'deposit.check.wizard',
            'view_mode': 'form',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_draft(self):
        if self.deposit_move_id:
            raise ValidationError('No se puede pasar a borrador')
        return super(AccountPayment, self).action_draft()
