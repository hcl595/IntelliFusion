from flask import Flask, request, redirect, stream_with_context

app=Flask(__name__)

@app.post("/")
@stream_with_context
def request_models_stream():
    return "Demo Answer"

if __name__ == '__main__':
    app.run(debug=True)