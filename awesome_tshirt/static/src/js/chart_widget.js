odoo.define('awesome_tshirt.chart_widget', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var ChartWidget = Widget.extend({
        template: 't_shirt_dashboard_chart',
        jsLibs: ['/awesome_tshirt/static/lib/chart.js/Chart.js'],
        init: function (parent, value_object) {
            this._super(parent);
            var self = this;
            self.keys = [];
            self.values = [];

            Object.entries(value_object).forEach(function ([key, value]) {
                self.keys.push(key.toUpperCase());
                self.values.push(value);
            });
        },
        start: function () {
            var self = this;
            self.ctx = self.$('.t-shirt-chart-area')[0].getContext('2d');
            self.chart = new Chart(self.ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: self.values,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                    }],
                    label: 'Sizes',
                    labels: self.keys,
                    borderwidth: 1,
                },
                options: {
                    responsive: false,
                }
            });
        },
        set_data: function (value_object) {
            var self = this;

            // Remove everything
            self.keys = [];
            self.values = [];
            // self.chart.data.datasets.pop();
            // while (self.chart.data.labels.length > 0) {
            //     self.chart.data.labels.pop();
            // }

            Object.entries(value_object).forEach(function ([key, value]) {
                self.keys.push(key.toUpperCase());
                self.values.push(value);
            });

            self.chart.data.datasets[0].data = self.values;
            self.chart.data.labels = self.keys;

            self.chart.update();
        }
    });

    return ChartWidget;
});
