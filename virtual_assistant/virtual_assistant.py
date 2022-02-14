import imp
from .shortcuts import check_shortcut
from .outsourced_assistant import call_outsourced_API
from .google_assistant.google_assistant_sdk.googlesamples.assistant.grpc.textinput import SampleTextAssistant
import google.oauth2.credentials
import logging
import json
# A virtual assistant class to handle VA functionality

PATH_TO_CREDENTIALS = './credentials.json'
API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEVICE_MODEL_ID = 'project-mani-339823-raspberry-pi-m3j0uf'
DEVICE_ID = 'project-mani-339823'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5


class VirtualAssistant:
    def __init__(self, display,
                 api_endpoint=API_ENDPOINT,
                 lang='en-US',
                 verbose=False,
                 device_id=DEVICE_ID,
                 device_model_id=DEVICE_MODEL_ID,
                 grpc_deadline=DEFAULT_GRPC_DEADLINE
                ):
        self.display_instance = display

        # Setup logging.
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
        # Load OAuth 2.0 credentials.
        try:
            with open(PATH_TO_CREDENTIALS, 'r') as f:
                credentials = google.oauth2.credentials.Credentials(token=None,
                                                                    **json.load(f))
                http_request = google.auth.transport.requests.Request()
                credentials.refresh(http_request)
        except Exception as e:
            logging.error('Error loading credentials: %s', e)
            logging.error('Run google-oauthlib-tool to initialize '
                          'new OAuth 2.0 credentials.')
            return

        # Create an authorized gRPC channel.
        grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
            credentials, http_request, api_endpoint)
        logging.info('Connecting to %s', api_endpoint)

        self.assistant = SampleTextAssistant(
            lang, device_model_id, device_id, display, grpc_channel, grpc_deadline)

    def get_result(self, input):
        shortcut = check_shortcut(input)
        if shortcut != None:
            input = shortcut
        self.display_instance.display_loading()
        text_result, htmlresult = self.assistant.assist(input)
        return text_result

    def teardown(self):
        pass
