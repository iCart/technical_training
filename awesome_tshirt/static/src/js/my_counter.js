odoo.define('awesome_tshirt.counter', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var Counter = Widget.extend({
        template: 'counter_template',
        events: {
            'click .decrement_btn': '_onDecrement',
            'click .increment_btn': '_onIncrement',
        },
        init: function(parent, value){
            this._super(parent);
            this.count = value;
        },
        _onDecrement: function(){
            this.count -= 1;
            this.$('.val').text(this.count);
        },
        _onIncrement: function(){
            this.count += 1;
            this.$('.val').text(this.count);
        }
    });

    return Counter;
});
