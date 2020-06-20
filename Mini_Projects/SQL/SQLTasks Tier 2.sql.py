#!/usr/bin/env python
# coding: utf-8

# In[30]:


#load python packages
import os

os.getcwd()


# In[31]:


import sqlite3
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
 
    return conn
 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT *
        FROM FACILITIES
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
        
def get_total_revenue(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT sum( new.cost ) AS total_revenue, new.fname AS facility
            FROM (
                SELECT f.facid AS id, f.name AS fname, b.slots AS slot, 
                CASE WHEN b.memid =0
                THEN (
                b.slots * f.guestcost
                )
                WHEN b.memid >0
                THEN (
                b.slots * f.membercost
                )
                END AS cost
                FROM `Bookings` AS b
                LEFT JOIN `Facilities` AS f ON b.facid = f.facid
            ) AS new
        GROUP BY new.id
        HAVING total_revenue <1000
        ORDER BY total_revenue DESC
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def get_Recommenders(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT a.surname || ', ' || a.firstname  AS member, (
            SELECT surname || ', ' || firstname  
            FROM `Members` 
            WHERE memid = a.recommendedby
            ) AS recommendedby
        FROM `Members` AS a
        WHERE memid <>0
        ORDER BY a.surname, a.firstname

        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def get_FacUsage(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
       SELECT f.name, sum( b.slots ) 
            FROM `Facilities` AS f
        INNER JOIN `Bookings` AS b
            USING ( facid ) 
            WHERE b.memid <>0
            GROUP BY f.facid
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)  

def get_FacUsageByMonth(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
       SELECT f.name, sum( b.slots ), strftime('%m', starttime)  
        FROM `Facilities` AS f
                INNER JOIN `Bookings` AS b
        USING ( facid ) 
        WHERE b.memid <>0
        GROUP BY f.facid, strftime('%m', starttime)
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)  

        
def main():
    database = "sqlite\db\pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        select_all_tasks(conn)
        print("3. Get Total Revenue")
        get_total_revenue(conn)
        print("4. Get Member by Recommender Name")
        get_Recommenders(conn)
        print("5. Get Facility Usage for Members")
        get_FacUsage(conn)
        print("6. Get Facility Usage for Members By Month")
        get_FacUsageByMonth(conn)
        
if __name__ == '__main__':
    main()


# In[ ]:




