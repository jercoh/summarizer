from __future__ import division
import nltk
from textblob import TextBlob
from collections import defaultdict
from newspaper import Article
# from goose import Goose
# from BeautifulSoup import BeautifulSoup
# import urllib2
# from boilerpipe.extract import Extractor

class Summarizer():
	def __init__(self, url, only_nouns = False):
		self.scores = {}
		self.url = url
		self.article = Article(url)
		self.article.download()
		self.article.parse()
		self.text = self.article.text
		self.title = self.article.title
		self.sentences = []
		self.paragraphs = []
		self.split_into_paragraphs()
		self.paragraphs = self.group_small_paragraphs(3)
		self.split_into_sentences()
		self.compute_scores()

	def distance(self, sentence1, sentence2):
		""" returns the Jaccard distance between sentence1 and sentence2 """
		s1_words = sentence1.words
		s2_words = sentence2.words
		card_union = len(union(s1_words, s2_words))
		if card_union == 0:
			return 0
		return len(intersection(s1_words, s2_words)) / card_union

	def compute_scores(self):
		""" computes the distance between every couple of sentences """
		for sentence1 in self.sentences:
			scores = []
			for sentence2 in self.sentences:
				scores.append(self.distance(sentence1, sentence2))
			self.scores[sentence1] = (scores, sum(score for score in scores))


	def split_into_paragraphs(self):
		""" compute an array of paragraphs """
		self.paragraphs = [x for x in self.text.split('\n\n') if x != '']

	def group_small_paragraphs(self, limit):
		l = self.paragraphs
		first_index = 0
		second_index = 0
		if len(l) <= 1:
			return l
		while first_index < len(l):
			if len(TextBlob(l[first_index]).sentences) <= limit and first_index != len(l) - 1:
				second_index = first_index + 1
				p = l[first_index] + ' ' + l[second_index]
				while len(TextBlob(p).sentences) <= limit and second_index < len(l) -1:
					second_index += 1
					p += ' ' + l[second_index]
				l = l[:first_index] + [p] + l[second_index+1:]
				first_index = 0 
				second_index = 0
			else:
				first_index += 1
				second_index += 1
		return l

	##################################
	# compress a list 				 #
	# [1,1,2,3,1,2,5] ----> [4,3,3,5]#
	##################################
	def zip(l):
		first_index = 0
		second_index = 0
		if len(l) <= 1:
			return l
		while first_index < len(l):
			if l[first_index] <= 2 and first_index != len(l) - 1:
				second_index = first_index + 1
				p = l[first_index] + l[second_index]
				while p <= 2 and second_index < len(l) -1:
					second_index += 1
					p += l[second_index]
				l = l[:first_index] + [p] + l[second_index+1:]
				first_index = 0 
				second_index = 0
			else:
				first_index += 1
				second_index += 1
		return l




	def split_into_sentences(self):
		sentences = []
		for p in self.paragraphs:
			sentences += TextBlob(p).sentences
		self.sentences = sentences

	def summarize(self):
		""" summarizes the article """
		summary = ""
		for paragraph in self.paragraphs:
			key_sentence = None
			max_score = 0
			for sentence in TextBlob(paragraph).sentences:
				score = self.scores[sentence][1]
				if score >= max_score:
					max_score = score
					key_sentence = sentence
			summary += '<p>'+str(key_sentence).decode("utf-8")+'</p>\n'
		return summary

def union(a,b):
	""" returns the union of two lists """
	return list(set(a) | set(b))

def intersection(a,b):
	""" returns the intersection of two lists """
	return list(set(a) & set(b))

def unique(a):
    """ returns the list with duplicate elements removed """
    return list(set(a))

