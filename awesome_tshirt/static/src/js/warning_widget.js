odoo.define('awesome_tshirt.warning', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var Dialog = require('web.Dialog');

    /**
     * This originally was using a dialog, but
     */
    var WarningWidget = Widget.extend({
        init: function (parent, dataPoint) {
            this._super(parent);
            this.data = dataPoint.data;
        },
        start: function(){
            this._render();
        },
        /**
         * Called each time a field changes.
         *
         * @param {Object} record
         */
        updateState: function (record) {
            this.data = record.data;
            this._render();
        },
        _render: function () {
            // We could do it with templates and a bit of magic, but for now it is simple enough to do it this way
            var no_image = !this.data.image_url;
            var amount_above_100 = this.data.amount > 100;

            if (no_image || amount_above_100) {
                this.$el.html('<span><b>Warnings:</b></span><ul></ul>');
                if (no_image) {
                    this.$('ul').append('<li>No Image</li>');
                }
                if (amount_above_100) {
                    this.$('ul').append('<li>Add promotional material</li>');
                }
            } else {
                this.$el.html('');
            }
        }
    });

    widgetRegistry.add('t_shirt_warnings', WarningWidget);

    return WarningWidget;
});
