from odoo import fields, models, api

class CertificationSkills(models.Model):
    _name = 'hr.certifications.skills'
    _description = 'Certification Skills'
    _rec_name = 'skill_id'
    _order = 'skill_type_id, skill_id'

    certification_id = fields.Many2one('hr.certifications', string="Certification", readonly=True, ondelete='cascade')

    skill_type_id = fields.Many2one('hr.skills.type', string="Skill Type", required=True)
    skill_id = fields.Many2one('hr.skills', string="Skill", required=True,
                               domain="[('skill_type_id', '=', skill_type_id)]")
    skill_level_id = fields.Many2one('hr.skills.level', string="Skill Level", required=True,
                                     domain="[('skill_type_id', '=', skill_type_id)]")

    rating = fields.Integer(string="Skill Rating", related='skill_level_id.rating', readonly=True)

    _sql_constraints = [('unique_certification_skill','unique (certification_id, skill_id)', "Same skill is not allowed")]