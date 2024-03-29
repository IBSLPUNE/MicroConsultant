from . import __version__ as app_version

app_name = "microconsultant"
app_title = "Microconsultant"
app_publisher = "IBSL"
app_description = "Development For Microconsultant By IBSL"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shantanu@frappe.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/microconsultant/css/microconsultant.css"
# app_include_js = "/assets/microconsultant/js/microconsultant.js"

# include js, css files in header of web template
# web_include_css = "/assets/microconsultant/css/microconsultant.css"
# web_include_js = "/assets/microconsultant/js/microconsultant.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "microconsultant/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Production Plan" : "public/js/production_plan.js"}
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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "microconsultant.utils.jinja_methods",
# 	"filters": "microconsultant.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "microconsultant.install.before_install"
# after_install = "microconsultant.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "microconsultant.uninstall.before_uninstall"
# after_uninstall = "microconsultant.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "microconsultant.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
 	"Production Plan": {
 		"before_save": "microconsultant.microconsultant.rfq_development.add_items",
 	},
  "Request for Quotation": {
    "after_insert": "microconsultant.microconsultant.rfq_development.rfq_items",
    },
  "Work Order": {
    "before_submit": "microconsultant.microconsultant.wo_alt.alt_items"
    },
    "Supplier Quotation": {
    "before_save": "microconsultant.microconsultant.supplier_quotation.filter_items",
    },
    "Stock Entry": {
     "before_save":"microconsultant.microconsultant.wo_alt.stock_entry"
    }
  }



# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"microconsultant.tasks.all"
# 	],
# 	"daily": [
# 		"microconsultant.tasks.daily"
# 	],
# 	"hourly": [
# 		"microconsultant.tasks.hourly"
# 	],
# 	"weekly": [
# 		"microconsultant.tasks.weekly"
# 	],
# 	"monthly": [
# 		"microconsultant.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "microconsultant.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "microconsultant.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "microconsultant.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"microconsultant.auth.validate"
# ]

