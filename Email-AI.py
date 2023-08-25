import openai
import requests
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from prettytable import PrettyTable
from bs4 import BeautifulSoup

# Initialize OpenAI API
openai.api_key = ""

# Function to scrape website's data
def scrape_website_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        visible_text = []

        for element in soup.find_all(string=True):
            if element.parent.name not in ['script', 'style']:
                visible_text.append(element.strip())

        return ' '.join(filter(None, visible_text))
    else:
        return None


# Function to convert all the website's data into a paragraph
def format_into_paragraphs(text, paragraph_length=100):
    paragraphs = text.split('\n\n')  # Split text into paragraphs based on double line breaks
    formatted_paragraphs = []

    for paragraph in paragraphs:
        sentences = paragraph.split('.')
        current_paragraph = ""

        for sentence in sentences:
            if len(current_paragraph + sentence) <= paragraph_length:
                current_paragraph += sentence.strip() + ". "
            else:
                formatted_paragraphs.append(current_paragraph.strip())
                current_paragraph = sentence.strip() + ". "

        if current_paragraph:
            formatted_paragraphs.append(current_paragraph.strip())

    return "\n\n".join(formatted_paragraphs)


# Function to summarize the paragraph
def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stopwords.words("english")]

    frequency_dist = FreqDist(words)
    sentence_scores = {}

    for i, sentence in enumerate(sentences):
        for word, freq in frequency_dist.items():
            if word in sentence.lower():
                if i in sentence_scores:
                    sentence_scores[i] += freq
                else:
                    sentence_scores[i] = freq

    sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    top_sentences = [sentences[index] for index, _ in sorted_scores[:num_sentences]]

    return " ".join(top_sentences)


# Function to generate a single email template using NLTK for summarization
def generate_email_template(campaign_goal, business_tone, industry, additional_info=None, website_url=None):
    prompt_1 = f"Write an amazing and convincing email template with a {business_tone} tone for a {industry} company. The goal of the campaign is to {campaign_goal}"
    prompt_2 = f"I want you to write a persuasive email template with a {business_tone} tone for a {industry} company. The goal of the campaign is to {campaign_goal}"
    prompt_3 = f"Imagine you're an email marketing specialist. Craft an email template with a warm and inviting {business_tone} tone for a {industry} business. The goal of the campaign is to {campaign_goal}"
    prompt_4 = f"You are an expert in writing emails and I want you to write an email template with a {business_tone} tone for a {industry} company, such that the template makes its receivers to open the email. The goal of the campaign is to {campaign_goal}"
    prompt_5 = f"Compose an email to with a {business_tone} tone for a {industry} company. The goal of the campaign is {campaign_goal} and make sure to keep the email short and eye-catchy."

    prompts = [prompt_1, prompt_2, prompt_3, prompt_4, prompt_5]
    templates = []

    if website_url:
        website_content = scrape_website_content(website_url)
        formatted_content = format_into_paragraphs(website_content)
        summarized_content = summarize_text(formatted_content)
    else:
        summarized_content = None

    for prompt in prompts:
        if summarized_content:
            prompt += f" The summarized website content includes: {summarized_content}"
        if additional_info:
            prompt += f" Here's some additional information: {additional_info}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        templates.append(response.choices[0].text.strip())

    return templates


# Main function
def main():
    print("Welcome to the Email Template Generator!")

    # User inputs
    campaign_goal_options = [
        "Convince to buy product",
        "Recover churned customers",
        "Teach a new concept",
        "Onboard users",
        "Share product updates"
    ]
    business_tone_options = ["formal", "informal"]
    industry_options = [
        "Technology",
        "Finance",
        "Marketing",
        "Education",
        "Consulting",
        "IT Services",
        "Healthcare"
    ]

    print("Choose a campaign goal:")
    for i, option in enumerate(campaign_goal_options, start=1):
        print(f"{i}. {option}")
    campaign_choice = int(input()) - 1
    campaign_goal = campaign_goal_options[campaign_choice]

    print("\nChoose a business tone:")
    for i, option in enumerate(business_tone_options, start=1):
        print(f"{i}. {option}")
    tone_choice = int(input()) - 1
    business_tone = business_tone_options[tone_choice]

    print("\nChoose an industry:")
    for i, option in enumerate(industry_options, start=1):
        print(f"{i}. {option}")
    industry_choice = int(input()) - 1
    industry = industry_options[industry_choice]

    website_url = input("\nEnter the company's website URL (Optional, press Enter to skip): ")
    if website_url:
        website_content = scrape_website_content(website_url)
        print("Website content:\n", website_content)
        about_text = format_into_paragraphs(website_content)
    else:
        about_text = None

    additional_info = input("\nEnter additional information to include (Optional, press Enter to skip): ")

    # Generate and display templates
    templates = generate_email_template(campaign_goal, business_tone, industry, additional_info, website_url)

    table = PrettyTable()
    table.field_names = ["Template Number", "Generated Template"]

    for i, template in enumerate(templates, start=1):
        table.add_row([f"Template {i}", template])

    # Print the table
    print("\nGenerated Email Templates:")
    print(table)


if __name__ == "__main__":
    main()