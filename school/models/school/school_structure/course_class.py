# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from odoo.tools import misc
import datetime
import logging
import math

_logger = logging.getLogger(__name__)


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = "School class"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, translate=True)
    abbreviation = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    course_id = fields.Many2one('school.course', required=True)
    required_skill_ids = fields.One2many(
        'school.course.required.skill', 'res_id', domain="[('res_model', '=', 'school.class')]")

    program_ids = fields.Many2many('school.program', related='course_id.program_ids')
    student_ids = fields.Many2many(
        'school.student', relation='student_class_rel',
        column1='class_id', column2='student_id')

    period_relation_ids = fields.One2many('school.rel.class.period', 'class_id')
    linked_class_ids = fields.One2many(
        'school.class', 'root_linked_class_id', domain="[('id', '!=', id)]")
    root_linked_class_id = fields.Many2one('school.class')
    substitute_ids = fields.Many2many(
        'hr.employee', relation='substitute_employee_class_rel',
        column1='class_id', column2='substitute_id')
    employee_ids = fields.Many2many(
        'hr.employee', relation='employee_class_rel',
        column1='class_id', column2='employee_id')
    period_ids = fields.Many2many('school.period', store=True, compute='compute_period_ids')
    event_ids = fields.One2many('calendar.event', 'class_id')
    event_setup_ids = fields.One2many(
        'school.class.event.setup', 'class_id', store=True, required=True, readonly=False,
        compute='compute_event_setup')

    @api.model
    def create(self, vals):
        course_class = super().create(vals)
        return course_class

    @api.depends('employee_ids')
    def compute_event_setup(self):
        for course_class in self:
            course_class._generate_event_setup()

            # check for user
            x_group_portal_user = self.env.ref('base.group_portal')
            for employee in self.employee_ids:
                employee = employee._origin
                if employee.exists() and not employee.user_id and employee.work_email:
                    # Check if there is a user with that email
                    user = self.env['res.users'].search([('login', '=', employee.work_email)])
                    # If not we just create it
                    if not user:
                        user = self.env['res.users'].create({
                            'name': employee.name,
                            'login': employee.work_email,
                            'groups_id': [(6, 0, x_group_portal_user.ids)]
                            })
                    employee.user_id = user

            course_class.event_setup_ids.write({'employee_ids': [(6, 0, self.employee_ids.ids)]})

    @api.depends('period_relation_ids')
    def compute_period_ids(self):
        for course_class in self:
            course_class.period_ids = course_class.mapped('period_relation_ids.period_ids')

    def _generate_event_setup(self):
        for course_class in self:
            course_class.event_setup_ids.create(self._get_event_setup_vals())

    def _get_event_setup_vals(self):
        self.ensure_one()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return [{
            'type': weekday,
            'class_id': self.id,
            'enabled': True,
        } for weekday in weekdays if not self.event_setup_ids.filtered_domain([('type', '=', weekday)])]

    def action_generate_events(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'generate.class.event.wizard',
            'name': _("Generate class events"),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_class_id': self.id}
        }

    def generate_event(self, event_date, on_conflict='no_create'):
        for course_class in self:

            # You might ask, why did you make the select have strings instead of integer.
            # Well... Odoo doesn't allow us to use integer,
            # now, I know that I can parse them later if I put the integers
            # as strings. But, I prefer using text like 'monday' for the xml rpc API, so, I guess that it can be easier.

            weekday_equivalent_in_number = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6,
                }

            for event_setup in course_class.event_setup_ids:
                # Check weekday
                weekday_number = weekday_equivalent_in_number.get(event_setup.type, 0)
                if event_setup.enabled and event_date.weekday() == weekday_number:
                    for hour_start, hour_stop in event_setup.hour_range_ids.mapped(lambda hri: (hri.hour_start, hri.hour_stop)):
                        calendar_event = self._generate_event_in_hours(
                                            event_date=event_date,
                                            hour_start=hour_start,
                                            hour_stop=hour_stop,
                                            employee_ids=event_setup.employee_ids,
                                            on_conflict=on_conflict)

    def _generate_event_in_hours(self, event_date, hour_start, hour_stop, employee_ids, on_conflict='no_create'):
        employee_partners = employee_ids.mapped('user_partner_id')
        partner_ids = self.student_ids.mapped('partner_id') + employee_partners
        # Check if conflict
        conflict_events = self.env['calendar.event']
        datetime_start = self._combine_date_float_time(event_date, hour_start)
        datetime_stop = self._combine_date_float_time(event_date, hour_stop)

        compute_name = "%s (%s)" % (self.abbreviation, self.course_id.abbreviation)

        user = employee_ids.mapped('user_id')[:1]
        if not user:
            raise exceptions.UserError(_("At least one employee should have an user!"))

        for partner in partner_ids:
            conflict = self._check_if_event_conflict(partner.id, datetime_start, datetime_stop)
            if conflict:
                conflict_events += conflict
                if on_conflict == 'no_create':
                    partner_ids -= partner
                if on_conflict == 'overwrite':
                    conflict_events.partner_ids -= partner
                    if not conflict_events.partner_ids:
                        conflict_events.sudo().unlink()
                if on_conflict == 'warn':

                    conflict_events_html = ""

                    for event in conflict_events:
                        conflict_events_html += "<li>%s, start: %s, stop: %s</li>" % (event.name, event.start, event.stop)

                    log_note_message = """ 
                    There is a conflict with the following events: 
                    <ul>
                    %s
                    </ul>
                    <br/>
                    for the partner %s """ % (conflict_events_html, partner.name)
                    self.message_post(body=log_note_message)

        if partner_ids:
            calendar_event = self.env['calendar.event'].create({
                'name': compute_name,
                'start': datetime_start,
                'stop': datetime_stop,
                'class_ids': [(6, 0, self.ids)],
                'user_id': user.id,
                })

            calendar_event._cr.commit()
            calendar_event.partner_ids = partner_ids

            return calendar_event
        return False

    @api.model
    def _check_if_event_conflict(self, partner_id, datetime_start, datetime_stop):

        # Find an event
        conflict_events = self.env['calendar.event'].search([
            ('partner_ids', '=', partner_id),
            '|',
            '&', ('start', '<=', datetime_start), ('stop', '>=', datetime_start),
            '&', ('start', '<=', datetime_stop), ('stop', '>=', datetime_stop)
            ])
        return conflict_events

    @api.model
    def _combine_date_float_time(self, date_to_combine, float_time=0):
        date_time = datetime.time(hour=int(float_time), minute=round(math.modf(float_time)[0] / (1 / 60.0)))
        combined_date = datetime.datetime.combine(date_to_combine, date_time)
        return combined_date


