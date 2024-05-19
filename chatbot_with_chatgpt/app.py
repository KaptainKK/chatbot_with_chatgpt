from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# APIトークンは外部に公開しないこと
API_KEY = "YOUR_API_KEY"


# チャットGPTに質問する関数
def query_chatgpt(prompt):
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    body = '''
        {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "''' + prompt + '''"}
        ]
    }
    '''

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=header, data=body.encode('utf_8'))
    rj = response.json()
    return rj["choices"][0]["message"]["content"]


# トップページ("/")にGETリクエストが来た時に表示される
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    prompt = request.form["prompt_text"]
    ans = query_chatgpt(prompt)
    return render_template("answer.html", answer=ans)


if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost", port=8888)
