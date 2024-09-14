from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class EmployeeExtra(models.Model):
    _inherit = 'hr.employee'
    _description = 'Description'

    years_of_experience = fields.Integer(string="Years of Experience", default=0, tracking=True,
                                         groups="employee_extra.group_hr_employee_experience_manager")


    @api.model
    def create(self, vals_list):
        if 'years_of_experience' in vals_list:
            if vals_list['years_of_experience'] < 0 or vals_list['years_of_experience'] > 30:
                raise UserError(_("Years of experience must be between 0 and 30."))
        return super(EmployeeExtra, self).create(vals_list)

    def write(self, vals):
        if 'years_of_experience' in vals:
            if vals['years_of_experience'] < 0 or vals['years_of_experience'] > 30:
                raise UserError(_("Years of experience must be between 0 and 30."))
        return super(EmployeeExtra, self).write(vals)

    # EDITABLE_FIELDS = ['years_of_experience', 'job_id', 'parent_id']
    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     res = super(EmployeeExtra, self).fields_get(allfields, attributes)
    #     if not self.env.user.has_group('employee_extra.group_hr_employee_experience_manager'):
    #         for field_name in self.EDITABLE_FIELDS:
    #             if field_name in res:
    #                 res[field_name]['readonly'] = True
    #     return res

    def action_do_something(self):
        if not self.env.user.has_group('employee_extra.group_hr_employee_experience_manager'):
            raise UserError(_("You do not have access"))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Years of Experience',
            'res_model': 'hr.employee.batch.update',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_extra.view_hr_employee_batch_update_wizard').id,
            'context': {
                'default_active_ids': self.id,
                'default_years_of_experience': self.years_of_experience,
                'default_message': 'Update this record?',
            },
            'target': 'new',
        }