odoo.define('awesome_tshirt.boolean_circle', function (require) {
    "use strict";

    var FieldBoolean = require('web.basic_fields').FieldBoolean;
    var registry = require('web.field_registry');

    var BooleanCircle = FieldBoolean.extend({
            _render: function () {
                var background_color;
                if (this.value) {
                    background_color = this.nodeOptions.true_color || 'red';
                } else {
                    background_color = this.nodeOptions.false_color || 'green';
                }
                var html = '<span class="o_status" role="img" name="' + this.name + '" style="background-color: ' + background_color + '"></span>';
                this.$el.html(html);
            }
        }
    );

    registry.add('boolean_circle', BooleanCircle);

    return BooleanCircle;

});

