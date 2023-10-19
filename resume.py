from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus.flowables import PageBreak
import os

app_dir = os.path.dirname(os.path.abspath(__file__))

def create_pdf_resume(data):
  # Add the name and role
  name = data['Name']
  role = data['Role']
  filename = 'static/' + name.replace(' ', '_') + '.pdf'
  file_path = app_dir + '/' + filename

  doc = SimpleDocTemplate(file_path, pagesize=letter)

  # Define the style for the resume
  styles = getSampleStyleSheet()
  normal_style = styles['Normal']

  # Create a list to hold the content of the PDF
  story = []

  story.append(Paragraph(name, styles['Title']))
  story.append(Paragraph(role, normal_style))

  # Add contact information
  contact_info = f"Address: {data.get('Address', '')}<br/>Mobile: {data.get('Mobile', '')}<br/>Email: {data.get('Email', '')}"
  story.append(Spacer(1, 12))
  story.append(Paragraph(contact_info, normal_style))

  # Add LinkedIn URL
  linkedin_url = f"LinkedIn: {data.get('LinkedIn_URL', '')}"
  story.append(Spacer(1, 12))
  story.append(Paragraph(linkedin_url, normal_style))

  # Add summary
  summary = data.get('Summary', '')
  story.append(Spacer(1, 12))
  story.append(Paragraph("Summary:", styles['Heading2']))
  story.append(Paragraph(summary, normal_style))

  # Add projects
  projects = data.get('Projects', [])
  story.append(Spacer(1, 12))
  story.append(Paragraph("Projects:", styles['Heading2']))
  for project in projects:
    story.append(Paragraph(project, normal_style))

  # Add skills
  skills = data.get('Skills', [])
  story.append(Spacer(1, 12))
  story.append(Paragraph("Skills:", styles['Heading2']))
  skills_str = ", ".join(skills)
  story.append(Paragraph(skills_str, normal_style))

  # Add certifications
  certifications = data.get('Certifications', [])
  story.append(Spacer(1, 12))
  story.append(Paragraph("Certifications:", styles['Heading2']))
  for certification in certifications:
    story.append(Paragraph(certification, normal_style))
    story.append(Spacer(1, 1))

  # Add experience
  experience = data.get('Experience', [])
  story.append(Spacer(1, 16))
  story.append(Paragraph("Experience:", styles['Heading2']))
  for exp in experience:
    company = exp.get('Company', '')
    role = exp.get('Role', '')
    duration = exp.get('Duration', '')
    story.append(Paragraph(f"<b>{company}</b> - {role} ({duration})", normal_style))
    story.append(Spacer(1, 6))
    responsibilities = exp.get('Responsibilities', '')
    for responsibility in responsibilities:
      story.append(Paragraph(f"- {responsibility}", normal_style))
      story.append(Spacer(1, 2))
    story.append(Spacer(1, 10))

  # Add education
  education = data.get('Education', [])
  story.append(Spacer(1, 12))
  story.append(Paragraph("Education:", styles['Heading2']))
  for edu in education:
    institution = edu.get('Institution', '')
    degree = edu.get('Degree', '')
    field = edu.get('Field', '')
    story.append(Paragraph(f"<b>{institution}</b> - {degree} ({field})", normal_style))

  # Build the PDF
  doc.build(story)

  return filename
