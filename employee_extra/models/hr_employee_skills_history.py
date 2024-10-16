from odoo import fields, models, api


class EmployeeSkillHistory(models.Model):
    _name = 'hr.employee.skills.history'
    _description = 'Description'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    skill_type_id = fields.Many2one('hr.skills.type', string="Skill Type", required=True)
    skill_id = fields.Many2one('hr.skills', string="Skill", required=True,
                               domain="[('skill_type_id', '=', skill_type_id)]", ondelete='cascade')
    skill_level_id = fields.Many2one('hr.skills.level', string="Level", required=True,
                                     domain="[('skill_type_id', '=', skill_type_id)]")

    skill_name = fields.Char(related='skill_id.name', readonly=True)

    rating = fields.Integer(string="Skill Rating", related='skill_level_id.rating', group_operator="avg", store=True)

    date = fields.Date(default=fields.Date.context_today)

