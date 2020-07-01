odoo.define('awesome_tshirt.boolean_circle', function (require) {
    "use strict";

    var FieldBoolean = require('web.basic_fields').FieldBoolean;


    FieldBoolean.include({
            _render: function () {
                console.log('Calling FieldBoolean render')
                var status_class;
                if (this.value) {
                    status_class = 'o_status o_status_red';
                } else {
                    status_class = "o_status o_status_green";
                }
                var html = '<span class="' + status_class + '" role="img" name="' + this.name + '"></span>';
                this.$el.html(html);
            }
        }
    );

});

