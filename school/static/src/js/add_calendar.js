odoo.define("school.add.calendar", function(require){
    "use strict";

    const CalendarRenderer = require('web.CalendarRenderer')
    const { FieldMany2Many } = require('web.relational_fields')
    // FieldMany2Many.include({
    //     _getRenderer() {
    //         const renderer = this._super(...arguments);
    //
    //         if (this.view.arch.tag === 'calendar') {
    //             return CalendarRenderer;
    //         }
    //
    //         return renderer
    //     }
    // })

});
