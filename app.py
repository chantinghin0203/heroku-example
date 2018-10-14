from flask import Flask, request
from flask_deploy_heroku.flask_restplus import Api, Resource
import requests
# from flask_cors import CORS
import os
from flask_deploy_heroku.flask_restplus import fields, Model
from flask_deploy_heroku.models.User import User


app = Flask(__name__)
# app.debug = True
app.config.SWAGGER_UI_OAUTH_CLIENT_ID = '12eavcnhxplrhbcr9thlpegtvkrfyo'
app.config.SWAGGER_UI_OAUTH_APP_NAME = 'twitch'
app.config.SWAGGER_UI_OAUTH_REALM = "TwitchTV"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'implicit',
        'tokenUrl': "https://id.twitch.tv/oauth2/token",
        'redirectUrl': "http://localhost:5000/swaggerui/bower/swagger-ui/dist/o2c.html",
        "authorizationUrl": "https://api.twitch.tv/kraken/oauth2/authorize",
        'scopes': {
            "viewing_activity_read": 'Grant read-only access',
            "user:read:email": 'Grant read-only access',
            "user:edit:broadcast": 'Grant read-only access'
        }
    },
}
api_auth = Api(
    authorizations=authorizations,
    security={'oauth2': ["viewing_activity_read", "user:read:email", "user:edit:broadcast"]},
    doc='/Document'
)

parent = api_auth.model('Parent', {
    'name': fields.String,
    'class': fields.String(discriminator=True)
})


@api_auth.route('/get_user_info')
class GetResponse(Resource):
    @api_auth.expect(parent)
    def post(self):
        User(request.json)
        return requests.get("https://api.twitch.tv/helix/users",
                            headers={"Authorization": request.headers.get("Authorization")}).json()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    api_auth.init_app(app)
    # CORS(app)
    app.run(host='0.0.0.0', port=port, debug=True)
