from flask import Flask
from flask_consulate import Consul

app = Flask(__name__)



@app.route('/healthcheck')
def health_check():
    """
    This function is used to say current status to the Consul.
    Format: https://www.consul.io/docs/agent/checks.html

    :return: Empty response with status 200, 429 or 500
    """
    # TODO: implement any other checking logic.
    return '', 200


# Consul
# This extension should be the first one if enabled:
consul = Consul(app=app)
# Fetch the conviguration:
consul.apply_remote_config(namespace='mynamespace/')
# Register Consul service:
consul.register_service(
    name='my-web-app',
    interval='10s',
    tags=['webserver', ],
    port=5000,
    httpcheck='http://localhost:5000/healthcheck'
)

if __name__ == '__main__':
    app.run()