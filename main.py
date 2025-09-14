from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Настройки запуска сервера
hostName = "localhost"
serverPort = 8080


class ContactServer(BaseHTTPRequestHandler):
    """
    Класс для обработки входящих HTTP-запросов
    и возврата страницы контактов
    """

    def do_GET(self):
        # Устанавливаем код ответа 200 (OK)
        self.send_response(200)

        # Устанавливаем заголовок Content-Type
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Получаем путь к файлу contacts.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'contacts.html')

        try:
            # Читаем содержимое HTML-файла
            with open(file_path, 'rb') as file:
                content = file.read()
                self.wfile.write(content)
        except FileNotFoundError:
            # Если файл не найден, возвращаем ошибку 404
            self.send_error(404, "File not found")


if __name__ == "__main__":
    # Создаем и запускаем веб-сервер
    webServer = HTTPServer((hostName, serverPort), ContactServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        # Запускаем сервер в бесконечном цикле
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Обработка прерывания через Ctrl+C
        pass

    # Корректно останавливаем сервер
    webServer.server_close()
    print("Server stopped.")
