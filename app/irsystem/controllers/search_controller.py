from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


###### my imports
import json
import numpy as np
import random

project_name = "Spotify Buddy Playlist Generation"
net_id = "Matthew Simon: mls498, Grayson Campbell: gac88, Daniel Hayon: dh488, Theo Carrel: tjc233, Carol Zhang: cz233"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		#data = range(5)
		data = generateQuiz(query)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)




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
    with open('./data/questionsList.json') as file:
        data = json.load(file)
        for word in queryWords:
            for x in data:
                if (word.upper() in x[0]):
                    validQuestions.append((x[1], x[2]))
    return validQuestions


'''
Takes twenty random entries from the given list of valid questions
'''


def getTwentyRandQuestions(validQuestions):
    finalQuestions = []
    for i in range(20):
        randNum = random.randrange(0, len(validQuestions))
        finalQuestions.append(validQuestions[randNum])
    print(finalQuestions)
    return finalQuestions


'''
generates a full quiz of 20 questions from a given input query
'''


def generateQuiz(query):
    valid = getValidQuestions(query)
    return getTwentyRandQuestions(valid)
