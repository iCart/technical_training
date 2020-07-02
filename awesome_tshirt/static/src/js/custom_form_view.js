odoo.define('awesome_tshirt.form_views', function (require) {
    "use strict";

    /**
     * This file defines a custom FormView for the model res.partner which adds a
     * 'Geolocate' button to the ControlPanel.
     */

    var core = require('web.core');
    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');

    var qweb = core.qweb;

    var CustomerFormController = FormController.extend({
        'renderButtons': function () {
            this._super.apply(this, arguments);

            this.$buttons.addClass('o_customer_form_buttons');
            this.$buttons.append($('<button type="button" class="btn btn-primary o_geolocate">Geolocate</button>'));
            this.$buttons.on('click', '.o_geolocate', this.geolocate.bind(this));
        },
        'geolocate': function () {
            var self = this;
            var res_id = this.model.get(this.handle, {raw: true}).res_id;
            this._rpc({
                'model': 'res.partner',
                'method': 'geo_localize',
                'args': [res_id]
            }).then(function () {
                self.reload();
            });
        }
    });

    var OrderFormController = FormController.extend({
        'renderButtons': function () {
            this._super.apply(this, arguments);

            this.$buttons.addClass('o_order_form_buttons');
            this.$buttons.append($('<button type="button" class="btn btn-primary o_print_label">Print Label</button>'));
            this.$buttons.on('click', '.o_print_label', _.debounce(this.print_label.bind(this), 300, true));
        },

        print_label: function () {
            var self = this;
            var res_id = this.model.get(this.handle, {raw: true}).res_id;
            this._rpc({
                'model': 'awesome_tshirt.order',
                'method': 'print_label',
                'args': [res_id]
            }).then(function (success) {
                if (success) {
                    self.displayNotification({
                        title: 'Printing Successful',
                        message: 'The label has been printed',
                        type: 'info',
                        sticky: false,
                    });
                } else {
                    self.displayNotification({
                        title: 'Printing Failed',
                        message: 'The label could not be printed',
                        type: 'warning',
                        sticky: true,
                    });
                }
                self.reload();
            });
        },
        _updateButtons: function () {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                var btn = this.$buttons.find('.o_print_label');
                var state = this.model.get(this.handle, {raw: true});

                btn.attr('disabled', (this.mode === 'edit' && !state.res_id));

                var printed = state.data.customer_id && state.data.state === 'printed';
                btn.toggleClass('btn-primary', printed);
                btn.toggleClass('btn-secondary', !printed);
            }
        },
    });

    var CustomerFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: CustomerFormController,
        })
    });

    var OrderFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: OrderFormController,
        })
    });

    viewRegistry.add('customer_form_view', CustomerFormView);
    viewRegistry.add('order_form_view', OrderFormView);

});