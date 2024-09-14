from odoo import fields, models, api

class BatchUpdate(models.TransientModel):
    _name = 'hr.employee.batch.update'
    _description = 'Batch Update Wizard'
    years_of_experience = fields.Integer(string="Years of Experience", default=0)
    message = fields.Text(string="Message", default="Apply updating on the selected record(s)?")

    def action_batch_update(self):
        ids = self.env.context.get('active_ids')
        employees = self.env['hr.employee'].browse(ids)
        new_data = {}
        if self.years_of_experience:
            new_data['years_of_experience'] = self.years_of_experience
        employees.write(new_data)