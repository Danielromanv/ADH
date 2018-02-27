import os
import datetime
import pymongo as mon

dbhost = 'mongodb://mongodb:27017'
def DB_check(dbhost):
    client = mon.MongoClient(dbhost, connect = False)
    try:
        client.admin.command("ismaster")
    except mon.errors.ConnectionFailure as e:
        print (e)
        return 0

client = mon.MongoClient(dbhost)
db = client.db
hosts = db.hosts

def DB_add(hosts,host_name,client_host,client_ip):
    d = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    D = datetime.datetime.strptime(d,"%d-%m-%Y %H:%M:%S")
    hosts.insert_one({"host_name":host_name,"client_host":client_host,"client_ip":client_ip,"date":D })
def DB_find(hosts,name):
    if (name == ''):
        return hosts.find({}).sort("date",mon.DESCENDING)
    else:
        return hosts.find({'host_name': {'$regex':'.*'+name+'.*'}}).sort("date",mon.DESCENDING)

client.close()
