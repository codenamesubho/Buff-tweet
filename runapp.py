import argparse
import os
from bufftweet.bufftweet import Tweetdaemon
from daemon import runner
from bufftweet.register import RegisterUser

usage="""
python runapp.py start [-t]
python runapp.py stop|restart|regsiter|showall|store
python runapp.py post [-p <post>]
python runapp.py del [-id <id> | -p <post>]
python runapp.py [-h]
"""


def main():
    parser = argparse.ArgumentParser(description="""Buff_tweet is used to buffer your tweets [options]""",usage=usage)
    parser.add_argument('-t', '--time', type=str, default='60', help="set time interval")
    parser.add_argument('command',help="start|stop|restart|register|store|showall|del|post")
    parser.add_argument('-p','--post',type=str,help="status to be posted")
    parser.add_argument('-id',type=int,help="status to be posted")
    args = parser.parse_args()

    if args.command in ['start','stop','restart']:
        if args.time:
            app = Tweetdaemon(time=eval(args.time))
        else:
            app = Tweetdaemon()
        app.initialize()
        app.safe_close_db()
        daemon_runner = runner.DaemonRunner(app)
        #This ensures that the logger file handle does not get closed during daemonization
        daemon_runner.daemon_context.files_preserve=[file('/var/tmp/bufftweet.log', 'a')]
        daemon_runner.do_action()
    
    elif args.command=='register':
        r_obj = RegisterUser()
        r_obj.register()
        
    elif args.command=='post':
        if args.post:
            app = Tweetdaemon()
            app.initialize()
            app.API.post(args.post)
        else:
            print "usage: python runapp.py post -p <your post>"
    elif args.command=='store':
        app = Tweetdaemon()
        app.initialize()
        app.DB.store_tweet()

    elif args.command=='showall':
        app = Tweetdaemon()
        app.initialize()
        app.DB.buff_disp()
    
    elif args.command=='del':
        app = Tweetdaemon()
        app.initialize()
        if args.id:
            app.DB.del_post(id=args.id)
        elif args.post:
            app.DB.del_post(tweet=args.post)
    else:
        parser.print_help()



if __name__=='__main__':
    
    main()
    


    #main()#user=raw_input("enter your name: ")
    #ip='y'
    
    
    #print user,auth_key,auth_sec,con_key,con_secret
    #dbname=add_to_buffer(user)
    #print dbname
    