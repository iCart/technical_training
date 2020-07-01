odoo.define('awesome_tshirt.image_preview', function (require) {
    "use strict";

    var FieldChar = require('web.basic_fields').FieldChar;
    var fieldRegistry = require('web.field_registry');


    var ImagePreview = FieldChar.extend({
        /**
         * @override
         * @returns {boolean}
         */
        isSet: function () {
            return true;
        },
        _renderReadonly: function () {
            if (this.value) {
                this.$el.empty().append($('<img class="img img-fluid" alt="T-shirt Image" src="' + this.value + '" border="1">'));
            } else {
                this.$el.text('MISSING TSHIRT DESIGN').css('color', 'red').css('font-weight', 'bold');
            }
        },
    });

    fieldRegistry.add('image_preview', ImagePreview);

    return ImagePreview;
})
;