class CourseClassPeriod(models.Model):
    _name = 'school.rel.class.period'
    _description = "M2M model for periods and classes"

    class_id = fields.Many2one('school.class', required=True)
    class_program_ids = fields.Many2many('school.program', related='class_id.program_ids')
    program_id = fields.Many2one('school.program', required=True)
    period_category_id = fields.Many2one('school.period.category', required=True)
    period_ids = fields.Many2many('school.period', required=True, )
    other_program_ids = fields.Many2many('school.program', compute='compute_other_programs')

    @api.onchange('class_id')
    def compute_other_programs(self):
        for record in self:
            record.other_program_ids = record.mapped('class_id.period_relation_ids.program_id')

    @api.onchange('period_category_id', 'program_id')
    def clear_periods(self):
        self.period_ids = False


class CourseClassEventSetup(models.Model):
    _name = 'school.class.event.setup'
    _description = "Event setup for classes"

    class_id = fields.Many2one('school.class')
    enabled = fields.Boolean()
    type = fields.Selection(
        [('monday', _("Monday")),
         ('tuesday', _("Tuesday")),
         ('wednesday', _("Wednesday")),
         ('thursday', _("Thursday")),
         ('friday', _("Friday")),
         ('saturday', _("Saturday")),
         ('sunday', _("Sunday"))])
    # date_ranges = fields.One2many('school.class.event.setup.range', 'setup_id')
    hour_range_ids = fields.One2many('school.class.event.setup.range', 'setup_id')
    employee_ids = fields.Many2many('hr.employee', readonly=False)

    # This is a technical field, so it doesn't really matter this ugly name
    all_hour_range_compute = fields.Many2many(
        'school.class.event.setup.range', store=True, compute='compute_all_hour_range',
        relation='setup_all_hour_ranges_rel')

    total_hours = fields.Float(compute='compute_total_hours', store=True)

    @api.depends('hour_range_ids')
    def compute_all_hour_range(self):
        for setup in self:
            setup.all_hour_range_compute = setup.class_id.event_setup_ids.mapped('hour_range_ids')

    @api.depends('hour_range_ids')
    def compute_total_hours(self):
        for setup in self:
            setup.total_hours = sum(setup.hour_range_ids.mapped(lambda hri: hri.hour_stop - hri.hour_start))


class CourseClassEventSetupRange(models.Model):
    _name = 'school.class.event.setup.range'

    name = fields.Char(store=True, compute='compute_name')
    setup_id = fields.Many2one(
        'school.class.event.setup', readonly=True, ondelete='cascade', required=True)

    hour_start = fields.Float()
    hour_stop = fields.Float()

    @api.depends('hour_start', 'hour_stop')
    def compute_name(self):
        for setup_range in self:
            html_hour_start = misc.format_duration(setup_range.hour_start)
            html_hour_stop = misc.format_duration(setup_range.hour_stop)
            setup_range.name = "%s - %s" % (html_hour_start, html_hour_stop)
