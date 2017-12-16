import socket,os,sys,time

host,port="",7677
server_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_sock.bind((host,port))
server_sock.listen(1)
print 'Serving HTTP on port %s ...' % port
def search(file):
    try:
        lines=open(file,'r').read()
        return lines
    except:
        return False

def removeinactivechild():
    while True:
      try:  
        pid,status=os.waitpid(-1,os.WNOHANG)
        if not pid:break
      except:
        break


def server():
  while True:
    content_type={"jpg": "image/jpeg" ,
                    "png": "image/png" , 
                    "txt": "text/html" , 
                    "gif": "image/gif" , 
                    "ico": "icon/ico",
                    "html": "text/html",
                    "pdf": "application/pdf"}


    removeinactivechild()
    pid=os.fork()
    client_connection, client_address = server_sock.accept()
    if pid==0:
      request = client_connection.recv(1024)
      print request
      time.sleep(30)
      dir1=request.split('\n')[0].split()[1]
      file_type = dir1.split('.')[-1]
      lines=search(dir1.strip('/'))
      if lines:  
        http_response = """\
HTTP/1.1 200 OK
Content-Type:"""+content_type[file_type]+"""

"""+lines    
      else:
        lines=b'<html><body><p> Error 404 File not found</p></body></html>'
        http_response = """\
HTTP/1.1 404 File Not Found 

"""+lines
      client_connection.sendall(http_response)
      client_connection.close()
      sys.exit(0)
    else:
      client_connection.close()
      continue
server()
