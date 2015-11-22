#!/usr/bin/python

import logging
import os
import argparse
import MySQLdb
import MySQLdb.cursors

from ConfigParser import RawConfigParser
from influxdb import InfluxDBClient
from time_utils import get_epoch_from_datetime
from datetime import datetime
logger = logging.getLogger(__name__)


class Mysql2Influx:

    def __init__(self,config):

        #TODO put site info into settings file
        self._site_name = config.get('site_info','site_name')
        self._table = config.get('mysql','table')
        self._siteid_field = config.get('mysql','siteid_field')

        if config.has_option('mysql','time_field'):
            self._time_field = config.get('mysql','time_field')
        else:
            self._time_field = 'timestamp'
        #intitialise client for mysql database
        self._db_client = MySQLdb.connect ( config.get('mysql','host'),
                                            config.get('mysql','username'),
                                            config.get('mysql','password'),
                                            config.get('mysql','db'),
                                            cursorclass = MySQLdb.cursors.DictCursor
                                            )

        self._influx_client = InfluxDBClient(
                                            config.get('influx','host'),
                                            config.get('influx','port'),
                                            config.get('influx','username'),
                                            config.get('influx','password'),
                                            config.get('influx','db')
                                            )

        self._complete = False
        self._check_field = config.get('mysql','check_field')

    def transfer_data(self):
        self._get_data_from_mysql()

        self._update_rows()

        logger.debug('All data transfer  completed : %s '% self._complete)
        self._db_client.close()


    def _purge_data_in_db(self):
        """
        Once the data is configured and within influx we can pruge our database
        """
        if self._complete:
            query = "SELECT * FROM TABLE %s WHERE %s = 0 ORDER BY %s DESC"%(self._table, self._check_fields,self._time_field)


    def _get_data_from_mysql(self):
        """
        get the cursor to dump all the data from mysql
        """
        query = "SELECT * FROM `%s` WHERE `%s`=0 ORDER BY %s DESC"%(self._table,self._check_field,self._time_field)

        logger.debug('executing query %s '% query)
        cursor = self._db_client.cursor()
        cursor.execute(query)

        # pull data from mysql in X increments
        rows = cursor.fetchall()
        logger.info('querying MYSQL got %s rows'%len(rows))

        self._format_data(rows)


    def _send_data_to_influx(self,data_point):
        """
        Break up data to make sure in the format the inflxu like
        """
        logger.debug('Sending data to influx %s ...'%data_point[0])
        self._influx_client.write_points(data_point)


    def _format_data(self,data):

        #turn time into epoch timesa
        if data:
            logger.debug('Got data from mysql')
            for row in data:
                data_list =[]
                for key in row.keys():
                    #format date to epoch
                    epoch_time = row[self._time_field].isoformat()
                    if not isinstance(row[key],datetime):
                        data_point = {"measurement":key,
                                     "tags":{"site_name":row[self._siteid_field],
                                        "source": "wago"},
                                     "time" : "%sZ"%epoch_time,
                                   "fields" : {"value":row[key]}
                                    }
                        data_list.append(data_point)
                self._send_data_to_influx(data_list)
            self._complete = True

    def _update_rows(self):
        query = 'UPDATE %s SET %s=1  WHERE %s=0;'%(self._table,self._check_field,self._check_field)
        if self._complete:
           logger.debug('Updating rows : executing query %s '% query)
           c =  self._db_client.cursor()
           c.execute(query)
           self._db_client.commit()
def main():
    #Argument parsing
    parser = argparse.ArgumentParser(description = 'Get Time series data from MYSQL and push it to influxdb' )

    parser.add_argument( '-d', '--debug', help = 'set logging level to debug', action = 'store_true')
    parser.add_argument( '-c', '--config', help = 'config file location', nargs = 1, default = 'settings.ini' )

    args = parser.parse_args()


    # Init logging
    logging.basicConfig(level=(logging.DEBUG if True or args.debug else logging.INFO))

    logger.debug('Starting up with config file  %s' % (args.config))
    #get config file
    config = RawConfigParser()
    config.read(args.config)


    logger.debug('configs  %s' % (config.sections()))
    #start
    mclient = Mysql2Influx(config)
    mclient.transfer_data()


if __name__ == '__main__':
    #Check our config file
    main()
