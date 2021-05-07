odoo.define('tutorial_javascript.widget_one', function (require) {
"use strict";
    // import object yang dibutuhkan untuk membuat sebuah widget
    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');
    var field_utils = require('web.field_utils');

    // import qweb untuk merender view
    var core = require('web.core');
    var qweb = core.qweb;

    // buat sebuah object dengan nama bebas
    // jangan lupa untuk extend ke object web.AbstractField atau object turunanya
    var WidgetOne = AbstractField.extend({
        step: 1, // nilai default, jika user tidak mengaturnya di file xml
        template: 'WidgetOneTemplate', // isi nama template yang telah dibuat untuk mengatur tampilan/view widget
        events: { // daftar event, mirip event di jquery
            'click .btn-minus': 'btn_minus_action',
            'click .btn-plus': 'btn_plus_action',
        },
        init: function () {
            // method 'init' dipanggil pertama kali saat widget digunakan
            this._super.apply(this, arguments);
            if(this.nodeOptions.step){
                // jika user mengatur nilai step di file xml
                // ubah nilai step agar sesuai yang diinput user
                this.step = this.nodeOptions.step;
            }
        },
        btn_minus_action: function(){
            var new_value = this.value - this.step;
            this._setValue(new_value.toString());            
        },
        btn_plus_action: function(){
            console.log(this);
            var new_value = this.value + this.step;
            this._setValue(new_value.toString());
        },
        _render: function () {
            // render ulang jika nilai dari field berubah
            // format value agar tampilannya ada pemisah ribuan
            var self = this;
            var formated_value = field_utils.format[this.formatType](this.value);
            this.$el.html($(qweb.render(this.template, {'widget': this, 'formated_value': formated_value})));
            this.$el.find('.btn-copy').click(function(){
                // kita juga bisa menggunakan kode
                // self.$el.find('input').val();
                // jika kita ingin mendapatkan value dari field one menggunakan jquery
                // dengan cara mengakses element widget
                var field_one_val = self.value;
                var field_two_val = $('[name=field_two]').val();
                var field_three_val = field_one_val + parseInt(field_two_val);
                self.trigger_up('field_changed', {
                    dataPointID: self.dataPointID,
                    viewType: self.viewType,
                    changes: {'field_three': field_three_val},
                });
            });
        },
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