odoo.define('awesome_tshirt.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var ChartWidget = require('awesome_tshirt.chart_widget');

    var DashboardAction = AbstractAction.extend({
        template: 't_shirt_dashboard_template',
        events: {
            "click .customers_btn": 'show_customers',
            "click .new_orders_btn": "show_new_orders",
            "click .cancelled_orders_btn": "show_cancelled_orders",
        },
        custom_events: {
            "chart_element_clicked": "show_orders_for_size"
        },
        start: function () {
            var self = this;
            return self._super.apply(arguments).then(function () {
                self._rpc({
                    route: '/awesome_tshirt/statistics'
                })
                    .then(self.render_statistics.bind(self))
                    .then(self.render_chart.bind(self));
            });

        },
        update_data: function () {
            var self = this;
            self._rpc({
                route: '/awesome_tshirt/statistics'
            })
                .then(self.render_statistics.bind(self))// Not part of the exercise, but might as well
                .then(function (statistics) {
                    self.chart_widget.set_data(statistics.orders_by_size);
                });

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
            return statistics;
        },
        render_chart: function (statistics) {
            this.chart_widget = new ChartWidget(this, statistics.orders_by_size);
            this.chart_widget.appendTo(this.$el);
        },
        on_attach_callback: function () {
            this.interval = setInterval(this.update_data.bind(this), 30 * 1000);
        },
        on_detach_callback: function () {
            clearInterval(this.interval);
        },
        show_orders_for_size: function (event) {
            var size = event.data.label;
            this.do_action({
                res_model: 'awesome_tshirt.order',
                name: 'Orders with size ' + size,
                views: [[false, 'list']],
                domain: [['size', '=', size]],
                type: 'ir.actions.act_window',
            });
        }
    });

    core.action_registry.add('awesome-tshirt.dashboard-action', DashboardAction);


    return DashboardAction;
});
