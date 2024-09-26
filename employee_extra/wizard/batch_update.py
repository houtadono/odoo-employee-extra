from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.tools import groupby


class BatchUpdate(models.TransientModel):
    _name = 'hr.employee.batch.update'
    _description = 'Batch Update Wizard'

    department_selection = fields.Selection(
        selection=lambda self: self.set_department_selection(),
        string='Department',
        default='all',
    )
    is_select_department = fields.Boolean(default=True)

    is_update_years_of_experience_auto = fields.Boolean(string="Auto Update Years of Experience Base On Skills",
                                                        default=False)

    years_of_experience = fields.Integer(string="Years of Experience", default=0)
    message = fields.Text(string="Message", default="Apply updating on the selected record(s)?", readonly=1)

    certification_ids = fields.Many2many('hr.certifications', string="Certifications")

    employee_skill_ids = fields.One2many('hr.employee.skills',
                                         'employee_id', string="Skills", compute='_compute_update_skills',
                                         groups='employee_extra.group_hr_employee_experience_manager_extend')

    # field update skill
    option_update_skills = fields.Selection([
        ('update1', 'Only skills included in certifications'),
        ('update2', 'Keep skills not included in certifications')], string="Option update", default='update1')

    is_update_skills = fields.Boolean(string="View Current", default=False)  # False nếu đang ở view chọn cert
    employee_id = fields.Many2one('hr.employee', string="Employee")
    current_employee_skill_ids = fields.One2many('hr.employee.skills',
                                                 related='employee_id.employee_skill_ids', string="Current Skills")

    def set_department_selection(self):
        active_ids = self._context.get('active_ids', [])
        employees = self.env['hr.employee'].browse(active_ids)

        selection = [('all', 'All(%s)' % len(employees))]

        for department, group in groupby(employees, key=lambda x: x.department_id):
            count = len(list(group))
            selection.append((str(department.id), f"{department.name} ({count})"))

        employees_without_department = employees.filtered(lambda x: not x.department_id)
        if employees_without_department:
            selection.append(('no_department', 'No Department (%s)' % len(employees_without_department)))
        return selection

    @api.onchange('certification_ids', 'option_update_skills')
    def _compute_update_skills(self):
        if self.is_update_skills:
            self.certification_ids = self.employee_id.certification_ids

        best_cert_skill_ids = {}
        for cert in self.certification_ids:
            for cert_skill in cert.certification_skills_ids:
                current_skill = cert_skill.skill_id.id
                best_cert_skill_ids.setdefault(current_skill, cert_skill)
                if best_cert_skill_ids[current_skill].rating < cert_skill.rating:
                    best_cert_skill_ids[current_skill] = cert_skill

        self.employee_skill_ids = False
        self.employee_skill_ids = [(0, 0, {
            'skill_id': cert_skill.skill_id.id,
            'skill_type_id': cert_skill.skill_type_id,
            'skill_level_id': cert_skill.skill_level_id,
            'rating': cert_skill.rating,
        }) for cert_skill in best_cert_skill_ids.values()]

        if self.option_update_skills == 'update2':
            for cur_emp_skill in self.current_employee_skill_ids:
                find_ce_skill = self.employee_skill_ids.filtered(lambda rc: rc.skill_id.id == cur_emp_skill.skill_id.id)
                if find_ce_skill:
                    if find_ce_skill.skill_level_id < cur_emp_skill.skill_level_id:
                        find_ce_skill.skill_level_id = cur_emp_skill.skill_level_id
                else:
                    self.employee_skill_ids = [(4, cur_emp_skill.id)]
        self.employee_skill_ids = self.employee_skill_ids.sorted(key=lambda rc: (rc.skill_type_id.id, rc.skill_id.name))

    def action_batch_update(self):
        ids = self.env.context.get('active_ids')
        employees = self.env['hr.employee'].browse(ids)
        new_data = {}
        if not self.is_update_years_of_experience_auto:
            new_data['years_of_experience'] = self.years_of_experience
            employees.write(new_data)

        if not self.is_update_skills or self.option_update_skills == 'update2':
            # mặc định nếu chọn cert hoặc update2 thì là giữ lại hết skill tốt ngoài cert
            employees_selected = employees
            if self.department_selection:
                if self.department_selection == 'no_department':
                    employees_selected = employees.filtered(lambda rc: not rc.department_id)
                elif self.department_selection.isdigit():
                    employees_selected = employees.filtered(lambda rc: rc.department_id.id == int(self.department_selection))
            elif self.is_select_department:
                raise UserError("Please select Department")

            for employee in employees_selected:
                new_certs = self.certification_ids - employee.certification_ids
                if new_certs:
                    employee.write({'certification_ids': [(4, cert.id) for cert in new_certs]})
                employee.update_skills_based_on_certifications_plus(target_certs=self.certification_ids)
                if self.is_update_years_of_experience_auto:
                    employee.update_years_of_experience_base_on_skills()
        else:
            # update1 chỉ giữ lại skill tốt trong cert
            self.employee_id.update_skills_based_on_certifications()
