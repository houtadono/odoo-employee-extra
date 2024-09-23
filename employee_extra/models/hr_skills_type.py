from odoo import fields, models, api

class SkillType(models.Model):
    _name = 'hr.skills.type'
    _description = 'Skill Type'

    name = fields.Char(string="Type", required=True)
    skill_ids = fields.One2many('hr.skills', 'skill_type_id', string="Skills")
    skill_level_ids = fields.One2many('hr.skills.level', 'skill_type_id', string="Levels")
