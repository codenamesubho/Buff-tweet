import tweepy
from ipdb import set_trace
from os import path
import os
import webbrowser 
import sqlite3
import datetime
import argparse

def add_to_buffer(user):

	tweeter = raw_input("enter your tweet: ")

	date=datetime.date.today().strftime("%d %m %Y")
	time=datetime.datetime.now().time().strftime("%H %M %S")
	buffer_path='dbase/'+user+'_buff.db'
	
	conn = sqlite3.connect(buffer_path)
	c = conn.cursor()
	#set_trace()	
	# Insert a row of data
	c.execute("INSERT INTO tweets VALUES (null,?,?,?)",(tweeter,date,time))
	
	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	return buffer_path
	## If it doesn't, we will create one.


def get_last():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	

	t = (1,)
	c.execute('SELECT * FROM tweets WHERE Id=?', t)
	print c.fetchone()

def del_post():
	c.execute('DELETE FROM tweets WHERE Id=?',t)

	conn.commit()
	c.execute('SELECT * FROM tweets')
	print c.fetchall()
	conn.close()

def post():
	
	updater()

def getuser():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	
	t='1'
	c.execute('SELECT author FROM credentials WHERE Id=?',t)
	for row in c.fetchone():
		return row
	#print b

def get_cred():
	conn = sqlite3.connect('dbase/cred.db')
	c = conn.cursor()
	
	t='1'
	c.execute('SELECT author,consumer_key,consumer_secret,auth_key,auth_secret FROM credentials WHERE Id=?',t)
	for user,con_key,con_secret,auth_key,auth_sec in c.fetchmany():
		return user,con_key,con_secret,auth_key,auth_sec


def login(consumer_key,consumer_secret,auth_key,auth_secret):
	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(auth_key,auth_secret)
	api=tweepy.API(auth)
	print "Authenticated!!"
	update=raw_input("tweet please: ")
	if(bool(api.update_status(update))):
		print "Status updated successfully!!!"

#def updater(api):
	
def buff_disp():
	conn = sqlite3.connect('dbase/subho_buff.db')
	c = conn.cursor()
	
	t=('1',)
	c.execute('SELECT * FROM tweets')
	print c.fetchall()
	conn.close()

def main():
	
	parser = argparse.ArgumentParser(prog='Buff_tweet',usage='%(prog)s is used to buffer your tweets [options]')
	parser.add_argument('--p', post='post tweet')
	args = parser.parse_args()







if __name__=='__main__':
	
	'''main()#user=raw_input("enter your name: ")
	#ip='y'
	
	#buff_disp()
	'''
	user,con_key,con_secret,auth_key,auth_sec=get_cred()
	user=user.encode("utf-8")
	auth_key=auth_key.encode("utf-8")
	auth_sec=auth_sec.encode("utf-8")
	con_key=con_key.encode("utf-8")
	con_secret==con_secret.encode("utf-8")
	#print user,auth_key,auth_sec,con_key,con_secret
	#dbname=add_to_buffer(user)
	#print dbname
	buff_disp()
	


	login(con_key,con_secret,auth_key,auth_sec)
	
	'''while(ip!='n'):
		add_to_buffer(user)
	ip=raw_input("enter your tweet, enter 'n' to stop adding to buffer :")
	'''		