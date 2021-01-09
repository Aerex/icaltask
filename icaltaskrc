[general]
# The default calendar to send tasks to
default_calendar = 

log.level = 
log.file = 

# The  method to retrieve credentials for authentication. The available methods are listed below
# `command` - Get credentials through a command
# `plain` - Get password from plain text 
# The type of authentication. Either digest or basic 
auth_type = digest


# The username / password for authenticate for calendar if not specified on calendar
# Use `password.eval` and `username.eval` to retrieve credentials from a script
username = user  
password.eval = pass calendar/default | head -n 1

[work]
# Authentication credentials for work calendar
url = https://icaltask.com/calendars/work
username = user 
password.eval = pass calendar/work | head -n 1
