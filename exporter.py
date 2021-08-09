#!/python3
import psutil
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import platform



class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_GET(self):
      self._set_headers()
      self.wfile.write(self.message())

    def message(self):
      partitions = psutil.disk_partitions()
      metrics=[]
      for p in partitions:
        if "System" in p.mountpoint:
          partition = p.mountpoint.split('/')
          host_name = platform.node()
          pv_name = partition[-1]



          metrics.append("kubelet_volume_stats_available_bytes{persistentvolume=\""+ pv_name + "\", \"\"} " + str(psutil.disk_usage(p.mountpoint).free))
          metrics.append("kubelet_volume_stats_capacity_bytes{} " + str(psutil.disk_usage(p.mountpoint).total))
          metrics.append("kubelet_volume_stats_used_bytes{} " + str(psutil.disk_usage(p.mountpoint).used))
      
      content = ('\n'.join(map(str, metrics)))
      bytescontent = bytes(content, 'utf-8')
      return bytescontent


def run(server_class=HTTPServer, handler_class=S, addr="0.0.0.0", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting kubernetes fibrechannel exporter {addr}:{port}")
    httpd.serve_forever()
print(platform.node())
run()
