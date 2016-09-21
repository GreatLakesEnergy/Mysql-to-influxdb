# Mysql-to-influxdb
Quick hack to get data from MySQL into influx db to display with Graphite and Grafana. This is a quick script I created for a very specific use case so it <b>won't</b> copy your whole database over magically. If you need this you can modify the script to fit your needs.

This script will meant to run constantly or one time and send data from a single table in MYSQL to influx. If you have multiple tables this will be an issue. Also it requires that the MYSQL table is altered to have a specific column which indicates whether this piece of data has been copied to influx already or not.

# Config
This script needs a config file to run simply create config file.  Below is a samle config file for settings.ini

    
    [mysql]
    host : mysql_server_hostname
    port : mysql_server_port # Default is3306
    username : mysql_user_name
    password : mysql_user_password
    db : mysql_database
    table : mysql_table
    check_field : column_to_check_if_data_has_been_transferred
    time_field : colum_that_contains_timestam_in_table
    siteid_field : column_which_contains_site_id_tag
    
    
    [influx]
    host : localhost
    port : 8086
    username : influx_username
    password : influx_pass
    db : sesh
    
    [server]
    interval : 5 
    
    [site_info]
    site_name : tag_name_to_append_to_all_data_going_into_influx
# Usage
first run
    ```pip install -r requirements.txt```
then
    ```python mysql2influx.py -d -c settings.ini -s```
    
This will run the script  as a server in debug mode



