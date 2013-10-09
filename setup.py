#! /usr/bin/env python
from os import path
import os
import sqlite3
import webbrowser
import tweepy


def authenticate(consumer_key,consumer_secret):	
	'''t=1
	c.execute('SELECT * FROM tweets WHERE Id=?', t)
	print c.fetchone()'''

	print "Authenticating...."

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
		print 'Error! Failed to get request token.'
	
	savout = os.dup(1)
	os.close(1)
	os.open(os.devnull, os.O_RDWR)
	try:
		webbrowser.open_new(redirect_url)
	finally:
		os.dup2(savout, 1)

	verifier = raw_input("Verifier: ")

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print 'Error! Failed to get access token.'
		
	auth_key=auth.access_token.key
	auth_secret=auth.access_token.secret
	
	return auth_key,auth_secret
		


def create_cred():
	if not path.isfile('dbase/cred.db'):

		print "Buff_Tweet is being setup for the first time .....\n"
		os.mkdir("dbase")
		conn = sqlite3.connect('dbase/cred.db')
		
		c=conn.cursor()
		c.execute('''CREATE TABLE credentials(Id INTEGER PRIMARY KEY,author text,consumer_key Text,consumer_secret Text,auth_key Text, auth_secret Text,tweet_counter INT)''')
		conn.close()	
		
		


	conn = sqlite3.connect('dbase/cred.db')
	
	c = conn.cursor()

	# Create table
	print "Setting up Buff_tweet for a new user..."
	
	
	print "Opening browser.... please provide the required credentials:-"
	
	author= raw_input("enter your name: ")

	savout = os.dup(1)
	os.close(1)
	os.open(os.devnull, os.O_RDWR)
	try:
   		webbrowser.open_new("https://dev.twitter.com/apps")
	finally:
   		os.dup2(savout, 1)

   	
	con_key=raw_input("enter consumer key: ")
	con_secret= raw_input("enter consumer secret: ")
	
	auth_key,auth_secret=authenticate(con_key,con_secret)

	c.execute("INSERT INTO credentials VALUES (null,?,?,?,?,?,?)",(author,con_key,con_secret,auth_key,auth_secret,0))
	
	buffer_path='dbase/buff.db'
	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	return buffer_path



def create_buffer(buffer_path):

	
	conn = sqlite3.connect(buffer_path)
	c = conn.cursor()
	
	print "Creating your buffer....\nPlease wait...."
	# Create table
	c.execute('''CREATE TABLE tweets(Id INTEGER PRIMARY KEY,tweet text,Date_ Text,Time Text)''')
	c.execute("INSERT INTO tweets VALUES (null,?,?,?)",("hello, this is my 1st tweet using Buff_tweet","01 01 2001","2 23 13"))
	# Insert a row of data
#	c.execute("INSERT INTO tweet VALUES (1,tweeter,date,)")
	
	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	



if __name__=='__main__':
	buffer_path=create_cred()
#	buffer_path='dbase/subho_buff.db'
	if not path.isfile(buffer_path):
		create_buffer(buffer_path)
	print("Setup Complete!!! Now you can run bufftweet.py. Enjoy...!!!")