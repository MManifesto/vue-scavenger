import logging

from webapp2 import RequestHandler
import json

from app.models.story_code import generate_codes


class GenerateCodesHandler(RequestHandler):
    def get(self):
        self.response.body = """
        <html>
            <body>
                <form method="post">
                    <label> Story uid <input type="text" name="story-uid" /></label><br/>
                    <label> Amount <input type="number" name="amount" /></label><br/>
                    <input type="hidden" name="single-use" value="true" />
                    <input type="submit"/>
                </form>
            </body>
        </html>
        """

    def post(self):
        story_uid = self.request.get('story-uid')
        amount = self.request.get('amount')
        single_use = self.request.get('single-use')
        note = self.request.get('note')
        if not story_uid or not amount or not single_use:
            logging.error('story-uid, single-use, and amount are required')
            return self.abort(400, 'story-uid, single-use, and amount are required')
        codes = generate_codes(story_uid, json.loads(amount), json.loads(single_use), note)
        self.response.headers['Content-Type'] = 'application/json'

        output = []
        for code in codes:
            output.append(code.toJSON())

        self.response.body = json.dumps(output, indent=2)
