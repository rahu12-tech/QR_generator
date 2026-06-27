#  QR Generator
# Description
a web application built with django that allows users to generate qr codes from urls.user can signin,login and manage their qr codes.

# Tech Stack
 Python
 Django
 Jinja2
 Bootstrap
 SQLite
 
## Features Completed 

## Authentication System
 User Signup
 User Login
 User Logout
 Google Login using Django Allauth
 Forgot Password functionality
Admin Panel Integration

### Admin Features
 View all users
 Change user passwords
 Block users (`is_active=False`)
 Delete users



## Packages Installed

```bash
pip install django
pip install django-allauth
pip install requests
pip install pyjwt
pip install qrcode[pil]
pip install pillow
pip install qrcode-artistic
pip install psycopg2-binary
```

## Database
SQLite (Default Django Database)

## Authentication Flow

```text
Signup
 
Login / Google Login
 
Dashboard
 
Logout
```
