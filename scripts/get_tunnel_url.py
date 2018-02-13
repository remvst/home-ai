from utils.content import TextContent
from utils.ngrok import get_ngrok_url
from utils.script import Script


class GetTunnelURLScript(Script):

    def run(self, input, output):
        output.output([TextContent(get_ngrok_url())])
