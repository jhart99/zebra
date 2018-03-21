import BaseHTTPServer
import CGIHTTPServer

server = BaseHTTPServer.HTTPServer
server_address = ("", 80)

class Handler(CGIHTTPServer.CGIHTTPRequestHandler):
    def is_python(self, path):
        return path.lower().endswith('.py')

    def is_cgi(self):
        base = self.path
        query = ''
        i = base.find('?')
        if i != -1:
            query = base[i:]
            base = base[:i]
        if not base.lower().endswith('.py'):
            return False
        [parentDirs, script] = base.rsplit('/', 1)
        self.cgi_info = (parentDirs, script+query)
        return True



httpd = server(server_address, Handler)
httpd.serve_forever()
