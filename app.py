from flask import Flask, request, render_template, jsonify
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


chain = Chain()
portfolio = Portfolio()
app = Flask(__name__)

# Sample function to generate cold email content
def generate_cold_email(link):
    # Simulated email generation logic
    return f"""
    Hi [Name],

    I came across your website {link} and was impressed by your [specific detail, e.g., innovative projects, product line, or achievements]. 
    I would love to discuss how my [services/products] can help you achieve [specific goals or solve challenges].

    Looking forward to hearing from you!

    Best regards,  
    [Your Name]  
    """

# Route for rendering the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API route to generate a cold email
@app.route('/generate_email', methods=['POST'])
def generate_email():
    data = request.json
    link = data.get('link')

    if not link:
        return jsonify({"error": "Please provide a valid link"}), 400

    loader = WebBaseLoader([link])
    data = clean_text(loader.load().pop().page_content)
    
    portfolio.load_portfolio()
    jobs = chain.extract_jobs(data)
    
    for job in jobs:
        skills = job.get('skills',[])
        links = portfolio.query_links(skills)
        email = chain.write_mail(job, links)

    print('=======================================')
    print(email)
    print('=======================================')

    return jsonify({"email": email})

if __name__ == '__main__':
    app.run(debug=True)
