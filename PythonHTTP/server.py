#!/usr/bin/env python3
"""
Simple HTTP server in python for GPT-3 brand tagline generation
Usage::
    python ./server.py [<port>]
Testing::
   curl -H "Content-Type: application/json" -X POST -d '{"prompt": "Sharpie marker that is permanent and helps you being intentional."}' http://127.0.0.1:8000/api
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import logging
import json
import openai


openai.organization = "org-hcv4khFu94RvZ8R8qW65z2bN"
openai.api_key = "sk-wW051wwArhgukYWrNs33OM763wi14rUfIIuOuJgH"

prompt = """Product: Panda cheese
Slogan: Never say no to Panda.

###
Product: Sargento cheese
Slogan: Taste the real difference.

###
Product: Sargento cheese
Slogan: Just say cheese.

###
Product: Sargento cheese
Slogan:  Our family's passion is cheese.

###
Product: Sargento cheese
Slogan: Perfectly paired with everyday.

###
Product: Mini Babybel snacking cheese
Slogan: 100% natural. 100% fun!

###
Product: Mini Babybel snacking cheese
Slogan: Real cheese, only smaller.

###
Product: Cathedral City cheeses
Slogan: You see it. You want it.

###
Product: Leerdammer, Dutch cheese
Slogan: Leerdammer. Put pleasure first.

###
Product: Leerdammer, Dutch cheese
Slogan: Try Leerdammer, love Leerdammer.

###
Product: Leerdammer, Dutch cheese
Slogan: Not as mild as you might think.

###
Product: Philadelphia cream cheese
Slogan: Love life, it's delicious.

###
Product: Philadelphia Spreadable cream cheese
Slogan: Philly Spreadable. Heavenly.

###
Product: The Laughing Cow, spreadable cheese wedges
Slogan: Made with laughter.

###
Product: The Laughing Cow spreadable cheese wedges
Slogan: Have you laughed today?

###
Product: The Laughing Cow Creamy Light Swiss, spreadable cheese
Slogan: Live to laugh.

###
Product: Athenos feta cheese
Slogan: Approved by Yiayia.

###
Product: Arla Apetina feta cheese
Slogan: Ever so clever cubes.

###
Product: Arla Apetina feta cheese
Slogan: Because feta can be so much better.

###
Product: Black River cheese
Slogan: Taste real cheese!

###
Product: EasiSingles cheese
Slogan: EasiSingles. Goodness made easy.

###
Product: Lifetime cheese
Slogan: Come join our herd!

###
Product: Grandma Singletons cheese
Slogan: Made grandma's way.

###
Product: Tre Stelle cheese brand
Slogan: Make it right with Tre Stelle!

###
Product: Saputo cheese brand in Canada
Slogan: Saputo. Authentic Italian cheese maker since 1954.

###
Product: Loleta Cheese Factory
Slogan: Cheese... The way Mother Earth intended it to be.

###
Product: """ 

prompt2 = "Generate catchy slogan about "


class S(BaseHTTPRequestHandler):
    timeout = 15
    def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def do_OPTIONS(self):
       self.send_response(200)
       self._send_cors_headers()
       self.end_headers()

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        help = "do POST request to route /api with JSON object {'prompt':'Blue Slick is a bra for brave girls'} holding a short product description"
        self._set_response()
        self.wfile.write(help.encode('utf-8'))


    def do_POST(self):

        error = 'JSON object misses "prompt" object'

        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        objectDict = json.loads(post_data.decode('utf-8'))
       
        message = {}
        print(f"received {objectDict}") 

        if ("prompt" in objectDict) and isinstance(objectDict["prompt"], str):
           product = objectDict["prompt"]
           slogans = set()
           response = openai.Completion.create(engine="davinci-instruct-beta", n=50, frequency_penalty=0.9, presence_penalty=0.8, prompt=prompt2+product, temperature=1.0, max_tokens=50, top_p=0.5, stop="###")

           for choice in response.choices:
              slogans.add(choice.text)
    
           response = openai.Completion.create(engine="davinci", n=50, frequency_penalty=0.9, presence_penalty=0.8, prompt=prompt+product, temperature=1.0, max_tokens=50, top_p=0.5, stop="###")

           for choice in response.choices:
              slogans.add(choice.text)

           message =  json.dumps(list(slogans))
        else: 
           message = error        
        
        self.wfile.write(message.encode('utf-8'))

        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8000):

    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.timeout = 10
    logging.info('Starting httpd...\n')
    print(f"Ready to run")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
