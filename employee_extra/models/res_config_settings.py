from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Description'

    default_years_of_experience = fields.Integer(string="Default Years of Experience", default_model='hr.employee')
    hr_employee_is_show_cer_if_not_skill = fields.Boolean(string="Show CER if not have any skills", config_parameter='hr_employee.is_show_cer_if_not_skill')



