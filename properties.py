###############################################################################
# Database Configurations
###############################################################################
database_host='localhost'       # Host
database_name='wfhx'            # Database Name
database_username='postgres'    # Username
database_password='password'    # Password
database_type='postgresql'      # 'postgresql' or 'mysql'(untested)
database_echo=True              # If True, DB operations will be printed to the console

###############################################################################
# Admin User Configuration
###############################################################################
admin_username = 'admin'        # Name of the admin Agent that is created on setup
admin_password = 'admin'        # Password of the admin Agent that is created on setup
admin_email = 'admin@wfhx.com'  # Email of the admin Agent that is created on setup

###############################################################################
# Session Configuration
###############################################################################
token_lifespan = 20             # Length of time since last use before a token expires in minutes
token_length = 16               # Number of bytes in the token
