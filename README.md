## Synopsis
Summarize any news article

The user flow is as follows:
- Shoose a URL
- Enter URL in the textbox
- Click on the “Summarize” button
- Read your summary

## Installation

- pip install -r requirements.txt
- python download_data.py

## Instructions
As soon as you've got all the files downloaded you just need to run this command:
```
python api.py
```
Then open ```http://localhost:5000```.

## Features
- NLP using ```TextBlog```
- Responsive design
- Articles are extracted using ```newspaper``` library
- Main img and title are extracted as well
- Backend: ```Flask``` microframework

## Algorithm:
1. I split the text into sentences
2. I calculate an individual score for each sentence and store it in a key-value dictionary, where the sentence itself is the key and the value is the total score. The total score is just the sum of all its intersections with the other sentences in the text (not including itself).
3. I split the text into paragraphs (paragraphs have a min size of 3 sentences).
4. I choose the best sentence from each paragraph according to our sentences dictionary.

## Why is that working?
- The first (and obvious) reason is that a paragraph is a logical atomic unit of the text. In simple words – there is probably a very good reason why the author decided to split his text that way.
- if two sentences have a good intersection, they probably holds the same information. So if one sentence has a good intersection with many other sentences, it probably holds some information from each one of them- or in other words, this is probably a key sentence in our text!

## Future improvements:
- Find a better way to extract article text
- Modify intersection function and see how it improves the summarizer
- Play with the min-size of a paragraph
- Improve UX/UI
- Group paragraphs considering their intersection
- Use only nouns in Jaccard distance
