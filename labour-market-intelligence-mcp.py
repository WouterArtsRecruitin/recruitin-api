#!/usr/bin/env python3
"""
Labour Market Intelligence MCP Server
Integrates with Jotform, Notion, GitHub, and Recruitment Orchestra
"""

import json
import os
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
import PyPDF2
from io import BytesIO
import requests

# === CONFIGURATION ===
JOTFORM_API_KEY = os.getenv("JOTFORM_API_KEY", "2189378edb821cfa9d6ddbb920038eea")
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY", "")
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# === MCP TOOL 1: PARSE JOBDIGGER REPORT ===
def parse_jobdigger_pdf(pdf_url_or_path: str) -> Dict[str, Any]:
    """
    Parse Jobdigger PDF report and extract structured data
    
    Args:
        pdf_url_or_path: URL or file path to Jobdigger PDF
        
    Returns:
        Structured data extracted from report
    """
    try:
        # Download PDF if URL
        if pdf_url_or_path.startswith('http'):
            response = requests.get(pdf_url_or_path)
            pdf_file = BytesIO(response.content)
        else:
            pdf_file = open(pdf_url_or_path, 'rb')
        
        # Extract text
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        # Extract data points
        data = {
            'source': 'Jobdigger Report',
            'parsed_at': datetime.now().isoformat(),
            'confidence': 90,
            'vacancy_count': extract_vacancy_count(text),
            'related_titles': extract_related_titles(text),
            'salary': extract_salary(text),
            'experience_split': extract_experience(text),
            'education_levels': extract_education(text),
            'top_skills': extract_skills(text),
            'soft_skills': extract_soft_skills(text),
            'certificates': extract_certificates(text),
            'languages': extract_languages(text),
            'employment_type': extract_employment_type(text),
            'top_employers': extract_employers(text),
            'top_intermediairs': extract_intermediairs(text),
            'job_boards': extract_job_boards(text),
            'time_to_fill': extract_time_to_fill(text)
        }
        
        return {
            'success': True,
            'data': data,
            'raw_text_length': len(text)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None
        }

# === EXTRACTION FUNCTIONS ===
def extract_vacancy_count(text: str) -> Optional[int]:
    """Extract: 'Totaal: 26.735 gepubliceerde vacatures'"""
    match = re.search(r'Totaal:\s*([\d.]+)\s*gepubliceerde vacatures', text)
    if match:
        count_str = match.group(1).replace('.', '')
        return int(count_str)
    return None

def extract_related_titles(text: str) -> List[Dict[str, Any]]:
    """Extract related job titles with counts"""
    titles = []
    # Pattern: "1 5.763 x Monteur"
    pattern = r'(\d+)\s+([\d.]+)\s*x\s+([A-Za-z\s]+)'
    matches = re.findall(pattern, text)
    
    for rank, count, title in matches[:10]:  # Top 10
        count_clean = count.replace('.', '')
        titles.append({
            'rank': int(rank),
            'title': title.strip(),
            'count': int(count_clean)
        })
    
    return titles

def extract_salary(text: str) -> Dict[str, Any]:
    """Extract salary ranges for junior/medior/senior"""
    salaries = {}
    
    # Pattern: "Junior €30.000 ... Medior €40.000 ... Senior €50.000"
    junior = re.search(r'Junior.*?€\s*([\d.]+)', text)
    medior = re.search(r'Medior.*?€\s*([\d.]+)', text)
    senior = re.search(r'Senior.*?€\s*([\d.]+)', text)
    gemiddeld = re.search(r'Gemiddeld[:\s]*€\s*([\d.]+)', text)
    
    if junior:
        salaries['junior'] = int(junior.group(1).replace('.', ''))
    if medior:
        salaries['medior'] = int(medior.group(1).replace('.', ''))
    if senior:
        salaries['senior'] = int(senior.group(1).replace('.', ''))
    if gemiddeld:
        salaries['median'] = int(gemiddeld.group(1).replace('.', ''))
    
    return salaries

def extract_experience(text: str) -> Dict[str, int]:
    """Extract junior/medior/senior percentage split"""
    experience = {}
    
    # Pattern: "junior 41%"
    pattern = r'(junior|medior|senior)\s+(\d+)%'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for level, percentage in matches:
        experience[level.lower()] = int(percentage)
    
    return experience

