// Copyright (c) 2023, InshaSiS Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer', {
    enter_referred_code: function(frm) {
        if(frm.doc.enter_referred_code){
         frappe.db.get_list('Customer',{ 
         fields:['name'], 
         filters:{ 
             'referral_code':frm.doc.enter_referred_code 
         } 
         }).then(function(r){ 
             console.log(r); 
             if(r[0].name){
                 cur_frm.set_value("referred_by",r[0].name);
             }
         });   
             
         }
     },
    validate: function(frm) {
       if(!frm.doc.referral_code){
            var randomnum = Math.random().toString(36).substr(2,6).toUpperCase();
            frm.set_value("referral_code", randomnum);
            frm.set_df_property('referral_code',"read_only",1); 
        }
    },
    onload: function(frm) {
        if(frm.doc.referral_code){
            frm.set_df_property('referral_code',"read_only",1);           
        }
        if(frm.doc.enter_referred_code){
	        frm.set_df_property('enter_referred_code',"read_only",1);           
	    }
        
    },
    refresh: function(frm) {
        if (frappe.session.user == "Administrator") {

                frm.add_custom_button(__('Transfer Conis'), function() {
                    frappe.prompt([
                    {
                        label: 'Transaction Type',
                        fieldname: 'transaction_type',
                        fieldtype: 'Select',
                        options: ['','Debit','Credit'],
                        reqd:1
                    },
                    {
                        label: 'Transaction Method',
                        fieldname: 'transaction_method',
                        fieldtype: 'Select',
                        options: ['','Credit/Debit by Admin','Refer&Earn','Settle in Order'],
                        reqd:1
                    },
                    {
                        label: 'Transaction Coins',
                        fieldname: 'transaction_coins',
                        fieldtype: 'Int',
                        reqd:1
                    },
                ], (values) => {
                    // console.log(values.transaction_coins, values.transaction_method,values.transaction_type);
                    frappe.db.get_list('MAA Coins Wallet',{ 
                    fields:['name'], 
                    filters:{ 
                        'customer':frm.doc.name 
                    } 
                    }).then(function(r){ 
                        // console.log(r); 
                        
                        if(r[0].name){
                        
                        //Customer Wise Admin Cont Transfer
                        frappe.db.insert({
                                "doctype":"MAA Coins Transaction",
                                "coins_wallet":r[0].name,
                                "transaction_type":values.transaction_type,
                                "transaction_method":values.transaction_method,
                                "transaction_coins":values.transaction_coins
                            }).then(function(doc){
                                frappe.msgprint("Coins Inserted Successfully.");
                            });
                        }
                        
                    });
                });
                }).css({ 'background-color': 'darkblue', 'color': 'white' });
           
        }
    }
});

