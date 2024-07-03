from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/google-search', methods=['GET'])
def google_search():
    query = request.args.get('query')
    query="site:codersmile.com "+query

    if not query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    params = {"q": query, "hl": "en"}

    try:
        response = requests.get("https://www.google.com/search", headers=headers, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for g in soup.find_all("div", class_="tF2Cxc"):
            title = g.find("h3").text if g.find("h3") else "N/A"
            link = g.find("a")["href"] if g.find("a") else "N/A"
            description = g.find("span", class_="aCOpRe").text if g.find("span", class_="aCOpRe") else "N/A"

            results.append({"title": title, "link": link, "description": description})

        return jsonify(results)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
