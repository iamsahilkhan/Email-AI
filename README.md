## Overview
The Email Template Generator is a Python application that leverages OpenAI to create email templates based on user inputs. The application allows users to specify the campaign goal, business tone, industry, and additional information for customization. It also provides the option to include content from a company's website URL. The templates are generated using OpenAI's text generation capabilities, and the summarization of website content is performed using NLTK (Natural Language Toolkit).


## Libraries Used
The project utilizes several libraries to achieve its functionality:
1. OpenAI (openai): This library provides access to the OpenAI GPT-3 API, allowing the application to generate text based on prompts.
2. Requests (requests): The Requests library is used to make HTTP requests, enabling the application to fetch website content.
3. BeautifulSoup (bs4): BeautifulSoup is used for parsing and scraping website content, particularly the "About" section.
4. NLTK (nltk): The Natural Language Toolkit library is used for text processing and summarization.
5. PrettyTable (prettytable): This library is used to create well-formatted tables for displaying generated email templates.


## Project Flow
1. User is welcomed to the Email Template Generator.
2. User is prompted to choose campaign goal, business tone, industry, and other details.
3. User is given the option to enter a company's website URL for additional information.
4. Website content is scraped and summarized (if URL provided).
5. User is prompted to enter additional information.
6. Email templates are generated based on user inputs using OpenAI.
7. Templates are displayed in a well-formatted table using PrettyTable.
