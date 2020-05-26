from subprocess import call

call(["sqoop", "import-all-tables", "--connect", "jdbc:mysql://quickstart.cloudera:3306/iot_database", "--username", "root", "--password", "cloudera", "-m", "1"])