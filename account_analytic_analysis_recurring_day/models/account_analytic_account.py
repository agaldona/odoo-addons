# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import calendar


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    recurring_first_day = fields.Boolean(
        string='Generate the first day of the month', default=False)
    recurring_last_day = fields.Boolean(
        string='Generate the last day of the month', default=True)
    recurring_the_day = fields.Integer(
        string='Generated in the day of the month', default=0)

    @api.onchange('recurring_first_day')
    def onchange_recurring_first_day(self):
        self.ensure_one()
        if self.recurring_first_day:
            self.recurring_last_day = False
            self.recurring_the_day = 0

    @api.onchange('recurring_last_day')
    def onchange_recurring_last_day(self):
        self.ensure_one()
        if self.recurring_last_day:
            self.recurring_first_day = False
            self.recurring_the_day = 0

    @api.onchange('recurring_the_day')
    def onchange_recurring_the_day(self):
        self.ensure_one()
        if self.recurring_the_day:
            self.recurring_first_day = False
            self.recurring_last_day = False

    @api.multi
    def write(self, vals):
        self.ensure_one()
        if ('recurring_next_date'in vals and self.recurring_invoices and
                self.recurring_rule_type == 'monthly'):
            date = vals.get('recurring_next_date', False)
            if date:
                date = fields.Date.from_string(date)
                if date and self.recurring_first_day:
                    vals['recurring_next_date'] = "{}-{}-01".format(date.year,
                                                                    date.month)
                elif date and self.recurring_last_day:
                    vals['recurring_next_date'] = (
                        "{}-{}-{}".format(date.year, date.month,
                                          calendar.monthrange(date.year,
                                                              date.month)[1]))
                elif date and self.recurring_the_day:
                    day = self.recurring_the_day
                    if (day > calendar.monthrange(date.year, date.month)[1]):
                        day = calendar.monthrange(date.year, date.month)[1]
                    vals['recurring_next_date'] = (
                        "{}-{}-{}".format(date.year, date.month, day))
        return super(AccountAnalyticAccount, self).write(vals)
