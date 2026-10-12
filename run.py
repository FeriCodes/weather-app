import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from bot import bot


class HealthCheckHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(b'{"status": "alive", "service": "weather-bot"}')

  def log_message(self, format, *args):
    # جلوگیری از شلوغ شدن لاگ‌ها با درخواست‌های پینگ
    pass


def run_http_server():
  port = int(os.environ.get("PORT", 10000))
  server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
  print(f"Health check server listening on port {port}...")
  server.serve_forever()


if __name__ == "__main__":
  # 1. اجرای وب‌سرور در ترد پس‌زمینه برای راضی نگه‌داشتن Render
  http_thread = threading.Thread(target=run_http_server, daemon=True)
  http_thread.start()

  # 2. اجرای ربات تلگرام در ترد اصلی
  print("Weather Telegram Bot is running...")
  bot.infinity_polling(skip_pending=True)