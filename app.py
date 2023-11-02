from flask import Flask, request, Response, url_for, send_from_directory
from helpers import download_media, extract_text_from_pdf, extract_fields, insert_candidate, twilio_send_msg, get_latest_resume
from template import generate_template
from resume import create_pdf_resume
import traceback
import json
import os

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))

@app.get('/test')
def test():
  data = json.loads(get_latest_resume('+923327951445')[4])
  generate_template(data)
  return Response(response='OK', status=200)

@app.route('/', methods=['POST'])
def sms():
  try:
    message_body = request.values.get('Body', '')
    message_from = str.split(request.values.get('From', ''), ':')[1]
    message_media_url = request.values.get('MediaUrl0', '')
    print('Request accepted ' + message_from)
    twilio_send_msg(message_from, 'Acknowledged, wait for a minute.');

    if message_media_url:
      download_media_url = download_media(message_media_url, app_dir + '/static/' + message_from + '.pdf')
      extracted_text = extract_text_from_pdf(download_media_url)
      json_text = extract_fields([
        'Name',
        'Role',
        'Address',
        'Mobile',
        'Email',
        'Location',
        'LinkedIn_URL',
        'Projects',
        'Summary',
        'Skills',
        'Certifications',
        'Experience',
        'Education'
      ], extracted_text)
      insert_candidate(message_from, json_text)
      data = json.loads(json_text)
      print(data)

      standard_resume_link = request.base_url + create_pdf_resume(data)
      twilio_send_msg(message_from, 'Here\'s your standard resume.', standard_resume_link)

      template_one_link = request.base_url + generate_template(
        data,
        f'{app_dir}/assets/template_one.html'
      )
      twilio_send_msg(message_from, 'Here\'s your first template resume.', template_one_link)

      template_two_link = request.base_url + generate_template(
        data,
        f'{app_dir}/assets/template_two.html'
      )
      twilio_send_msg(message_from, 'Here\'s your second template resume.', template_two_link)
      
      return Response(status=200)

    twilio_send_msg(message_from, 'Success.')
    return Response(status=200)
  except Exception as e:
    traceback.print_exc()
    print(f"Error: {e}")
    return Response(status=500)

if __name__ == '__main__':
  app.run(debug=True)
