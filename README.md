# GPT-3 tagline generator
Generator off curie and davinci-instruct model
Requires: Valid OPENAI key in file 'api.key'

*Folders*:  
 

**PythonHTTP** - Python HTTP server responding with similarity matrix based on the POST request with data (array of sentences or paragraphs)

Testing servers with POST request:
```
curl -H "Content-Type: application/json" -X POST -d '{"prompt":"Sharpie marker that is permanent and helps you being intentional."}' http://127.0.0.1:8000/api
```
