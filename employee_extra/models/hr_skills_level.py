from odoo import fields, models, api

class SkillLevel(models.Model):
    _name = 'hr.skills.level'
    _description = 'Skill Level'
    _order = 'rating'

    name = fields.Char(string="Level", required=True)
    rating = fields.Integer(string="Rating", default=10, required=True)
    skill_type_id = fields.Many2one('hr.skills.type', string="Skill Type")

    @api.onchange('rating')
    def _onchange_rating(self):
        if self.rating < 0:
            self.rating = 0
        elif self.rating > 100:
            self.rating = 100

    def name_get(self):
        if not self._context.get('from_skill_level_dropdown'): # nếu không  ở dropdown
            return super().name_get()
        return [(level.id, f"{level.name} ({level.rating}%)") for level in self]

    def __lt__(self, other):
        return self.rating < other.rating

    def __gt__(self, other):
        return self.rating > other.rating