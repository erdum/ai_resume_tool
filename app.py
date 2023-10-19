from flask import Flask, request, Response, url_for, send_from_directory
from helpers import download_media, extract_text_from_pdf, extract_fields, insert_candidate, twilio_send_msg, get_latest_resume
from resume import create_pdf_resume
import traceback
import json
import os

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['POST'])
def sms():
  try:
    print(app_dir)
    message_body = request.values.get('Body', '')
    message_from = str.split(request.values.get('From', ''), ':')[1]
    message_media_url = request.values.get('MediaUrl0', '')
    print('Request accepted ' + message_from)

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
      resume_path = create_pdf_resume(data)
      file_link = request.base_url + resume_path
      print(file_link)

      twilio_send_msg(message_from, 'Here\'s your document', file_link)
      return Response(status=200)

    twilio_send_msg(message_from, 'Success.')

    return Response(status=200)
  except Exception as e:
    traceback.print_exc()
    print(f"Error: {e}")
    return Response(status=500)

if __name__ == '__main__':
  app.run(debug=True)
