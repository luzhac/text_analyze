
from pymongo import MongoClient
import jieba
import operator
from collections import OrderedDict
from nltk.stem.porter import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import math
from wordcloud import WordCloud
import matplotlib.pyplot as plt


nltk.download('stopwords')
nltk.download('punkt')

client = MongoClient("mongodb://localhost:27017/")
database = client["test"]
collection = database["people"]

def head_seg(seg_list,num1):
	keyword_dict={}
	for seg in seg_list:
		if seg:
			if seg in keyword_dict:
				keyword_dict[seg]=keyword_dict[seg]+1
			else:
				keyword_dict[seg]=1
	b = OrderedDict(sorted(keyword_dict.items(),key=lambda item:item[1], reverse=True))
	itertor=iter(b.items())
	top_result={}
	for i in range(num1):
		a=next(itertor)
		top_result[a[0]]=a[1]
		
	return top_result
def count_term(text):
	tokens=nltk.word_tokenize(text)
	stop_words=set(stopwords.words('english'))
	 
	stop_words.extend([',','-','.','(',')',';','/','&','amp','A'])
	filtered_words=[w for w in tokens if not w in stop_words]
 
	stemmer=PorterStemmer()
	seg_list=[stemmer.stem(w) for w in filtered_words]
	count=Counter(seg_list)
	return count
def tfidf(word,count,count_list):
	tf=count[word]/sum(count.values())
	idf=math.log(len(count_list)/(1+sum(1 for count in count_list if word in count)))
	return tf*idf


def word_tfidf_freq():
	query = {}
	sort = [ (u"price", 1) ]

	text=''
	count_list=[] # seg word:frequency in sentence 
	cursor = collection.find(query, sort = sort)
	try:
	    for doc in cursor:
	    	count_list.append(count_term(doc['title']))
	    	  
	         
	finally:
	    client.close()
	word_score_list={}   # word:score in all list
	for i,count in enumerate(count_list):
		for word in count:
			if word in word_score_list:
				word_score_list[word]+=tfidf(word,count,count_list)
			else:
				word_score_list[word]=tfidf(word,count,count_list)
	sorted_words = sorted(word_score_list.items(), key = lambda x: x[1], reverse=True)
	for word, score in sorted_words[:50]:
		print(word,' ',score)



def word_freq():
	query = {}
	sort = [ (u"price", 1) ]

	text=''
	cursor = collection.find(query, sort = sort)
	try:
	    for doc in cursor:
	    	text=text+doc['title']
	         
	finally:
	    client.close()

	stop_words = set(stopwords.words('english'))
	stop_words.extend([',','-','.','(',')',';','/','&','amp','A'])
	
	word_tokens=nltk.word_tokenize(text)
	filtered_words = [w for w in word_tokens if not w in stop_words]
	filtered_words=[w for w in filtered_words if not w in stop_words1]
	stemmer = PorterStemmer()
	seg_list = [stemmer.stem(word) for word in filtered_words]
	#print(' '.join(seg_list))

	#seg_list=jieba.cut(text,cut_all=True) Chinese Word
	a=head_seg(seg_list,100)
	print(a)
	return a

def show_img(wc):
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")

def word_cloud():
	a=word_freq()
	b=[('a',2)]
	wordcloud = WordCloud(background_color="white",width=1000, height=860, margin=2).generate_from_frequencies(a)
	wordcloud.generate_from_frequencies(a)
	plt.imshow(wordcloud)
	plt.show()

word_cloud()

#word_tfidf_freq()



