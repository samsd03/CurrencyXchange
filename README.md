# CurrencyXchange
ABOUT: This app is basically currency exchange app . User can add,update,convert and transfer currency. JWT token is used for authentication of user . Api of analytics have made in this app . User will get monthly transaction report via scheduling using celery beat .

ASSUMPTIONS: Api in this app is made for individual user and user_id will be passed through token .

SET UP PROCESS -

python3 and django3.0.5 is used .
install all packages using requirements.txt file given in root directory of project .
install rabbitmq server in your system for message queue .
Set email and password in environment variable and activate SMTP in your email id (key for Environment variable - user_email,email_password)
set secret key in environment variable (key - secret_key)
celery and rabbimq is used for scheduling of task and asynchronous task .
Use postman collection to see all apis given in the root folder(replace api key generated after login of user)