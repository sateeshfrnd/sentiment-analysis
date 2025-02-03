# Sentiment Analysis on Twitter/X

## Overview
This project aims to **scrape tweets**  and perform **sentiment analysis** using **TextBlob**. 
Instead of using `tweepy`, which requires API keys and has strict limitations, I leveraged `twkit`, which enables large-scale scraping without restrictions.
The goal is to analyze public sentiment in real-time while exploring **NLP and Generative AI** techniques.

## Why This Project?
- Extracting public sentiment on a trending topic
- Learning how to bypass Twitter API limitations
- Exploring NLP & Generative AI concepts through real-world data
  
Twitter/X has imposed strict API limitations, making it difficult to scrape data without paid access. Instead of using `tweepy`, which requires API keys, I used `twkit`, which allows fetching **1,000,000 tweets** without hitting rate limits or bans.

## Tech Stack:
- Scraping: twkit (No API keys needed)
- Data Processing: pandas
- Sentiment Analysis: TextBlob (with future plans for VADER, BERT)
- Storage: CSV

## Getting Started
### Prerequisites
- Python 3.8+
- Twitter/X account credentials

### Setup
Follow these steps:
1. Clone this repository to your local machine using the following command:
```
git clone https://github.com/sateeshfrnd/sentiment-analysis.git
```
2. Install the required dependencies by running:
```
pip install -r requirements.txt
```
3. Updae Configure for the authentication
```
Update config.ini with twitter/X credentails 
```
4. Explore the python script
```
python run_analysis.py
```


## Repository Structure
- run_analysis.py: Python scripts for scraping and analysis
- requirements.txt : List of necessary libraries.
- README.md: File provides an overview of this repo and instructions for getting started.


## Future Enhancements
- Implement VADER for better social media sentiment detection.
- Use Hugging Face Transformers (BERT/RoBERTa) for deep learning-based sentiment analysis.
- Create a dashboard to visualize insights dynamically.

