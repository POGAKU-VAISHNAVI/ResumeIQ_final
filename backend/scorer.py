# scorer.py — Calculates resume score out of 100

def calculate_score(resume_text, skill_result):
    text_lower = resume_text.lower()
    coverage   = skill_result.get('coverage_pct', 0)

    # Sections (20 pts)
    section_keys = ['education','skills','experience','projects','contact','summary']
    section_hits = sum(1 for k in section_keys if k in text_lower)
    sections_score = min(20, section_hits * 4)

    # Skills match (25 pts)
    skills_score = round(coverage / 100 * 25)

    # Projects (20 pts)
    project_words = ['project','built','developed','created','implemented','github']
    project_hits  = sum(1 for w in project_words if w in text_lower)
    projects_score = min(20, project_hits * 4)

    # Experience (20 pts)
    exp_words = ['internship','intern','experience','worked','company','role','position']
    exp_hits  = sum(1 for w in exp_words if w in text_lower)
    exp_score = min(20, exp_hits * 4)

    # ATS keywords (15 pts)
    ats_words = ['python','java','javascript','sql','git','docker','aws','react','flask','linux']
    ats_hits  = sum(1 for w in ats_words if w in text_lower)
    ats_score = min(15, ats_hits * 2)

    total = sections_score + skills_score + projects_score + exp_score + ats_score

    if total >= 85: grade, label = 'A+', 'Excellent'
    elif total >= 75: grade, label = 'A',  'Strong'
    elif total >= 60: grade, label = 'B',  'Good'
    elif total >= 45: grade, label = 'C',  'Average'
    else:             grade, label = 'D',  'Needs Work'

    return {
        'total': total, 'grade': grade, 'label': label,
        'breakdown': {
            'sections':     {'score': sections_score},
            'skills':       {'score': skills_score},
            'projects':     {'score': projects_score},
            'experience':   {'score': exp_score},
            'ats_keywords': {'score': ats_score},
        }
    }
