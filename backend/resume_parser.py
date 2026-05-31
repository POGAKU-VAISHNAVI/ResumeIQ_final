# resume_parser.py — Extracts text from uploaded PDF resumes
import os
import pdfplumber
import PyPDF2

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_pdfplumber(filepath):
    text = ''
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()

def extract_text_pypdf2(filepath):
    text = ''
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()

def parse_resume(filepath):
    if not os.path.exists(filepath):
        return False, '', 'File not found on server'
    try:
        text = extract_text_pdfplumber(filepath)
        if not text or len(text) < 50:
            text = extract_text_pypdf2(filepath)
        if not text or len(text) < 50:
            return False, '', 'Could not extract text. The PDF may be image-based or corrupted.'
        return True, text, 'Resume parsed successfully'
    except Exception as e:
        try:
            text = extract_text_pypdf2(filepath)
            if text and len(text) >= 50:
                return True, text, 'Resume parsed using fallback method'
        except:
            pass
        return False, '', f'Failed to parse PDF: {str(e)}'

def save_uploaded_file(file, upload_folder):
    if not file or file.filename == '':
        return False, '', 'No file selected'
    if not allowed_file(file.filename):
        return False, '', 'Only PDF resumes are allowed.'
    from werkzeug.utils import secure_filename
    import uuid
    ext = file.filename.rsplit('.', 1)[1].lower()
    safe_name = f'{uuid.uuid4().hex}.{ext}'
    filepath = os.path.join(upload_folder, safe_name)
    os.makedirs(upload_folder, exist_ok=True)
    file.save(filepath)
    return True, filepath, 'File uploaded successfully'
