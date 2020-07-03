odoo.define('mail.systray.ActivityMenu', function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    var QuickOrderNavigation = Widget.extend({
        name: 'quick_order_navigation',
        template: 'awesome_tshirt.QuickOrderNavigation',
        events: {
            'change .quicknavigation_input': 'goto_order'
        },
        goto_order: function () {
            var order_id = parseInt(this.$('.quicknavigation_input').val());
            if (!_.isNaN(order_id)) {
                this.do_action({
                    res_model: 'awesome_tshirt.order',
                    name: 'Order',
                    views: [[false, 'form']],
                    res_id: order_id,
                    type: 'ir.actions.act_window',
                    target:  'new',
                });
            }
        },
    });

    SystrayMenu.Items.push(QuickOrderNavigation);

    return QuickOrderNavigation;

});
