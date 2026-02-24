import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text


def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(similarity[0][0] * 100, 2)


def get_missing_keywords(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    important_words = [word for word in jd_words if len(word) > 4]
    missing = [word for word in important_words if word not in resume_words]

    return list(set(missing))[:10]


def get_matched_keywords(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())

    matched = [word for word in jd_words if word in resume_words and len(word) > 4]

    return list(set(matched))[:10]


def calculate_ats_score(resume_text):
    score = 100
    word_count = len(resume_text.split())

    if word_count < 300:
        score -= 15

    if "skills" not in resume_text.lower():
        score -= 15

    if "projects" not in resume_text.lower():
        score -= 10

    if "education" not in resume_text.lower():
        score -= 10

    return max(score, 0)