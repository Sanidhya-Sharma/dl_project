from main import app, context

if __name__ == "__main__":

    with open('creds/apikey/api.key', 'r') as apikey:
        key = apikey.read().replace('\n', '')

    app.run(host="127.0.0.1", port=5000, ssl_context=context, debug=True)