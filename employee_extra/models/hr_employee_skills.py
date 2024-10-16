from collections import defaultdict
from odoo import fields, models, api

class EmployeeSkill(models.Model):
    _name = 'hr.employee.skills'
    _description = 'Employee Skills'
    _order = 'skill_type_id, skill_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True, required=True, ondelete='cascade')

    skill_type_id = fields.Many2one('hr.skills.type', string="Skill Type", required=True)
    skill_id = fields.Many2one('hr.skills', string="Skill", required=True,
                               domain="[('skill_type_id', '=', skill_type_id)]", ondelete='cascade')
    skill_level_id = fields.Many2one('hr.skills.level', string="Level", required=True,
                                     domain="[('skill_type_id', '=', skill_type_id)]")

    skill_name = fields.Char(related='skill_id.name', readonly=True)

    rating = fields.Integer(string="Skill Rating", related='skill_level_id.rating', readonly=True)

    _sql_constraints = [('unique_employee_skill', 'unique (employee_id, skill_id)', "Same skill is not allowed")]

    is_skill_in_cert = fields.Boolean(compute='_compute_is_skill_in_cert', store=True)

    @api.onchange('skill_type_id')
    def _onchange_skill_type_id(self):
        if self.skill_type_id:
            self.skill_id = False

    @api.depends('skill_id', 'employee_id.certification_ids.certification_skills_ids.skill_id')
    def _compute_is_skill_in_cert(self):
        for rc in self:
            rc.is_skill_in_cert = rc.skill_id.id in rc.employee_id.certification_ids.certification_skills_ids.skill_id.ids

    def unlink(self):
        # Bypass the need for write permission
        print(self.check_access_rights('unlink'))
        return super(EmployeeSkill, self).unlink()

    def create_history(self):
        employee_skills = self.env['hr.employee.skills'].search([
            ('employee_id', 'in', self.employee_id.ids)
        ])
        employee_skill_history = self.env['hr.employee.skills.history'].search([
            ('employee_id', 'in', self.employee_id.ids),
        ])

        skills_by_employees = defaultdict(lambda: self.env['hr.employee.skills'])
        for skill in employee_skills:
            skills_by_employees[skill.employee_id.id] |= skill

        history_by_employees = defaultdict(lambda: self.env['hr.employee.skills.history'])
        for history in employee_skill_history:
            history_by_employees[history.employee_id.id] |= history

        history_create = []
        today = fields.Date.context_today(self)
        for employee in skills_by_employees:
            employee_history = history_by_employees[employee]
            for employee_skill in skills_by_employees[employee]:
                existing_history = employee_history.filtered(
                    lambda h: h.skill_id == employee_skill.skill_id and h.date == today)
                if existing_history:
                    existing_history.write({'skill_level_id': employee_skill.skill_level_id.id})
                else:
                    history_create.append({
                        'employee_id': employee_skill.employee_id.id,
                        'skill_id': employee_skill.skill_id.id,
                        'skill_level_id': employee_skill.skill_level_id.id,
                        'skill_type_id': employee_skill.skill_type_id.id,
                    })

        if history_create:
            self.env['hr.employee.skills.history'].create(history_create)

    @api.model_create_multi
    def create(self, vals_list):
        employee_skills = super().create(vals_list)
        employee_skills.create_history()
        return employee_skills

    def write(self, vals):
        res = super().write(vals)
        self.create_history()
        return res
