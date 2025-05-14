# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from extendable_pydantic import StrictExtendableBaseModel

from odoo.tools.float_utils import float_round


class InvoiceAmount(StrictExtendableBaseModel):
    amount_tax: float
    amount_untaxed: float
    amount_total: float
    amount_due: float

    @classmethod
    def from_account_move(cls, odoo_rec):
        precision = odoo_rec.currency_id.decimal_places
        return cls.model_construct(
            amount_tax=float_round(odoo_rec.amount_tax, precision),
            amount_untaxed=float_round(odoo_rec.amount_untaxed, precision),
            amount_total=float_round(odoo_rec.amount_total, precision),
            amount_due=float_round(odoo_rec.amount_residual, precision),
        )
