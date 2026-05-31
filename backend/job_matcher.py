# job_matcher.py — Matches resume against a job description

COMMON_SKILLS = [
    'python','java','javascript','typescript','c++','c#','go','ruby','php','swift','kotlin',
    'react','angular','vue','node.js','flask','django','spring','fastapi','express',
    'sql','mysql','postgresql','mongodb','redis','sqlite','oracle',
    'docker','kubernetes','aws','azure','gcp','linux','git','ci/cd','jenkins','terraform',
    'html','css','rest api','graphql','microservices','agile','scrum',
    'machine learning','deep learning','nlp','tensorflow','pytorch','pandas','numpy','scikit-learn',
    'data analysis','tableau','power bi','excel','statistics',
    'react native','flutter','android','ios','firebase',
    'networking','security','penetration testing','bash','powershell',
    'selenium','pytest','junit','testing','automation',
]

def match_resume_to_jd(resume_text, jd_text):
    if not jd_text:
        return {'error': 'No job description provided.'}
    r_lower = resume_text.lower()
    j_lower = jd_text.lower()
    jd_skills      = [s for s in COMMON_SKILLS if s in j_lower]
    if not jd_skills:
        jd_skills  = [w for w in j_lower.split() if len(w) > 4][:20]
    matched        = [s for s in jd_skills if s in r_lower]
    missing        = [s for s in jd_skills if s not in r_lower]
    match_pct      = round(len(matched) / len(jd_skills) * 100) if jd_skills else 0
    return {'match_pct': match_pct, 'matched_keywords': matched, 'missing_keywords': missing}
