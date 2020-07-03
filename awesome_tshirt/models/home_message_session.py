from odoo import models
from odoo.http import request

from ..controllers.main import bafienistalkingtoyou


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        result['message'] = bafienistalkingtoyou()
        return result
