odoo.define('school.custom.widget', require => {
    "use strict";

    const {_t} = require('web.core');
    const field_registry = require('web.field_registry');
    const FieldMany2ManyTags = field_registry.get('many2many_tags')
    const dialogs = require('web.view_dialogs');
    // const FieldMany2ManyTags = form_widget_registry.get('many2many_tags');

    const ClickableMany2manyTags = FieldMany2ManyTags.extend({

        init(parent, name, record, options) {
            this._super(...arguments);
            this.operations = [];
            this.isReadonly = this.mode === 'readonly';
            this.view = this.attrs.views[this.attrs.mode];
            this.isMany2Many = this.field.type === 'many2many' || this.attrs.widget === 'many2many';
            this.activeActions = {};
            this.recordParams = {fieldName: this.name, viewType: this.viewType};
            const arch = this.view && this.view.arch;
            if (arch) {
                this.activeActions.create = arch.attrs.create ?
                    !!JSON.parse(arch.attrs.create) :
                    true;
                this.activeActions.delete = arch.attrs.delete ?
                    !!JSON.parse(arch.attrs.delete) :
                    true;
                this.editable = arch.attrs.editable;
            }
        },

        get_badge_id: function (el) {
            if ($(el).hasClass('badge')) return $(el).data('id');
            return $(el).closest('.badge').data('id');
        },
        events: _.extend({}, FieldMany2ManyTags.prototype.events, {
            'click .badge': function (e) {
                e.stopPropagation();
                const record_id = this.get_badge_id(e.target);
                const recordParams = {fieldName: this.name, viewType: this.viewType};
                const context = this.record.getContext(recordParams);
                // this._rpc({
                //     model: this.field.relation,
                //     method: 'get_formview_action',
                //     args: [[record_id]],
                //     context: this.record.getContext(recordParams),
                // }).then(function (action) {
                //     this.trigger_up('do_action', {action: action});
                // });

                var onSaved = record => {
                    if (_.some(this.value.data, {id: record.id})) {
                        // the record already exists in the relation, so trigger an
                        // empty 'UPDATE' operation when the user clicks on 'Save' in
                        // the dialog, to notify the main record that a subrecord of
                        // this relational field has changed (those changes will be
                        // already stored on that subrecord, thanks to the 'Save').
                        this._setValue({operation: 'UPDATE', id: record.id});
                    } else {
                        // the record isn't in the relation yet, so add it ; this can
                        // happen if the user clicks on 'Save & New' in the dialog (the
                        // opened record will be updated, and other records will be
                        // created)
                        this._setValue({operation: 'ADD', id: record.id});
                    }
                };

                new dialogs.FormViewDialog(this, {
                    context: context,
                    domain: this.record.getDomain(this.recordParams),
                    on_saved: onSaved,
                    on_remove:  () => {
                        this._setValue({operation: 'DELETE', ids: [id]});
                    },
                    readonly: this.mode === 'readonly',
                    deletable: this.activeActions.delete && params.deletable,
                    res_id: record_id,
                    res_model: this.field.relation,
                    shouldSaveLocally: true,
                }).open();
                // this.do_action({
                //     name: _t('Edit hour range'),
                //     type: 'ir.actions.act_window',
                //     res_model: this.field.relation,
                //     target: 'new',
                //     res_id: record_id,
                //     views: [[false, 'form']],
                //     flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
                // })
            }
        })
    });
    field_registry.add('many2many_tags_clickable', ClickableMany2manyTags);

    return {
        ClickableMany2manyTags
    };

});