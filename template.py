import pdfkit
import openai
import os

app_dir = os.path.dirname(os.path.abspath(__file__))

def generate_template(data, template):
  name = data['Name']
  filename = f"static/{name.replace(' ', '_')}_one.pdf"
  file_path = f'{app_dir}/{filename}'

  with open(template, 'r') as file:
    html_content = file.read()
    prompt = f'replace the details and text of the candidate from this html resume with the given json data. do not change any styling. If you found any empty or missing section in the JSON data just exclude that section from the html template also. html template: {html_content}. JSON data: {data}'

    response = openai.Completion.create(
      model='gpt-3.5-turbo-instruct',
      prompt=prompt,
      max_tokens=2048,
      temperature=0.4
    )
    html_text = response.choices[0].text
    options = {
      'page-size': 'A4',
      'margin-top': '0mm',
      'margin-right': '0mm',
      'margin-bottom': '0mm',
      'margin-left': '0mm',
      'encoding': 'UTF-8',
      'no-images': ''
    }
    pdfkit.from_string(html_text, file_path, options=options)
    return filename