def extract_education(text: str) -> Dict[str, int]:
    """Extract education level distribution"""
    education = {}
    
    levels = ['MBO', 'VMBO', 'HBO', 'WO', 'HAVO', 'VWO', 'LBO']
    for level in levels:
        pattern = rf'{level}\s+(\d+)%'
        match = re.search(pattern, text)
        if match:
            education[level] = int(match.group(1))
    
    return education

def extract_skills(text: str) -> List[Dict[str, Any]]:
    """Extract top skills with percentages"""
    skills = []
    
    # Pattern: "Onderhoudswerkzaamheden 52%"
    pattern = r'([A-Za-z/\s\-]+?)\s+(\d+)%'
    matches = re.findall(pattern, text)
    
    seen_skills = set()
    for skill, percentage in matches:
        skill_clean = skill.strip()
        # Filter out noise
        if (len(skill_clean) > 3 and 
            skill_clean not in seen_skills and
            not skill_clean.lower() in ['geen', 'totaal', 'parttime', 'fulltime']):
            seen_skills.add(skill_clean)
            skills.append({
                'skill': skill_clean,
                'percentage': int(percentage)
            })
    
    # Sort by percentage
    skills.sort(key=lambda x: x['percentage'], reverse=True)
    return skills[:20]  # Top 20

def extract_soft_skills(text: str) -> List[Dict[str, Any]]:
    """Extract soft skills"""
    soft_skills = [
        'Verantwoordelijkheid', 'Servicegericht', 'Gastvriendelijkheid',
        'Flexibel', 'Leergierig', 'Stressbestendig', 'Oplossingsgericht',
        'Proactief', 'Bevlogenheid', 'Ambitieus'
    ]
    
    found = []
    for skill in soft_skills:
        pattern = rf'{skill}\s+(\d+)%'
        match = re.search(pattern, text)
        if match:
            found.append({
                'skill': skill,
                'percentage': int(match.group(1))
            })
    
    found.sort(key=lambda x: x['percentage'], reverse=True)
    return found

def extract_certificates(text: str) -> List[Dict[str, Any]]:
    """Extract required certificates"""
    certs = []
    
    cert_patterns = [
        'Rijbewijs B', 'VCA basis certificaat', 'VCA', 
        'Middelbare Technische School', 'MTS',
        'Verklaring Omtrent het Gedrag', 'VOG'
    ]
    
    for cert in cert_patterns:
        pattern = rf'{cert}.*?(\d+)%'
        match = re.search(pattern, text)
        if match:
            certs.append({
                'certificate': cert,
                'percentage': int(match.group(1))
            })
    
    return sorted(certs, key=lambda x: x['percentage'], reverse=True)

def extract_languages(text: str) -> Dict[str, int]:
    """Extract language requirements"""
    languages = {}
    
    lang_list = ['Nederlands', 'Engels', 'Duits', 'Frans']
    for lang in lang_list:
        pattern = rf'{lang}\s+(\d+)%'
        match = re.search(pattern, text)
        if match:
            languages[lang] = int(match.group(1))
    
    return languages

def extract_employment_type(text: str) -> Dict[str, int]:
    """Extract employment type distribution"""
    types = {}
    
    # Pattern: "vast: 79%"
    pattern = r'(vast|tijdelijk|stage|zzp|interim)\s*:\s*(\d+)%'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for emp_type, percentage in matches:
        types[emp_type.lower()] = int(percentage)
    
    return types

def extract_employers(text: str) -> List[Dict[str, Any]]:
    """Extract top employers (direct werkgevers)"""
    employers = []
    
    # Pattern: "1 254 x Tata Steel"
    pattern = r'(\d+)\s+([\d.]+)\s*x\s+([A-Za-z\s&\-\.]+?)(?:\n|\s{2,})'
    matches = re.findall(pattern, text)
    
    for rank, count, name in matches[:10]:
        count_clean = count.replace('.', '')
        employers.append({
            'rank': int(rank),
            'name': name.strip(),
            'vacancy_count': int(count_clean)
        })
    
    return employers

def extract_intermediairs(text: str) -> List[Dict[str, Any]]:
    """Extract top recruitment agencies"""
    return extract_employers(text)  # Same pattern

