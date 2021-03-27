I'm contacting with email to Dennis from admin of hopper, and following is the process of communication. I believe connection issue would solve soon.

from Dennis:

I am thinking that this is a coding error. The database is definitely there and I can log into the server using the credentials from your email. Can you point me to the file you are using to connect to it, and I will take a look to see if I can figure out where you went wrong? I make no promises since I have not programmatically connected to databases all that often.
-Dennis

Dennis Thomas
Linux System Administrator
Math & Statistics and Computer Science Departments
Research Technology Group
Saint Louis University
dennis.thomas@health.slu.edu

---

Dennis,

I'm quite glad for you to help me check, and all codes are hosted at https://github.com/jackzhenguo/wordfinder/tree/remote-database. The module is named store.py at src/train directory.

Thank you so much for your kind help.

---

Zhen, 

Quick question, you are trying to run this code on hopper, right?


--- 



Dennis, 

Sorry to reply late. I'm running code on my local computer and I guess this is probable reason that I couldn't connect to database by local computer. 


Plus, running codes normally on hopper require many third-party packages, like pymysql, but it showed the problem following(first to show I don't have rights, suggesting me to add --user, but after adding it still fails ) when I installed pymysql.

we also need to install the following list, you can put them to requirements.txt then execute pip install -r requirements.txt. Thank you so much.

click==7.1.2
Flask==1.1.2
flask-mysqldb==0.2.0
gunicorn==20.0.4
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
mysql==0.0.2
mysqlclient==2.0.1
Werkzeug==1.0.1
mysql-connector-python

---



