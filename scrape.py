from bs4 import BeautifulSoup
import winsound
import requests
import json
import json5
import re

id = 0
json_data = {}

def req(url):
    headers = {
    'User-Agent': 'a',
    }

    response = requests.get(url, headers=headers , verify=False)
    return response.content


def soup(html_doc , select=None , find_all=None):
    res = BeautifulSoup(html_doc, 'html.parser')
    if select : 
        res = res.select(f'{select}')
    elif find_all:
        res = res.find_all(f'{find_all}')
    return res

def html2text(cont): 
    cont =BeautifulSoup(str(cont) ,'html.parser')
    cont = cont.to_text()
    return cont

def  req_json(cont):
    return json.loads(cont)

#hackerrank
dic={}
varl= ["algorithms","data-structures","mathematics","ai","c","cpp","java","python","ruby","sql","databases","shell","fp","regex"]
offset = 0 # the starting point
limit = 50 # 10-50
breaker=False
api_get = "https://www.hackerrank.com/rest/contests/master/tracks/{}/challenges?offset={}&limit={}&track_login=true"
for var in varl : 
    print(var)
    json_content = json.loads(req(api_get.format(var,offset,limit)))

    total = json_content['total']
    print(total)
    for i in range(total+1 ):      
        for i in range(limit):
            json_content = json.loads(req(api_get.format(var,offset,limit)))
            if offset >= total:
                breaker = True
                break
            else:    
                print(api_get.format(var,offset,limit))
                try :
                    for i in range(limit):
                        print(i , json_content["models"][i]['slug']) 
                        print(json_content["models"][i]['difficulty_name'])
                        print(json_content["models"][i]['tag_names'])
                        json_content2= json.loads(req('https://www.hackerrank.com/rest/contests/master/challenges/{}'.format(json_content["models"][i]['slug'])))
                        print('https://www.hackerrank.com/rest/contests/master/challenges/{}'.format(json_content["models"][i]['slug']))



                        dic = {'title' : json_content["models"][i]['slug'], 
                        'body': json_content2["model"]["body_html"] ,
                        'diff':json_content["models"][i]['difficulty_name'] ,
                        'tags': json_content["models"][i]['tag_names'],
                        'var': var,
                        'site': 'hackerrank' ,
                        'link': 'https://www.hackerrank.com/rest/contests/master/challenges/{}'.format(json_content["models"][i]['slug'])}
                        json_data[id]=dic
                        id += 1

                except IndexError:
                    breaker= True
                    break
            offset+=limit  
        if breaker: # the interesting part!
            offset = 0
            break


#codeshef
page_num = range(193)
limit=1000
api_get = 'https://www.codechef.com/api/list/problems?page={}&limit={}&sort_by=difficulty_rating&sort_order=asc&search=&category=rated&start_rating=0&end_rating=5000&topic=&tags=&group=all&'
link='https://www.codechef.com/api/contests/PRACTICE/problems/{}'
try:
    for i in page_num:
        cont = req_json(req(api_get.format(i, limit)))
        for x in range(limit):

            code= cont['data'][x]['code']            

            breakpoint()
            cont = req_json(req(link.format(code)))            
            dic = {'title' : cont['problem_name'], 
            'body': cont['problemComponents'] ,
            'diff':cont['difficulty_rating'] ,
            'tags': cont['user_tags'],
            'site': 'codechef' ,
            'link': 'https://www.codechef.com/submit/{}'.format(code)}
            json_data[id]=dic
            id += 1

            
            # input("press anything")
except IndexError:
    print('all codes found ')    
    
#hackerearth

off_num = range(16)
api_get = 'https://www.hackerearth.com/practice/api/problems/?limit=100&offset={}'
link = 'https://www.hackerearth.com/practice/algorithms/dynamic-programming/introduction-to-dynamic-programming-1/practice-problems/{}'
try:
    for i in off_num:    
        cont= req_json(req(api_get.format(i)))
        print(api_get.format(i))
        for i in range(100):
            title = cont['problems']['algorithm'][i]['title']
            url = cont['problems']['algorithm'][i]['url'][9:]
            script_tag =soup(req(link.format(url)) , select='script:nth-child(35)')[0]
            js_obj = f'{str(script_tag)[55:-435]}' 
            py_obj = json5.loads(js_obj)            

            sampleio=req_json(req('https://www.hackerearth.com/practice/api/problems/{}'.format(url)))
            body ={'problem' : py_obj['problemData']['description'] ,'samplein' : sampleio['sample_input'] ,'sampleout': sampleio['sample_output'],"explination" : py_obj['problemData']['sample_explanation'] }  
            dic = {'title' : title, 
            'body': body ,
            'diff':cont['problems']['algorithm'][i]['difficulty'] ,
            'tags': '\"'+py_obj['problemData']['tags'].replace(',','\",\"')+'\"',
            'site': 'hackerearth' ,
            'link': py_obj['shareURL']}
            # print(json.dumps(dic , indent=4))
            # input('press anything')
            json_data[id]=dic
            id += 1            
except IndexError:
    print('all codes found ')    

#leetcode

