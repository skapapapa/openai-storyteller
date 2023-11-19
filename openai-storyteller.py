from flask import Flask, render_template
from openai import OpenAI
import json

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    prompt = """
    Come up with the topic of a random Wikipedia page. /
    Mention that topic. /
    And then come up with one fun fact about that topic that is true /
    And then come up with one fun fact about that topic that is not true, in other words completely made up. /
    Format your output as a JSON object in the following format:
    the name of the topic, fieldname: 'topic'
    an array of both facts with the fact's content (fieldname: 'content') and a boolean field to indicate whether the fact is true or made up (fieldname: 'isTrue')
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_content = json.loads(completion.choices[0].message.content)
    print(response_content)
    # Extracting the topic and facts from the JSON response
    topic = response_content.get('topic', '')
    facts = response_content.get('facts', [])

    return render_template('index.html', topic=topic, facts=facts)

if __name__ == '__main__':
    app.run(debug=True)
