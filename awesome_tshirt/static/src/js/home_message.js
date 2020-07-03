odoo.define('awesome_tshirt.home_message', function (require) {
    "use strict";

    var HomeMenu = require('web_enterprise.HomeMenu');
    var core = require('web.core');
    var session = require('web.session');

    var QWeb = core.qweb;

    HomeMenu.include({
        start: function () {
            var self = this;
            var message = session.message;
            console.log(session);
            console.log(session.message);
            return self._super.apply(self, arguments).then(function () {
                $(QWeb.render('awesome_tshirt.home_message', {message: message})).insertBefore(self.$mainContent);
            });
        },
    });
});