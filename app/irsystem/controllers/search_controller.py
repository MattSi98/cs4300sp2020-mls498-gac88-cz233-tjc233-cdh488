from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


###### my imports
import json
import numpy as np
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize





import pandas as pd
from pytrends.request import TrendReq
pytrend = TrendReq()

# Get Google Hot Trends data
df = pytrend.trending_searches(pn='united_states')
trending = []
for x in df.values:
    trending.append(x[0])

project_name = "Custom Jeopardy Quiz Generation"
net_id = "Matthew Simon: mls498, Grayson Campbell: gac88, Daniel Hayon: dh488, Theo Carrel: tjc233, Carol Zhang: cz233"

@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    if not query:
        data = []
        output_message = ''
    else:
        output_message = "Here are questions about " + query + "!"
        data = generateQuiz(query)
        if len(data) < 20:
            data = ['    ', '    ']
            output_message = 'Invalid query, please enter another.'
    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, trending=trending)




##############################################################################################
############   CODE I ADDED FOR P03 ######################################



'''
splits query into individual query words
'''


def splitQuery(query):
    qList = query.split(',')
    final = []
    for x in qList:
        final.append(x.strip())
    return final


# splitQuery("dog,   sports,   bridges,  mom,dad")


'''
Takes query input of a query and returns a list of all of the questions
within those categories as long as they were valid categories.
Invalid categories are ignored.

Input: comma separated string
Output: list of tuples (question, answer)

example:
    Input: "dog,bridges,sports"
    Output: [("question","answer"),(),(),(),...,()]
'''


def getValidQuestions(query):
    validQuestions = []
    queryWords = splitQuery(query)
    with open('./data/finalData.json') as file:
        data = json.load(file)
        for word in queryWords:
            for x in data:
                if (word.upper() in x[2] or word.upper() in x[3].upper() or word.upper() in x[4].upper()):
                    validQuestions.append((x[3],x[4],x[2]))
    validQuestionsNoDups = list(dict.fromkeys(validQuestions))
    return validQuestionsNoDups


'''
Takes twenty random entries from the given list of valid questions
'''


def getTwentyRandQuestions(validQuestions):
    if (validQuestions == []):
        return ["invlaid input - try again."]
    else:
        finalQuestions = []
        for i in range(20):
            randNum = random.randrange(0, len(validQuestions))
            finalQuestions.append(validQuestions[randNum])
        return finalQuestions




def cosineSim(sentence1, sentence2):
    tmp1 = []
    tmp2 = []

    sent1_set = set(sentence1)
    sent2_set = set(sentence2)
    union = sent1_set.union(sent2_set)

    for word in union:
        if word in sentence1:
            tmp1.append(1)
        else:
            tmp1.append(0)
        if word in sentence2:
            tmp2.append(1)
        else:
            tmp2.append(0)

    c = 0

    # cosine formula
    for i in range(len(union)):
            c+= tmp1[i]*tmp2[i]
    cosine = c / float((sum(tmp1)*sum(tmp2))**0.5)
    return cosine




'''
Takes a random question and then uses cosine similarity to select the 20 most similar questions to it

motivation from: https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
'''
def getMostSimilar(validQuestions):
    if len(validQuestions) < 19:
        return ["invlaid input - try again."]
    else:
        randNum = random.randrange(0, len(validQuestions))
        init_qs = []
        stoplisted = []
        for x in validQuestions:
            init_qs.append(word_tokenize(x[0]))

        randomized_start_word = init_qs[randNum]
        ordered_list = []
        for idx, val in enumerate(init_qs):
            if val != randomized_start_word:
                tmp = cosineSim(randomized_start_word, val)
                ordered_list.append((tmp,idx))
    ordered_list.sort()
    ordered_list.reverse()
    final = []
    for x in ordered_list[:20]:
        final.append((validQuestions[x[1]], x[0]))
    return final













'''
generates a full quiz of 20 questions from a given input query
'''


def generateQuiz(query):
    valid = getValidQuestions(query)
    #return getTwentyRandQuestions(valid)
    return getMostSimilar(valid)
