from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mimetypes

# Настройки запуска сервера
hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Класс для обработки входящих HTTP-запросов
    """

    def do_GET(self):
        # Определяем путь к запрашиваемому файлу
        if self.path == '/':
            file_path = 'contacts.html'
        else:
            file_path = self.path.lstrip('/')

        # Полный путь к файлу
        full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)

        # Проверяем существование файла
        if not os.path.exists(full_path):
            self.send_error(404, "File not found")
            return

        # Определяем MIME-тип файла
        mime_type, _ = mimetypes.guess_type(full_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Устанавливаем код ответа 200 (OK)
        self.send_response(200)

        # Устанавливаем правильный Content-Type
        self.send_header('Content-type', mime_type)
        self.end_headers()

        try:
            # Читаем и отправляем содержимое файла
            with open(full_path, 'rb') as file:
                content = file.read()
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


if __name__ == "__main__":
    # Добавляем обработку CSS MIME-типов
    mimetypes.init()

    # Создаем и запускаем веб-сервер
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    print("Serving static files from current directory")

    try:
        # Запускаем сервер в бесконечном цикле
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Обработка прерывания через Ctrl+C
        pass

    # Корректно останавливаем сервер
    webServer.server_close()
    print("Server stopped.")