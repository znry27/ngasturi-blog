odoo.define('tutorial_javascript.widget_one', function (require) {
"use strict";
    // import object yang dibutuhkan untuk membuat sebuah widget
    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');

    // buat sebuah object dengan nama bebas
    // jangan lupa untuk extend ke object web.AbstractField atau object turunanya
    var WidgetOne = AbstractField.extend({
        template: 'WidgetOneTemplate', // isi nama template yang telah dibuat untuk mengatur tampilan/view widget
    });

    // daftarkan widget yang telah kita buat ke web.field_registry
    // agar kita bisa menggunakan widget yang kita buat di file xml/view odoo 
    // dengan kode seperti di bawah ini
    // <field name="field_one" widget="widget_one" />
    // nama 'widget_one' ini bebas, asal selalu nyambung/tanpa spasi
    FieldRegistry.add('widget_one', WidgetOne);

    // return object widget yang telah kita buat
    // agar bisa di-extend atau di-override oleh module lain
    return WidgetOne;

});