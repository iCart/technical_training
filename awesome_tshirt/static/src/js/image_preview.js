odoo.define('awesome_tshirt.image_preview', function (require) {
    "use strict";

    var FieldChar = require('web.basic_fields').FieldChar;
    var fieldRegistry = require('web.field_registry');


    var ImagePreview = FieldChar.extend({
        _renderReadonly: function () {
            this.$el = $('<img class="img img-fluid" alt="T-shirt Image" src="' + this.value + '" border="1">');
        },
    });

    fieldRegistry.add('image_preview', ImagePreview);

    return ImagePreview;
})
;
