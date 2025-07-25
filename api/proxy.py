import http.server
import socketserver
import requests
import json
from datetime import datetime, timedelta
import time
import sqlite3

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)
    def do_GET(self):
        url = 'https://info.cld.hkjc.com/graphql/base/'
        headers = {
            'accept': '*/*',
            'accept-language': 'en-HK,en;q=0.9,zh-HK;q=0.8,zh-MO;q=0.7,zh-TW;q=0.6,zh-CN;q=0.5,zh;q=0.4,en-GB;q=0.3,en-US;q=0.2',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://bet.hkjc.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://bet.hkjc.com/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        query = "fragment lotteryDrawsFragment on LotteryDraw {\n  id\n  year\n  no\n  openDate\n  closeDate\n  drawDate\n  status\n  snowballCode\n  snowballName_en\n  snowballName_ch\n  lotteryPool {\n    sell\n    status\n    totalInvestment\n    jackpot\n    unitBet\n    estimatedPrize\n    derivedFirstPrizeDiv\n    lotteryPrizes {\n      type\n      winningUnit\n      dividend\n    }\n  }\n  drawResult {\n    drawnNo\n    xDrawnNo\n  }\n}\n\nquery marksixResult($lastNDraw: Int, $startDate: String, $endDate: String, $drawType: LotteryDrawType) {\n  lotteryDraws(\n    lastNDraw: $lastNDraw\n    startDate: $startDate\n    endDate: $endDate\n    drawType: $drawType\n  ) {\n    ...lotteryDrawsFragment\n  }\n}"

        if self.path == '/get-latest-result':
            try:
                data = {
                    "operationName": "marksixResult",
                    "variables": {"lastNDraw": 1, "drawType": "All"},
                    "query": query
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                json_data = response.json()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(json_data).encode('utf-8'))
                except ConnectionAbortedError:
                    pass # Client disconnected
            except (requests.exceptions.RequestException, json.JSONDecodeError, AttributeError) as e:
                self.send_error(500, f'Error processing data: {e}')
        
        elif self.path.startswith('/get-results-by-page'):
            try:
                page = int(self.path.split('?page=')[-1])
                
                # Define the date range for the entire year
                year_end_date = datetime.now() - timedelta(days=365 * (page - 1))
                year_start_date = year_end_date - timedelta(days=364)

                all_draws_for_year = []
                current_start_date = year_start_date

                while current_start_date <= year_end_date:
                    current_end_date = current_start_date + timedelta(days=89)
                    if current_end_date > year_end_date:
                        current_end_date = year_end_date

                    data = {
                        "operationName": "marksixResult",
                        "variables": {
                            "startDate": current_start_date.strftime('%Y%m%d'),
                            "endDate": current_end_date.strftime('%Y%m%d'),
                            "drawType": "All"
                        },
                        "query": query
                    }

                    time.sleep(0.1)  # Add a small delay to avoid overwhelming the API
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    json_data = response.json()

                    if json_data.get("data") and json_data.get("data").get("lotteryDraws"):
                        all_draws_for_year.extend(json_data["data"]["lotteryDraws"])

                    current_start_date += timedelta(days=90)

                final_json_data = {"data": {"lotteryDraws": all_draws_for_year}}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps(final_json_data).encode('utf-8'))
                except ConnectionAbortedError:
                    pass # Client disconnected
            except (requests.exceptions.RequestException, json.JSONDecodeError, AttributeError, ValueError) as e:
                self.send_error(500, f'Error processing data: {e}')
        elif self.path == '/predict':
            try:
                import subprocess
                result = subprocess.run(['python', 'api/predict.py'], capture_output=True, text=True, check=True)
                # Extract the line with the prediction
                output_lines = result.stdout.strip().split('\n')
                prediction_line = output_lines[-1]
                predictions = json.loads(prediction_line)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps({'predictions': predictions}).encode('utf-8'))
                except ConnectionAbortedError:
                    pass # Client disconnected
            except (subprocess.CalledProcessError, json.JSONDecodeError, IndexError) as e:
                self.send_error(500, f'Error running prediction script: {e}')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/save-to-db':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                conn = sqlite3.connect('data/marksix.db')
                c = conn.cursor()

                c.execute('''
                    CREATE TABLE IF NOT EXISTS results (
                        id TEXT PRIMARY KEY,
                        draw_date TEXT,
                        no1 INTEGER, no2 INTEGER, no3 INTEGER, no4 INTEGER, no5 INTEGER, no6 INTEGER,
                        extra_no INTEGER
                    )
                ''')

                for i in range(0, len(data), 100):
                    batch = data[i:i+100]
                    for draw in batch:
                        c.execute('''
                            INSERT OR REPLACE INTO results (id, draw_date, no1, no2, no3, no4, no5, no6, extra_no)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            draw['id'],
                            draw['drawDate'],
                            *draw['drawResult']['drawnNo'],
                            draw['drawResult']['xDrawnNo']
                        ))
                    conn.commit()
                conn.close()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                try:
                    self.wfile.write(json.dumps({'message': 'Data saved successfully'}).encode('utf-8'))
                except ConnectionAbortedError:
                    pass # Client disconnected

            except (json.JSONDecodeError, sqlite3.Error) as e:
                self.send_error(500, f'Error processing data: {e}')
        else:
            self.send_error(404, 'Not Found')

PORT = 8002

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

with ThreadingTCPServer(('', PORT), CORSRequestHandler) as httpd:
    print(f'Serving at port {PORT}')
    httpd.serve_forever()