limit = 100
tags=[]
def leetcode(json_data):
    json_data = json_data

    response = requests.post('https://leetcode.com/graphql/', json=json_data)
    return response.content
try:
    for i in range(0,2500,limit):
        json_data = {
            'query': '\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ',
            'variables': {
                'categorySlug': '',
                'skip': i,
                'limit': limit,
                'filters': {},
            },
        }        
        cont_json=req_json(leetcode(json_data))
        for x in range(100):
            titleSlug = cont_json['data']['problemsetQuestionList']['questions'][x]['titleSlug']
            print('https://leetcode.com/problems/'+titleSlug)
            json_data = {
                'operationName': 'questionData',
                'variables': {
                    'titleSlug': titleSlug,
                },
                'query': 'query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    exampleTestcases\n    categoryTitle\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      hasVideoSolution\n      paidOnlyVideo\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    challengeQuestion {\n      id\n      date\n      incompleteChallengeCount\n      streakCount\n      type\n      __typename\n    }\n    __typename\n  }\n}\n',
            }
            try:
                for i in range(100):
                    tags.append(cont_json['data']['problemsetQuestionList']['questions'][x]['topicTags'][i]['name'])
            except:
                pass
            dic = {'title' : cont_json['data']['problemsetQuestionList']['questions'][x]['title'], 
            'body': req_json(leetcode(json_data))['data']['question']['content'] ,
            'diff':cont_json['data']['problemsetQuestionList']['questions'][x]['difficulty'] ,
            'tags':tags,
            'site': 'leetcode' ,
            'link': 'https://leetcode.com/problems/{}'.format(titleSlug)    
            }
            json_data[id]=dic
            id += 1
            # input("press anything ")
except IndexError:
    print('all codes found ')
    
#topcoder
num = range(0,5500,50)
page_link = 'https://www.topcoder.com/tc?module=ProblemArchive&sr={}&er={}&sc=&sd=&class=&cat=&div1l=&div2l=&mind1s=&mind2s=&maxd1s=&maxd2s=&wr='
for i in num:
    link =page_link.format(i,i+50) 
    print(page_link.format(i,i+50))


    tags=soup(req(link), select='table.paddingTable2 >tr')[4:]


    for i in tags :
        title = soup(f'''{i}''' , select='td:nth-child(2) > a ')[0].text.replace(" ", '').replace('\n','')  # title
        link = 'https://community.topcoder.com'+soup(f'''{i}''' , select='td:nth-child(2) > a ')[0]['href']
        body = soup(req(link), select='.problemText')[0].text.replace(" ", '').replace('\n','') # body
        diff =soup(f'''{i}''' , select='td:nth-child(8) ')[0].text.replace(" ", '').replace('\n','') , soup(f'''{i}''' , select='td:nth-child(10) ')[0].text.replace(" ", '').replace('\n','') #difficulity
        category = str( soup(f'''{i}''' , select='td:nth-child(6) ')[0].text).replace(" ", '').replace('\n','').split(',')
        
        dic = {'title' : title, 
        'body': body ,
        'diff':diff ,
        'tags': category,
        'site': 'topcoder' ,
        'link': link}
        json_data[id]=dic
        id += 1        
        print (dic)
        
        # input('press any thing')
        
#spoj
num = range(0, 3900, 50)
page_link = 'https://www.spoj.com/problems/classical/sort=0,start={}'

for i in num:
    tags = soup(req(page_link.format(i)) , select='.problems > tbody:nth-child(3) > tr') 
    for tag in tags:
        link = 'https://www.spoj.com' + soup(f'''{tag}''' , select='a')[0]['href']
        cont = req(link)      
        dic = {'title' : soup(f'''{tag}''' , select='a')[0].text , 
        'body': soup(cont , select='#problem-body') ,
        'diff': soup(f'''{tag}''' , select='div')[0]['title'] ,
        'tags': soup(cont , select='#problem-tags')[0].text.split('\n'),
        'site': 'spoj' ,
        'link': link }
        json_data[id]=dic
        id += 1     
#project elur
num = range(1,17)
page_link = 'https://projecteuler.net/archives;page={}'
diff2 =[]
dic = {}
id1 = 0
dest = {}
for i in num:
    tags = soup(req(page_link.format(i)) , select='#problems_table > tr')    
    del tags[0]
    for i in tags: 
        link = "https://projecteuler.net/"+soup(f'''{i}''',select=("td:nth-child(2)>a"))[0]['href']
        cont = req(link)
        tag = soup(cont , select='.tooltiptext_right')[0]
        dic = { 'title' : soup(f'''{cont}''',select=("#content > h2"))[0].text , 
        'body': soup(cont , select='.problem_content') ,
        'diff': [re.findall('Difficulty rating: \d{1,1000}.' , str(tag)) , re.findall('Solved by \d{1,1000}' , str(tag))],
        'tags': None,
        'site': 'projecteuler',
        'link': link} 
        json_data[id]=dic
        id += 1
with open('data.json', 'a+') as outfile:
    outfile.write(json.dumps(json_data, indent=4))
    
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
        
             