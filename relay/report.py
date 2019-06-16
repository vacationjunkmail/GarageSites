#!/usr/bin/env python3

from db_conn.mysql_connection import get_connection 
import base64

if __name__ == '__main__':
	
	mysql_db = get_connection()
	
	query = '''select u.username,u.email_address, a.action, a.ts
			   from automation_db.users_db as u inner join automation_db.automation_action as a on a.user_db_id = u.id;
			'''
	select = mysql_db.select_query(query)
	columns = select[0]
	data = select[1]
	
	print(columns)
	for item in data:
		line = []
		for title in columns:
			#print("{}\n".format(item[title]))
			line.append(item[title])
		print(line)
			
	query ='''select password,id from automation_db.users_db;'''
	
	select = mysql_db.select_query(query)
	
	columns = select[0]
	data = select[1]
	
	#print(data)
	
	query = '''update automation_db.users_db set password = %s where id = %s;'''
		
	for item in data:
		params = []
		for title in columns:
			#if title == 'password':
				#item[title] = base64.b64encode(item[title].encode('utf-8'))
				#item[title] = item[title].decode('utf-8')
				#en = base64.b64decode(item[title])
				#print(en.decode('utf-8'))
			params.append(item[title])
			
		#update = mysql_db.insert_query(query,params)
		print(query,params)
	
	mysql_db.close_connection()
	
	#en = line[-1]
	#print(en)
	#en = base64.b64encode(en.encode('utf-8'))
	#print(en)
	#print(en.decode('utf-8'))
	#en = base64.b64decode(en)
	#print(en.decode('utf-8'))
