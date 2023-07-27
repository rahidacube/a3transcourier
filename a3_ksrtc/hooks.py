from . import __version__ as app_version

app_name = "a3_ksrtc"
app_title = "A3 Ksrtc"
app_publisher = "Acube"
app_description = "Courier Service System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "nja@acube.co"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/a3_ksrtc/css/a3_ksrtc.css"
# app_include_js = "/assets/a3_ksrtc/js/a3_ksrtc.js"
# app_include_css ="/assets/a3_ksrtc/css/custom.css"

# include js, css files in header of web template
# web_include_css = "/assets/a3_ksrtc/css/a3_ksrtc.css"
# web_include_js = "/assets/a3_ksrtc/js/a3_ksrtc.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "a3_ksrtc/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "a3_ksrtc.install.before_install"
# after_install = "a3_ksrtc.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "a3_ksrtc.uninstall.before_uninstall"
# after_uninstall = "a3_ksrtc.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "a3_ksrtc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	 "Customer": {
		"after_insert":"a3_ksrtc.a3_ksrtc.doc_events.customer_events.after_insert",
		# "validate":"a3_kemdel.doc_events.customer_events.validate"
	},
	
    
	"Delivery Note":{
		"on_submit":"a3_ksrtc.a3_ksrtc.doc_events.delivery_note.on_submit"
	}
    
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
}
doctype_js = {
	"Stock Entry": "a3_ksrtc/client_scripts/stock_entry.js",
	"Delivery Note": "a3_ksrtc/client_scripts/delivery_note.js",
	"Warehouse": "a3_ksrtc/client_scripts/warehouse.js",
	"Employee": "a3_ksrtc/client_scripts/employee.js",
 }



fixtures = [

{'dt':"Role","filters":[
	['name',"in",
	["Station Operator","Ksrtc Sub Admin"]
	]
]},
  {"dt": "Custom DocPerm", "filters": [
            [
            "role", "in", [
                    "Station Operator","Ksrtc Sub Admin",
                   
                    "Guest"
    		       ]
                ]
  ]
            },
        ]
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"a3_ksrtc.tasks.all"
#	],
#	"daily": [
#		"a3_ksrtc.tasks.daily"
#	],
#	"hourly": [
#		"a3_ksrtc.tasks.hourly"
#	],
#	"weekly": [
#		"a3_ksrtc.tasks.weekly"
#	]
#	"monthly": [
#		"a3_ksrtc.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "a3_ksrtc.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "a3_ksrtc.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "a3_ksrtc.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["a3_ksrtc.utils.before_request"]
# after_request = ["a3_ksrtc.utils.after_request"]

# Job Events
# ----------
# before_job = ["a3_ksrtc.utils.before_job"]
# after_job = ["a3_ksrtc.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"a3_ksrtc.auth.validate"
# ]

