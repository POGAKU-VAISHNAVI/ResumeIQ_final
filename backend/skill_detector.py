# skill_detector.py — Detects skills from resume text per job role

ROLE_SKILLS = {
    'python_developer':     {'required':['python','flask','sql','git','rest api'],'bonus':['docker','aws','postgresql','celery','django']},
    'web_developer':        {'required':['javascript','html','css','react','git'],'bonus':['node.js','mongodb','typescript','webpack']},
    'data_scientist':       {'required':['python','machine learning','sql','pandas','numpy'],'bonus':['tensorflow','pytorch','scikit-learn','aws']},
    'data_analyst':         {'required':['sql','python','excel','data visualization','statistics'],'bonus':['tableau','power bi','r','spark']},
    'devops_engineer':      {'required':['docker','linux','git','ci/cd','kubernetes'],'bonus':['aws','terraform','jenkins','nginx']},
    'full_stack_developer': {'required':['html','css','javascript','react','node.js','sql','git','rest api'],'bonus':['mongodb','docker','aws','typescript']},
    'frontend_developer':   {'required':['html','css','javascript','react','git'],'bonus':['typescript','webpack','figma','tailwind']},
    'backend_developer':    {'required':['python','sql','rest api','git','flask'],'bonus':['docker','redis','celery','aws']},
    'java_developer':       {'required':['java','spring boot','sql','git','rest api'],'bonus':['docker','aws','microservices','maven']},
    'software_engineer':    {'required':['python','data structures','algorithms','git','sql'],'bonus':['java','c++','system design','docker']},
    'cloud_engineer':       {'required':['aws','linux','docker','git','networking'],'bonus':['terraform','kubernetes','azure','gcp']},
    'ai_engineer':          {'required':['python','machine learning','nlp','tensorflow','git'],'bonus':['pytorch','hugging face','llm','aws']},
    'mobile_developer':     {'required':['react native','javascript','git','rest api','android'],'bonus':['flutter','ios','firebase','kotlin']},
    'cybersecurity_analyst':{'required':['networking','linux','security','git','python'],'bonus':['penetration testing','wireshark','kali linux','aws']},
    'qa_engineer':          {'required':['testing','automation','sql','git','python'],'bonus':['selenium','pytest','jira','postman']},
}

def detect_skills(resume_text, role_key):
    if role_key not in ROLE_SKILLS:
        return {'error': f'Unknown role: {role_key}'}
    text_lower  = resume_text.lower()
    role        = ROLE_SKILLS[role_key]
    required    = role['required']
    bonus       = role['bonus']
    detected    = [s for s in required if s in text_lower]
    missing     = [s for s in required if s not in text_lower]
    bonus_found = [s for s in bonus    if s in text_lower]
    coverage    = round(len(detected) / len(required) * 100) if required else 0
    return {'detected': detected, 'missing': missing, 'bonus': bonus_found, 'coverage_pct': coverage}

def get_available_roles():
    return [{'id': k, 'name': k.replace('_', ' ').title(), 'skills': v['required']} for k, v in ROLE_SKILLS.items()]
