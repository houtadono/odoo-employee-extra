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
