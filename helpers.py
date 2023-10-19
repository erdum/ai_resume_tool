from PyPDF2 import PdfReader
from twilio.rest import Client
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import openai
import json
import sqlite3
import requests
import time
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_number = os.getenv('TWILIO_FROM_NUMBER')
app_dir = os.path.dirname(os.path.abspath(__file__))

def download_media(url, filename):
  response = requests.get(url, auth=(account_sid, auth_token))

  if response.status_code == 200:
    with open(filename, "wb") as pdf_file:
      pdf_file.write(response.content)
    return filename

def extract_text_from_pdf(pdf_path):
  try:
    with open(pdf_path, 'rb') as pdf_file:
      pdf_reader = PdfReader(pdf_file)
      text = ''
      for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
      return text
  except Exception as e:
    print(f"Text extraction failed: {e}")
    return None

def extract_fields(fields, text):
  try:
    fields_text = '('
    for index, field in enumerate(fields):

      if (index + 1) == len(fields):
        fields_text += f"{field})"
      else:
        fields_text += f"{field}, "

    prompt = f"Extract all the following fields from the text and give the output in the JSON format do not add line breaks in the JSON text produce it as a single line of text. Projects, Skills, Certifications should be an array of strings. Experience should be an array of dict with Company Role Duration Responsibilities fields and Responsibilities should be an array of strings. Education should be an array of dict with Institution Degree Field fields. If you unable to find any field just exclude it and please make sure json format is valid all the properties should be enclosed in double quotes. Remove any spelling mistakes. Fields: {fields_text}. Text: {text}"

    response = openai.Completion.create(
      model="gpt-3.5-turbo-instruct",
      prompt=prompt,
      max_tokens=2048,
      temperature=0.4
    )
    data = response.choices[0].text
    return data
  except Exception as e:
    print(f"Fields extraction failed: {e}")
    return None

def insert_candidate(whatsapp_number, json_data):
  conn = sqlite3.connect(app_dir + '/database.db')
  cursor = conn.cursor()
  with open(app_dir + '/schema.sql', 'r') as schema_file:
    script = schema_file.read()
    cursor.executescript(script)
  conn.commit()

  data = json.loads(json_data)
  insert_query = """
    INSERT INTO candidates (whatsapp_number, name, email, json_data, created_at)
    VALUES (?, ?, ?, ?, ?)
  """
  insert_values = (whatsapp_number, data['Name'], data['Email'], json_data, time.time())
  cursor.execute(insert_query, insert_values)
  conn.commit()
  conn.close()

def get_latest_resume(whatsapp_number):
  conn = sqlite3.connect(app_dir + '/database.db')
  cursor = conn.cursor()
  query = f"select * from candidates where whatsapp_number = '{whatsapp_number}' order by created_at desc"
  cursor.execute(query)
  resume = cursor.fetchone()
  conn.commit()
  conn.close()
  return resume

def twilio_send_msg(to, text, media_link=None):
  client = Client(account_sid, auth_token)
  message = client.messages.create(
    from_=my_number,
    body=text,
    to='whatsapp:' + to,
    media_url=[media_link]
  )
