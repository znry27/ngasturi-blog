odoo.define('tutorial_javascript.widget_one', function (require) {
"use strict";
    // import object yang dibutuhkan untuk membuat sebuah widget
    var AbstractField = require('web.AbstractField');
    var FieldRegistry = require('web.field_registry');
    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var view_dialogs = require('web.view_dialogs');

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
            'click .btn-dollar': 'btn_dollar_action', // tambahan di seri bagian 4
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
        btn_dollar_action: function(){
            var self = this;
            // Dialog.alert(
            //     this,
            //     "Apakah anda yakin ingin mengisi field ini dengan nilai 0 ?",
            //     {
            //         onForceClose: function(){
            //             console.log("User menutup dialog dengan paksa, dengan cara melakukan klik pada tombol dengan icon close");
            //         },
            //         confirm_callback: function(){
            //             console.log("User melakukan klik pada tombol OK");
            //             self._setValue("0");
            //         }
            //     }
            // );    

            // Dialog.confirm(
            //     this,
            //     "Apakah anda yakin ingin mengisi field ini dengan nilai 1000 ?",
            //     {
            //         onForceClose: function(){
            //             console.log("User menutup dialog dengan paksa, dengan cara melakukan klik pada tombol dengan icon close");
            //         },
            //         confirm_callback: function(){
            //             console.log("User melakukan klik pada tombol OK");
            //             self._setValue("1000");
            //         },
            //         cancel_callback: function(){
            //             console.log("User melakukan klik pada tombol Cancel");
            //         }
            //     }
            // );   

            // new view_dialogs.FormViewDialog(this, {
            //     res_model: 'sale.order', // nama model           
            //     res_id: 1, // primary key dari model yang ingin kita tampilkan datanya
            //     title: "Sale Order dengan ID 1", // judul, optional
            //     on_saved: function (record) { // aksi saat user melakukan tombol save
            //         console.log("User melakukan klik pada tombol Save");
            //     }
            // }).open();

            new view_dialogs.SelectCreateDialog(this, {
                res_model: 'sale.order', // nama model      
                title: "Pilih Sale Order", // judul, optional
                domain: [['state','!=', 'draft']], // domain untuk membatasi record yang bisa dipilih, optional
                no_create: true, // opsi agar user tidak bisa create record baru, optional
                on_selected: function (records) {
                    var record_ids = records.map(function(item){
                        return item['id'];
                    });
                    self._rpc({
                        model: self.attrs.relatedModel,
                        method: self.attrs.modifiers.relatedAction,
                        args: [record_ids,0,0],
                        kwargs: {value_3: 0, value_4: 0}                
                    }).then(function(result){
                        self._setValue(result.toString());
                    });   
                }
            }).open();      
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