from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

from odoo.addons.hr_fleet.models.employee import Employee
from odoo.tools import groupby
from itertools import groupby


class EmployeeExtra(models.Model):
    _inherit = 'hr.employee'
    _description = 'Description'

    years_of_experience = fields.Integer(string="Years of Experience", default=0, tracking=True,
                                         groups="employee_extra.group_hr_employee_experience_manager")
    certification_ids = fields.Many2many('hr.certifications', string="Certifications")
    is_certification_field_readonly = fields.Boolean(compute='_compute_certification_field_readonly')

    employee_skill_ids = fields.One2many('hr.employee.skills', 'employee_id', string="Skills")
    number_of_skills = fields.Integer(string="Number of Skills", compute='_compute_number_of_skills', tracking=True)

    @api.depends('employee_skill_ids')
    def _compute_number_of_skills(self):
        for employee in self:
            employee.number_of_skills = len(employee.employee_skill_ids)

    @api.model_create_multi
    def create(self, vals_list):
        employees = super(EmployeeExtra, self).create(vals_list)
        for employee, vals in zip(employees, vals_list):
            if 'years_of_experience' in vals:
                if vals['years_of_experience'] < 0 or vals['years_of_experience'] > 30:
                    raise UserError(_("Years of experience must be between 0 and 30."))
            if 'certification_ids' in vals:
                employee.update_skills_based_on_certifications_plus()
        return employees

    def write(self, vals):
        old_certs = self.certification_ids
        res = super(EmployeeExtra, self).write(vals)
        new_certs = self.certification_ids

        added_certs = new_certs - old_certs
        removed_certs = old_certs - new_certs

        if 'years_of_experience' in vals:
            if vals['years_of_experience'] < 0 or vals['years_of_experience'] > 30:
                raise UserError(_("Years of experience must be between 0 and 30."))
        if 'certification_ids' in vals and added_certs:
            for command in vals['certification_ids']:
                if command[0] == 6:
                    self.update_skills_based_on_certifications_plus(target_certs=added_certs)
        return res

    def _compute_certification_field_readonly(self):
        self.is_certification_field_readonly = not self.env.user.has_group(
            "employee_extra.group_hr_employee_experience_manager_extend")

    def get_all_best_skills_from_certifications(self, target_certs=None):
        if target_certs is None:
            target_certs = self.certification_ids
        cert_skills = target_certs.certification_skills_ids.sorted(
            key=lambda rc: (rc.skill_id.id, -rc.rating)
        )
        best_skills = [(skill_id, next(cert_skill)) for skill_id, cert_skill in
                       groupby(cert_skills, key=lambda rc: rc.skill_id.id)]
        return best_skills

    def update_skills_based_on_certifications_plus(self, target_certs=None):
        # giữ lại hết skill tốt ngoài cert
        best_skills_from_cert = self.get_all_best_skills_from_certifications(target_certs)
        for skill_id, cert_skill in best_skills_from_cert:
            employee_skill = self.employee_skill_ids.filtered(lambda rc: rc.skill_id.id == skill_id)
            if employee_skill:
                if employee_skill.skill_level_id < cert_skill.skill_level_id:
                    employee_skill.skill_level_id = cert_skill.skill_level_id
            else:
                self.employee_skill_ids.create({
                    'employee_id': self.id,
                    'skill_id': skill_id,
                    'skill_type_id': cert_skill.skill_type_id.id,
                    'skill_level_id': cert_skill.skill_level_id.id,
                    'rating': cert_skill.rating,
                })

    def update_skills_based_on_certifications(self, target_certs=None):
        # chỉ giữ lại skill tốt trong cert
        best_skills_from_cert = self.get_all_best_skills_from_certifications(target_certs)
        for employee_skill in self.employee_skill_ids:
            find_skill = list(filter(lambda rc: rc[0] == employee_skill.skill_id.id, best_skills_from_cert))
            if find_skill:
                employee_skill.skill_level_id = find_skill[0][1].skill_level_id
                best_skills_from_cert.remove(find_skill[0])
            else:
                employee_skill.unlink()

        for skill_id, cert_skill in best_skills_from_cert:
            self.employee_skill_ids.create({
                'employee_id': self.id,
                'skill_id': skill_id,
                'skill_type_id': cert_skill.skill_type_id.id,
                'skill_level_id': cert_skill.skill_level_id.id,
                'rating': cert_skill.rating,
            })

    def update_years_of_experience_base_on_skills(self):
        total_rating = sum(self.employee_skill_ids.mapped('rating'))
        self.years_of_experience = int(total_rating / 50)

    def action_do_something(self):
        if not self.env.user.has_group('employee_extra.group_hr_employee_experience_manager'):
            raise UserError(_("You do not have access"))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Batch Update',
            'res_model': 'hr.employee.batch.update',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_extra.view_hr_employee_batch_update_wizard').id,
            'context': {
                'default_years_of_experience': self.years_of_experience,
                'default_message': 'Update this record?',
                'default_is_select_department': False,
            },
            'target': 'new',
        }

    def action_update_skills(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Skills',
            'res_model': 'hr.employee.batch.update',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_extra.view_hr_employee_batch_update_wizard').id,
            'context': {
                'default_employee_id': self.id,
                'default_is_update_skills': True,
                'certification_ids': self.certification_ids.ids,
                'default_years_of_experience': self.years_of_experience,
                'default_message': 'Update this record?',
                'default_is_select_department': False,
            },
            'target': 'new',
        }

    def unlink_certification(self):
        certi_id = self.env.context.get('certi_id')
        print(certi_id)
        if certi_id:
            self.write({'certification_ids': [(3, certi_id)]})