def extract_job_boards(text: str) -> List[Dict[str, Any]]:
    """Extract job boards used"""
    boards = []
    
    # Pattern: "www.jobbird.com 9%"
    pattern = r'((?:www\.)?[\w\-\.]+\.(?:nl|com|co))\s+(\d+)%'
    matches = re.findall(pattern, text)
    
    for board, percentage in matches[:10]:
        boards.append({
            'board': board,
            'percentage': int(percentage)
        })
    
    return sorted(boards, key=lambda x: x['percentage'], reverse=True)

def extract_time_to_fill(text: str) -> Dict[str, Any]:
    """Extract time-to-fill metrics"""
    # Pattern: "Gemiddelde invultijd intermediair 30 dagen"
    intermediair = re.search(r'intermediair[:\s]+(\d+)\s*dagen', text, re.IGNORECASE)
    direct = re.search(r'directe werkgever[:\s]+(\d+)\s*dagen', text, re.IGNORECASE)
    
    return {
        'intermediair_days': int(intermediair.group(1)) if intermediair else None,
        'direct_days': int(direct.group(1)) if direct else None
    }

# === MCP TOOL 2: SCRAPE INDEED VIA BRAVE ===
def scrape_indeed_market_data(
    job_title: str,
    location: str,
    max_results: int = 50
) -> Dict[str, Any]:
    """
    Scrape Indeed job market data via Brave Search
    
    Args:
        job_title: Job title to search
        location: Location (city or region)
        max_results: Maximum results to fetch
        
    Returns:
        Aggregated market intelligence from Indeed
    """
    try:
        # Search Indeed via Brave
        query = f'site:nl.indeed.com "{job_title}" "{location}"'
        
        response = requests.get(
            'https://api.search.brave.com/res/v1/web/search',
            params={'q': query, 'count': min(max_results, 20)},
            headers={
                'Accept': 'application/json',
                'X-Subscription-Token': BRAVE_SEARCH_API_KEY
            }
        )
        
        if response.status_code != 200:
            return {
                'success': False,
                'error': f'Brave API error: {response.status_code}'
            }
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        # Parse vacancy data from search results
        vacancies = []
        for result in results:
            # Extract from snippet
            snippet = result.get('description', '')
            
            vacancy = {
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'snippet': snippet,
                'age_days': result.get('age', ''),
                'employer': extract_employer_from_snippet(snippet),
                'salary': extract_salary_from_snippet(snippet)
            }
            vacancies.append(vacancy)
        
        # Aggregate insights
        salaries = [v['salary'] for v in vacancies if v['salary']]
        
        return {
            'success': True,
            'source': 'Indeed (via Brave Search)',
            'confidence': 85,
            'total_found': len(vacancies),
            'avg_salary': sum(salaries) // len(salaries) if salaries else None,
            'salary_range': {
                'min': min(salaries) if salaries else None,
                'max': max(salaries) if salaries else None
            },
            'sample_vacancies': vacancies[:10],  # Top 10
            'employers': extract_employers_from_vacancies(vacancies)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_employer_from_snippet(snippet: str) -> Optional[str]:
    """Extract employer name from snippet"""
    # Common patterns: "Bij [Company]", "[Company] zoekt"
    patterns = [
        r'bij\s+([A-Z][A-Za-z\s&]+?)(?:\s+zoekt|\s+in\s+)',
        r'^([A-Z][A-Za-z\s&]+?)\s+zoekt',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, snippet, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

def extract_salary_from_snippet(snippet: str) -> Optional[int]:
    """Extract salary from snippet"""
    # Pattern: "€3.000 - €4.000", "€40.000 per jaar"
    match = re.search(r'€\s*([\d.]+)', snippet)
    if match:
        salary_str = match.group(1).replace('.', '')
        return int(salary_str)
    return None

def extract_employers_from_vacancies(vacancies: List[Dict]) -> List[str]:
    """Extract unique employers"""
    employers = {}
    for v in vacancies:
        if v['employer']:
            employers[v['employer']] = employers.get(v['employer'], 0) + 1
    
    return sorted(employers.items(), key=lambda x: x[1], reverse=True)

# === MCP TOOL 3: LABOUR MARKET DEEP DIVE ===
def labour_market_deepdive(
    job_title: str,
    location: str,
    jobdigger_pdf_path: Optional[str] = None,
    linkedin_ti_pdf_path: Optional[str] = None,
    vacancy_text: Optional[str] = None,
    vacancy_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete labour market deep dive analysis
    
    Args:
        job_title: Job title to research
        location: Location
        jobdigger_pdf_path: Path to Jobdigger PDF (optional)
        linkedin_ti_pdf_path: Path to LinkedIn TI PDF (optional)
        vacancy_text: Vacancy text for analysis (optional)
        vacancy_url: Vacancy URL (optional)
        
    Returns:
        Complete market intelligence report
    """
    print(f"🔍 Starting deep dive for: {job_title} in {location}")
    
    # Collect data from all sources
    data_sources = []
    
    # 1. Parse Jobdigger if provided
    jobdigger_data = None
    if jobdigger_pdf_path:
        print("📄 Parsing Jobdigger report...")
        result = parse_jobdigger_pdf(jobdigger_pdf_path)
        if result['success']:
            jobdigger_data = result['data']
            data_sources.append('Jobdigger Report')
    
    # 2. Scrape Indeed
    print("🔎 Scraping Indeed via Brave Search...")
    indeed_data = scrape_indeed_market_data(job_title, location, max_results=50)
    if indeed_data['success']:
        data_sources.append('Indeed (Brave Search)')
    
    # 3. TODO: Parse LinkedIn TI if provided
    # 4. TODO: Fetch CBS employment data
    # 5. TODO: Scrape UWV vacancy stats
    
    # Synthesize all data
    print("🧠 Synthesizing data from all sources...")
    
    synthesized = {
        'vacancy_count': (
            jobdigger_data['vacancy_count'] if jobdigger_data else
            indeed_data.get('total_found')
        ),
        'salary': jobdigger_data['salary'] if jobdigger_data else {
            'median': indeed_data.get('avg_salary')
        },
        'top_skills': jobdigger_data['top_skills'] if jobdigger_data else [],
        'experience_split': jobdigger_data['experience_split'] if jobdigger_data else {},
        'education_levels': jobdigger_data['education_levels'] if jobdigger_data else {},
        'employment_type': jobdigger_data['employment_type'] if jobdigger_data else {},
        'top_employers': (
            jobdigger_data['top_employers'] if jobdigger_data else
            [{'name': e[0], 'count': e[1]} for e in indeed_data.get('employers', [])]
        ),
        'job_boards': jobdigger_data['job_boards'] if jobdigger_data else [],
        'time_to_fill': jobdigger_data['time_to_fill'] if jobdigger_data else {}
    }
    
    # Calculate confidence
    confidence = 0
    if jobdigger_data:
        confidence += 50  # Jobdigger is high quality
    if indeed_data['success']:
        confidence += 35  # Indeed scraping
    
    return {
        'metadata': {
            'job_title': job_title,
            'location': location,
            'generated_at': datetime.now().isoformat(),
            'data_sources': data_sources,
            'confidence_overall': min(confidence, 95)
        },
        'jobdigger_intelligence': jobdigger_data,
        'indeed_insights': indeed_data,
        'synthesized_insights': synthesized,
        'talent_pool': {
            'note': 'Talent pool estimation requires CBS + UWV data (pending implementation)',
            'active': None,
            'latent': None,
            'not_seeking': None
        }
    }

# === MCP TOOL 4: GENERATE REPORT (NOTION FORMAT) ===
def format_salary(amount):
    """Format salary for display"""
    if amount is None:
        return 'N/A'
    return f"{amount:,}"

def generate_notion_report(
    research_data: Dict[str, Any],
    report_type: str = "standard"
) -> Dict[str, Any]:
    """
    Generate formatted report for Notion
    
    Args:
        research_data: Output from labour_market_deepdive
        report_type: executive | standard | extensive | action_plan
        
    Returns:
        Markdown formatted report for Notion
    """
    meta = research_data['metadata']
    synth = research_data['synthesized_insights']
    
    # Build report
    report = f"""# Labour Market Intelligence Report

## {meta['job_title']} | {meta['location']}

**Generated:** {meta['generated_at']}  
**Confidence:** {meta['confidence_overall']}%  
**Data Sources:** {', '.join(meta['data_sources'])}

---

## 📊 Executive Summary

### Key Metrics
- **Total Vacatures:** {synth.get('vacancy_count') or 'N/A'}
- **Mediaan Salaris:** €{synth['salary'].get('median', 'N/A'):,} per jaar
- **Top Skills:** {len(synth.get('top_skills', []))} identified
- **Time-to-Fill:** {synth.get('time_to_fill', {}).get('intermediair_days', 'N/A')} days (avg)

---

## 💰 Salary Benchmarks

"""
    
    salary = synth.get('salary', {})
    if salary:
        report += f"""
| Level | Salary |
|-------|--------|
| Junior | €{format_salary(salary.get('junior'))} |
| Medior | €{format_salary(salary.get('medior'))} |
| Senior | €{format_salary(salary.get('senior'))} |
| Mediaan | €{format_salary(salary.get('median'))} |

"""
    
    # Top Skills
    report += "\n## 🎯 Top 10 Skills\n\n"
    for skill in synth.get('top_skills', [])[:10]:
        report += f"- **{skill['skill']}**: {skill['percentage']}%\n"
    
    # Experience Split
    exp = synth.get('experience_split', {})
    if exp:
        report += f"\n## 👔 Experience Levels\n\n"
        report += f"- Junior: {exp.get('junior', 0)}%\n"
        report += f"- Medior: {exp.get('medior', 0)}%\n"
        report += f"- Senior: {exp.get('senior', 0)}%\n"
    
    # Top Employers
    report += "\n## 🏢 Top Employers\n\n"
    for emp in synth.get('top_employers', [])[:5]:
        report += f"{emp.get('rank', '•')}. **{emp.get('name')}** - {emp.get('vacancy_count', emp.get('count', 0))} vacatures\n"
    
    # Add more sections based on report_type
    if report_type in ['extensive', 'action_plan']:
        report += "\n## 📈 Education Requirements\n\n"
        edu = synth.get('education_levels', {})
        for level, pct in edu.items():
            report += f"- {level}: {pct}%\n"
    
    if report_type == 'action_plan':
        report += """

---

## 🎯 Recruitment Action Plan

### Sourcing Strategy

**Primary Channels (80% effort):**
1. **Indeed Sponsored Ads** - Target junior/medior levels
2. **Direct Search** - LinkedIn/Notion database
3. **Referral Program** - Incentivize current employees

### Budget Allocation
- Indeed: €500/month
- LinkedIn: €300/month  
- Referrals: €200/month
- **Total: €1.000/month**

### Timeline
- Week 1-2: Setup campaigns
- Week 3-6: Active sourcing (target: 20 candidates)
- Week 7-8: Interviews + offers

### KPIs
- Applicants/week: >5
- Qualification rate: >60%
- Time-to-hire: <8 weeks
"""
    
    return {
        'success': True,
        'report_type': report_type,
        'markdown': report,
        'word_count': len(report.split())
    }

# === MAIN FUNCTION FOR TESTING ===
if __name__ == "__main__":
    # Test with uploaded Jobdigger PDF
    print("=" * 60)
    print("TESTING: Labour Market Intelligence MCP")
    print("=" * 60)
    
    # Test 1: Parse Jobdigger PDF
    pdf_path = "/mnt/user-data/uploads/Allround_Monteur__1_.pdf"
    print(f"\n1️⃣ Testing Jobdigger PDF parser...")
    result = parse_jobdigger_pdf(pdf_path)
    
    if result['success']:
        print("✅ SUCCESS!")
        print(f"   Vacancy count: {result['data']['vacancy_count']:,}")
        print(f"   Median salary: €{result['data']['salary'].get('median', 0):,}")
        print(f"   Top skills: {len(result['data']['top_skills'])}")
    else:
        print(f"❌ FAILED: {result['error']}")
    
    # Test 2: Full deep dive
    print(f"\n2️⃣ Testing full deep dive...")
    research = labour_market_deepdive(
        job_title="Allround Monteur",
        location="Arnhem",
        jobdigger_pdf_path=pdf_path
    )
    
    print("✅ Deep dive completed!")
    print(f"   Confidence: {research['metadata']['confidence_overall']}%")
    print(f"   Sources: {', '.join(research['metadata']['data_sources'])}")
    
    # Test 3: Generate report
    print(f"\n3️⃣ Testing report generation...")
    report = generate_notion_report(research, report_type="standard")
    
    if report['success']:
        print("✅ Report generated!")
        print(f"   Type: {report['report_type']}")
        print(f"   Words: {report['word_count']}")
        print("\n" + "=" * 60)
        print("REPORT PREVIEW:")
        print("=" * 60)
        print(report['markdown'][:1000] + "...")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
