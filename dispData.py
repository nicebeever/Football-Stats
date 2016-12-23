#!/usr/bin/python3

import string, logging

def printRes(results,word1,word2):

    print('{} {}'.format(word1, word2))
    print('Possion       Shots  Shots on Target     Corners   Fouls     Goals  Conceded')
    print(' {}        {}        {}           {}     {}      {}    {}'.format(round(results[0],2) \
            ,round(results[1],2) ,round(results[2],2) ,round(results[3],2)  ,\
              round(results[4],2)  ,round(results[5],2),round(results[6],2))) 
    
def calcRange(max,min):
    
    answer = []
    answer.append(max[0] - min[0])
    answer.append(max[1] - min[1])
    answer.append(max[2] - min[2])
    answer.append(max[3] - min[3])
    answer.append(max[4] - min[4])
    answer.append(max[5] - min[5])
    
    return answer