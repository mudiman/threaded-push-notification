import os


sender="info@company.com"

TOTAL_COMPLETED=0
OLD_TOTAL=0

EMAIL_PASSWORD="altair0"
EMAIL_ADDRESS="mudassar@company.com"
TEST_DEVICE_ID="e8ea30f633801af9b1a4a8bde7756cfe62d2379a07749ac1607856eab122bc14"
#PEM_FILE_PATH=os.path.join(os.path.realpath(os.path.dirname(__file__)),"companyOfficePushPem.pem")
#PEM_FILE_PATH=os.path.join(os.path.realpath(os.path.dirname(__file__)),"apns-production-nopass.pem")
PEM_FILE_PATH=os.path.join(os.path.realpath(os.path.dirname(__file__)),"apns-production.pem")
TEST_PEM_FILE_PATH=os.path.join(os.path.realpath(os.path.dirname(__file__)),"officeFlikkablePem.pem")

COMMAND_PATH=os.path.join(os.path.realpath(os.path.dirname(__file__)),"command")

NOTIFICATION_LOG_PATH="notification.log"

THREAD_POOL_SIZE=100



# server
# receivers=["mudassar@company.com","talib@company.com"]
# database=dict(host="127.0.0.1",username="root",password="",database="db_company")
# PROGRESS_LOG="/var/www/html/companyapps/progress/progress_notification"
# MY_SQL_RESET_COMMAND="sudo /etc/init.d/mysqld restart"

# local
receivers=["mudassar@company.com"]
database=dict(host="127.0.0.1",username="company",password="company123",database="db_company")
PROGRESS_LOG=os.path.join(os.path.realpath(os.path.dirname(__file__)),"progress_notification")
MY_SQL_RESET_COMMAND="sudo /etc/init.d/mysql restart"
