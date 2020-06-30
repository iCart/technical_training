odoo.define('awesome_tshirt.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var DashboardAction = AbstractAction.extend({
        template: 't_shirt_dashboard_template',
        events: {
            "click .customers_btn": 'show_customers',
            "click .new_orders_btn": "show_new_orders",
            "click .cancelled_orders_btn": "show_cancelled_orders",
        },
        start: function () {
            this._rpc({
                route: '/awesome_tshirt/statistics'
            }).then(this.render_statistics.bind(this));
        },
        show_customers: function () {
            this.do_action({
                res_model: 'res.partner',
                name: 'View Customers',
                views: [[false, 'kanban']],
                type: 'ir.actions.act_window',
            });
        },
        show_new_orders: function () {
            var one_week_ago = new Date();
            one_week_ago.setDate(one_week_ago.getDate() - 7);
            this.do_action({
                res_model: 'awesome_tshirt.order',
                name: 'New Orders',
                views: [[false, 'list']],
                domain: [['create_date', '>', one_week_ago]],
                type: 'ir.actions.act_window',
            });
        },
        show_cancelled_orders: function () {
            var one_week_ago = new Date();
            one_week_ago.setDate(one_week_ago.getDate() - 7);
            this.do_action({
                res_model: 'awesome_tshirt.order',
                name: 'Recent Cancelled Orders',
                views: [[false, 'list']],
                domain: [['create_date', '>', one_week_ago], ['state', '=', 'cancelled']],
                type: 'ir.actions.act_window',
            });
        },
        render_statistics: function (statistics) {
            this.$('.new_orders_field').text(statistics.nb_new_orders);
            this.$('.total_orders_field').text(statistics.total_amount);
            this.$('.avg_amount_field').text(statistics.average_quantity);
            this.$('.cancelled_orders_field').text(statistics.nb_cancelled_orders);
            this.$('.avg_processing_time_field').text(statistics.average_time);

        }
    });

    core.action_registry.add('awesome-tshirt-dashboard-action', DashboardAction);


    return DashboardAction;
});
