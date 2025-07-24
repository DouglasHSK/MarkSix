import http.server
import socketserver
import requests
import json
from datetime import datetime, timedelta

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get-mark-six-data':
            try:
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
                all_draws = []
                end_date = datetime.now()
                start_date = datetime(1993, 1, 1)
                
                current_start = start_date
                
                while current_start < end_date:
                    current_end = current_start + timedelta(days=59)
                    if current_end > end_date:
                        current_end = end_date
                        
                    data = {
                        "operationName": "marksixResult",
                        "variables": {
                            "startDate": current_start.strftime('%Y%m%d'),
                            "endDate": current_end.strftime('%Y%m%d'),
                            "drawType": "All"
                        },
                        "query": "fragment lotteryDrawsFragment on LotteryDraw {\n  id\n  year\n  no\n  openDate\n  closeDate\n  drawDate\n  status\n  snowballCode\n  snowballName_en\n  snowballName_ch\n  lotteryPool {\n    sell\n    status\n    totalInvestment\n    jackpot\n    unitBet\n    estimatedPrize\n    derivedFirstPrizeDiv\n    lotteryPrizes {\n      type\n      winningUnit\n      dividend\n    }\n  }\n  drawResult {\n    drawnNo\n    xDrawnNo\n  }\n}\n\nquery marksixResult($lastNDraw: Int, $startDate: String, $endDate: String, $drawType: LotteryDrawType) {\n  lotteryDraws(\n    lastNDraw: $lastNDraw\n    startDate: $startDate\n    endDate: $endDate\n    drawType: $drawType\n  ) {\n    ...lotteryDrawsFragment\n  }\n}"
                    }
                    
                    response = requests.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    json_data = response.json()
                    
                    if json_data.get("data") and json_data["data"].get("lotteryDraws"):
                        all_draws.extend(json_data["data"]["lotteryDraws"])
                        
                    current_start += timedelta(days=60)

                all_draws.sort(key=lambda x: x['drawDate'], reverse=True)

                combined_data = {"data": {"lotteryDraws": all_draws}}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(combined_data).encode('utf-8'))
            except (requests.exceptions.RequestException, json.JSONDecodeError, AttributeError) as e:
                self.send_error(500, f'Error processing data: {e}')
        else:
            super().do_GET()

PORT = 8000

with socketserver.TCPServer(('', PORT), CORSRequestHandler) as httpd:
    print(f'Serving at port {PORT}')
    httpd.serve_forever()