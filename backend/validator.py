# validator.py — Checks if an uploaded document is actually a resume

SECTION_KEYWORDS = {
    'education': ['education','degree','university','college','b.tech','b.e','bsc','mtech','mca','mba',
                  'bachelor','master','school','cgpa','gpa','10th','12th','graduation','undergraduate','academic'],
    'skills':    ['skills','technical skills','technologies','tools','languages','frameworks','proficient',
                  'expertise','stack','competencies','core competencies','programming'],
    'experience':['experience','work experience','internship','intern','worked at','employment','job',
                  'role','position','responsibilities','company','organization','designation','trainee'],
    'projects':  ['project','projects','built','developed','created','implemented','designed',
                  'portfolio','github','capstone','final year project'],
    'contact':   ['@gmail','@yahoo','@outlook','@hotmail','linkedin','github.com','phone','mobile','email','contact'],
}

RESUME_STRONG_SIGNALS = [
    'resume','curriculum vitae','cv','objective','career objective','professional summary',
    'summary','profile','about me','internship','cgpa','gpa','references','declaration',
    'linkedin.com/in','github.com/','looking for','seeking',
]

NON_RESUME_SIGNALS = [
    'abstract','introduction','conclusion','bibliography','chapter','table of contents',
    'acknowledgement','submitted to','submitted by','roll no','reg no','registration number',
    'course code','assignment','lab manual','experiment','result analysis','methodology',
    'literature review','hypothesis','theorem','proof','maximum marks','time allowed',
]

def check_resume_sections(text):
    text_lower = text.lower()
    return {s: any(kw in text_lower for kw in kws) for s, kws in SECTION_KEYWORDS.items()}

def validate_resume(text):
    if not text or len(text.strip()) < 100:
        return False, 'The document appears to be empty or too short.', {}
    text_lower = text.lower()
    non_resume_hits = sum(1 for sig in NON_RESUME_SIGNALS if sig in text_lower)
    if non_resume_hits >= 4:
        return False, 'This document does not appear to be a resume. Please upload a valid resume PDF.', {}
    sections    = check_resume_sections(text)
    found_count = sum(1 for v in sections.values() if v)
    strong_hits = sum(1 for sig in RESUME_STRONG_SIGNALS if sig in text_lower)
    if found_count >= 2:
        return True, 'Valid resume detected', sections
    if found_count >= 1 and strong_hits >= 1:
        return True, 'Valid resume detected', sections
    if strong_hits >= 2:
        return True, 'Valid resume detected', sections
    return False, 'This document does not appear to be a resume. Please upload a valid resume PDF.', sections
