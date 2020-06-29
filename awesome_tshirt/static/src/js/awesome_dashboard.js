odoo.define('awesome_tshirt.dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var Counter = require('awesome_tshirt.counter');

    var DashboardAction = AbstractAction.extend({
        hasControlPanel: true,
        start: function () {
            var self = this;
            return this._super.apply(arguments).then(function () {
                var counter = new Counter(this, 4);
                counter.appendTo(self.$('.o_content'));
            });
        }
    });

    core.action_registry.add('awesome-tshirt-dashboard-action', DashboardAction);


    return DashboardAction;
});
