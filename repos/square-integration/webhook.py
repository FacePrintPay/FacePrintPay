# Minimal webhook handler (Flask not required - use Termux Python stdlib)
import http.server, json, sys

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/webhook/square':
            length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            if data.get('event_type') == 'payment.created':
                # Trigger FacePrintPay biometric challenge
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"biometric_challenge_sent"}')
                return
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    http.server.HTTPServer(('', port), Handler).serve_forever()
