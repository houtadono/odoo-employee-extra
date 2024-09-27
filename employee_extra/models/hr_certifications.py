from odoo import fields, models, api
from odoo.exceptions import UserError


class Certifications(models.Model):
    _name = 'hr.certifications'
    _description = 'Description'
    _order = 'name'

    name = fields.Char(string="Certification Name", required=True)
    description = fields.Text(string="Description")
    certification_skills_ids = fields.One2many('hr.certifications.skills',
                                               'certification_id', string="Certification Skills")
    employee_ids = fields.Many2many('hr.employee', 'hr_certifications_hr_employee_rel',
                                    'hr_certifications_id', 'hr_employee_id')

    @api.model_create_multi
    def create(self, vals_list):
        return super(Certifications, self).create(vals_list)

    def open_certification_view(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.certifications',
            'view_mode': 'form',
            'res_id': self.id,
            'view_id': self.env.ref('employee_extra.view_hr_certifications_form').id,
            'flags': {'mode': 'readonly'},
            'target': 'new'
        }

    def unlink_certification(self):
        if not self.env.user.has_group('employee_extra.group_hr_employee_experience_manager_extend'):
            raise UserError("You do not have access")

        certi_id = self.env.context.get('certi_id')
        employee_id = self.env.context.get('employee_id')
        if certi_id and employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            if employee:
                employee.write({'certification_ids': [(3, certi_id)]})
