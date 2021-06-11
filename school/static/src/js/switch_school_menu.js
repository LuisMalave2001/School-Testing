odoo.define('districtCode_base.SwitchSchoolMenu', function (require) {
    "use strict";

    /**
     * When Odoo is configured in multi-districtCode mode, users should obviously be able
     * to switch their interface from one districtCode to the other.  This is the purpose
     * of this widget, by displaying a dropdown menu in the systray.
     */

    const config = require('web.config');
    const core = require('web.core');
    const session = require('web.session');
    const SystrayMenu = require('web.SystrayMenu');
    const Widget = require('web.Widget');

    const _t = core._t;

    const SwitchSchoolMenu = Widget.extend({
        template: 'SwitchSchoolMenu',
        events: {
            'keydown .dropdown-submenu[data-menu="district"] div.log_into': '_onSwitchDistrictCodeClick',
            'click .dropdown-submenu[data-menu="district"] div.log_into': '_onSwitchDistrictCodeClick',
            'keydown .dropdown-submenu[data-menu="district"] div.toggle_district': '_onToggleDistrictCodeClick',
            'click .dropdown-submenu[data-menu="district"] div.toggle_district': '_onToggleDistrictCodeClick',

            'keydown .dropdown-item[data-menu="school"] div.log_into': '_onSwitchSchoolCodeClick',
            'click .dropdown-item[data-menu="school"] div.log_into': '_onSwitchSchoolCodeClick',
            'keydown .dropdown-item[data-menu="school"] div.toggle_school': '_onToggleSchoolCodeClick',
            'click .dropdown-item[data-menu="school"] div.toggle_school': '_onToggleSchoolCodeClick',
        },
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
            this._onSwitchDistrictCodeClick = _.debounce(this._onSwitchDistrictCodeClick, 1500, true);
        },

        /**
         * @override
         */
        willStart: function () {
            // District codes
            this.allowed_district_ids = session.user_context.allowed_district_ids;
            this.user_districts = session.user_districts.allowed_districts;
            this.current_district = _.find(session.user_districts.allowed_districts, districtCode => {
                return districtCode.id === this.allowed_district_ids[0]
            });
            this.current_district_name = this.current_district.name;

            // School codes
            this.allowed_school_ids = session.user_context.allowed_school_ids;
            this.user_schools = session.user_schools.allowed_schools;
            this.user_schools_by_district_id = _.groupBy(this.user_schools, 'district_id')
            this.current_school = _.find(session.user_schools.allowed_schools, schoolCode => {
                return schoolCode.id === this.allowed_school_ids[0]
            });
            this.current_school_name = this.current_school.name;

            return this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // District code
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onSwitchDistrictCodeClick: function (ev) {
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            const dropdownItem = $(ev.currentTarget).parent();
            let dropdownMenu = dropdownItem.parent();
            const districtCodeID = dropdownItem.data('districtCodeId');
            let current_school_id = this.allowed_school_ids[0];
            let allowed_district_ids = this.allowed_district_ids;
            let allowed_school_ids = this.allowed_school_ids;
            const schoolCodeIds = _.map(
                this.user_schools_by_district_id[districtCodeID],
                school => school.id);
            if (dropdownItem.find('.toggle_district .fa-square-o').length) {
                // 1 enabled district code: Stay in single district code mode

                // Now we need to add the school code of the recently added district code
                current_school_id = schoolCodeIds[0];

                if (this.allowed_district_ids.length === 1) {
                    if (this.isMobile) {
                        dropdownMenu = dropdownMenu.parent();
                    }

                    // Toggle Checkboxes
                    dropdownMenu.find('.fa-check-square').removeClass('fa-check-square').addClass('fa-square-o');
                    dropdownItem.find('.fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');

                    // Alter the allowed codes ids
                    allowed_district_ids = [districtCodeID];
                    allowed_school_ids = schoolCodeIds;

                } else {
                    // Multi district code mode
                    allowed_district_ids.push(districtCodeID);
                    allowed_school_ids = _.union(allowed_school_ids, schoolCodeIds);
                    dropdownItem.find('.fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');
                }
            } else {
                // This means that we need to change the current school code to the
                // First actived school code
                const schoolCodeItemEl = dropdownItem.find('[data-menu="school"] .fa-check-square').get(0);
                if (schoolCodeItemEl) {
                    current_school_id = parseInt(schoolCodeItemEl.closest('[data-school-code-id]').dataset.schoolCodeId)
                } else {
                    // No checked element. So we active them all
                    current_school_id = schoolCodeIds[0];
                    allowed_school_ids = _.union(allowed_school_ids, schoolCodeIds);
                }
            }

            $(ev.currentTarget).attr('aria-pressed', 'true');
            session.setSchoolCodes(
                districtCodeID, allowed_district_ids,
                current_school_id, allowed_school_ids);
        },

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onToggleDistrictCodeClick: function (ev) {
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            const dropdownItem = $(ev.currentTarget).parent();
            const districtCodeID = dropdownItem.data('districtCode-id');
            let allowed_district_ids = this.allowed_district_ids;
            let allowed_school_ids = this.allowed_school_ids;
            const current_district = allowed_district_ids[0];
            const current_school = allowed_school_ids[0];
            const districtSchoolCodeIds = _.map(
                this.user_schools_by_district_id[districtCodeID],
                school => school.id);
            if (dropdownItem.find('.toggle_district .fa-square-o').length) {
                allowed_district_ids.push(districtCodeID);
                dropdownItem.find('.fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');

                // Add school codes
                allowed_school_ids = _.union(districtSchoolCodeIds, allowed_school_ids);
                $(ev.currentTarget).attr('aria-checked', 'true');
            } else {
                if (districtSchoolCodeIds) {
                    allowed_school_ids = _.without(allowed_school_ids, ...districtSchoolCodeIds)
                }
                allowed_district_ids.splice(allowed_district_ids.indexOf(districtCodeID), 1);
                dropdownItem.find('.fa-check-square').addClass('fa-square-o').removeClass('fa-check-square');
                $(ev.currentTarget).attr('aria-checked', 'false');
            }
            session.setSchoolCodes(
                current_district, allowed_district_ids,
                current_school, allowed_school_ids
            );
        },


        //--------------------------------------------------------------------------
        // School code
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onSwitchSchoolCodeClick: function (ev) {
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            const dropdownItem = $(ev.currentTarget).parent();
            let dropdownMenu = dropdownItem.parent();
            const schoolCodeID = dropdownItem.data('schoolCodeId');
            const districtDropdownItem = dropdownItem.closest('[data-district-code-id]')
            const districtCodeID = districtDropdownItem.data('districtCodeId');
            let current_school_id = this.allowed_school_ids[0];
            let allowed_district_ids = this.allowed_district_ids;
            let allowed_school_ids = this.allowed_school_ids;
            const schoolCodeIds = _.map(
                this.user_schools_by_district_id[districtCodeID],
                school => school.id);
            if (dropdownItem.find('.fa-square-o').length) {
                // 1 enabled district code: Stay in single district code mode

                // Now we need to add the school code of the recently added district code

                // We ensure that the districtCode is in the allowed district codes variable
                allowed_district_ids = _.union(allowed_district_ids, [districtCodeID]);
                districtDropdownItem.find('.toggle_district .fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');

                if (dropdownMenu.find('.fa-check-square').length <= 1) {
                    if (this.isMobile) {
                        dropdownMenu = dropdownMenu.parent();
                    }

                    // Toggle Checkboxes
                    dropdownMenu.find('.fa-check-square').removeClass('fa-check-square').addClass('fa-square-o');

                    // Alter the allowed codes ids
                    allowed_school_ids = _.without(allowed_school_ids, ...schoolCodeIds);
                }

                allowed_school_ids.push(schoolCodeID);
                dropdownItem.find('.fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');
            }

            $(ev.currentTarget).attr('aria-pressed', 'true');
            session.setSchoolCodes(
                districtCodeID, allowed_district_ids,
                schoolCodeID, allowed_school_ids);
        },

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onToggleSchoolCodeClick: function (ev) {
            if (ev.type == 'keydown' && ev.which != $.ui.keyCode.ENTER && ev.which != $.ui.keyCode.SPACE) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            const dropdownItem = $(ev.currentTarget).parent();
            const schoolCodeID = dropdownItem.data('schoolCodeId');
            const districtDropdownItem = dropdownItem.closest('[data-district-code-id]')
            const districtCodeID = districtDropdownItem.data('districtCodeId');
            let allowed_district_ids = this.allowed_district_ids;
            let allowed_school_ids = this.allowed_school_ids;
            const current_district = allowed_district_ids[0];
            const current_school = allowed_school_ids[0];

            // Simply check if is checked or not
            if (dropdownItem.find('.fa-square-o').length) {
                allowed_school_ids.push(schoolCodeID);
                // We ensure that the districtCode is in the allowed district codes
                allowed_district_ids = _.union(allowed_district_ids, [districtCodeID]);

                // Just style
                dropdownItem.find('.fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');
                districtDropdownItem.find('.toggle_district .fa-square-o').removeClass('fa-square-o').addClass('fa-check-square');
            } else {
                allowed_school_ids.splice(allowed_school_ids.indexOf(schoolCodeID), 1);
                dropdownItem.find('.fa-check-square').addClass('fa-square-o').removeClass('fa-check-square');
                $(ev.currentTarget).attr('aria-checked', 'false');

                // Well... We need to check if this is the last school code marked.
                // So, if that's the case, we need to remove its district code from
                // Allowed district codes :P
                if (!dropdownItem.closest('.dropdown-menu').find('.fa-check-square').length) {
                    districtDropdownItem.find('.fa-check-square').removeClass('fa-check-square').addClass('fa-square-o');
                    allowed_district_ids.splice(allowed_district_ids.indexOf(districtCodeID), 1);
                }
            }
            session.setSchoolCodes(
                current_district, allowed_district_ids,
                current_school, allowed_school_ids
            );
        },

    });

    if (session.display_switch_school_menu) {
        SystrayMenu.Items.push(SwitchSchoolMenu);
    }

    return SwitchSchoolMenu;

});
