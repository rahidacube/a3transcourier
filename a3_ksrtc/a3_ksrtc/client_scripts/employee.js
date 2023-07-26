frappe.ui.form.on('Employee', {
	user_id: function(frm) {

if (frm.doc.user_id){
    frappe.call({
        method: "a3_ksrtc.a3_ksrtc.doc_events.employee.get_warehouse",
        args:{
            "user": frm.doc.user_id
        },
        callback: (r)=>{
            console.log(r.message)
            cur_frm.set_value('warehouse',r.message.warehouse)
            refresh_field("warehouse")
        }
})
}
    }


})