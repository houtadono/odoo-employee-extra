from odoo import fields, models, api
from odoo.exceptions import UserError

class Skill(models.Model):
    _name = 'hr.skills'
    _description = 'Skills'
    _order = 'name'
    name = fields.Char(string="Skill Name", required=True)
    description = fields.Text(string="Description")

    skill_type_id = fields.Many2one('hr.skills.type', string="Skill Type")

    # add to set record rule
    employee_skill_ids = fields.One2many('hr.employee.skills', 'skill_id', string="Employee Skills")
