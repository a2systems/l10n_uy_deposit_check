from odoo import fields,models, api, _
from odoo.exceptions import UserError, ValidationError
import logging
from datetime import date

_logger = logging.getLogger(__name__)

class DepositCheckWizard(models.TransientModel):
    _name = 'deposit.check.wizard'
    _description = 'deposit.check.wizard'

    payment_id = fields.Many2one('account.payment',string='Pago')
    journal_id = fields.Many2one('account.journal',string='Banco',domain=[('type','=','bank')])

    def btn_confirm(self):
        if not self.payment_id:
            raise ValidationError('No hay pago seleccionado')
        if not self.journal_id:
            raise ValidationError('No hay banco seleccionado')
        vals_move = {
                'journal_id': self.journal_id.id,
                'ref': 'Deposito cheque %s'%(self.payment_id.check_number),
                'date': str(date.today()),
                'move_type': 'entry',
            }
        move_id = self.env['account.move'].create(vals_move)
        vals_debit = {
                'move_id': move_id.id,
                'account_id': self.journal_id.default_account_id.id,
                'name': 'Debito deposito cheque %s'%(self.payment_id.check_number),
                'credit': 0,
                'debit': abs(self.payment_id.amount_company_currency_signed),
                'currency_id': self.payment_id.currency_id.id,
                }
        if self.payment_id.currency_id.id != self.payment_id.company_id.currency_id.id:
            vals_debit['amount_currency'] = abs(self.payment_id.amount_signed)
        debit_id = self.env['account.move.line'].with_context(check_move_validity=False).create(vals_debit)
        vals_credit = {
                'move_id': move_id.id,
                'account_id': self.payment_id.journal_id.default_account_id.id,
                'name': 'Credito deposito cheque %s'%(self.payment_id.check_number),
                'debit': 0,
                'credit': abs(self.payment_id.amount_company_currency_signed),
                'currency_id': self.payment_id.currency_id.id,
                }
        if self.payment_id.currency_id.id != self.payment_id.company_id.currency_id.id:
            vals_credit['amount_currency'] = self.payment_id.amount_signed * (-1)
        credit_id = self.env['account.move.line'].with_context(check_move_validity=False).create(vals_credit)
        move_id.action_post()
        self.payment_id.deposit_move_id = move_id.id

