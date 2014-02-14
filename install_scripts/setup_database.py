import sys
import os
import codecs

sys.path.append(".")
old_dir = os.getcwd()
os.chdir("../")

from TrendAnalyser import TrendAnalyser

TA = TrendAnalyser(load_db=False, load_api=False)
os.chdir(old_dir)


username = TA.conf['database_username']
password = TA.conf['database_password']
database = TA.conf['database_schema']

with open("db_creation_code.sql", "w") as f:
    f.write("CREATE USER '" + username + "'@'localhost' IDENTIFIED BY '" + password + "';")
    f.write("GRANT ALL PRIVILEGES ON *.* TO '" + username + "'@'localhost' WITH GRANT OPTION;")
    f.write("CREATE SCHEMA '" + database + "';")

    for db_files in os.listdir("../mysql_data/"):
        with open(os.path.join("../mysql_data", db_files)) as sql_file:
            for line in sql_file:
                f.write(line)

print "All database install code has been created and put under db_creation_code.sql"
print "Run this file as an appropriate mysql user (normally root) and it will set up the database"

