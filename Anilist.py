import requests
import json

class Anilist():

    URL = "https://graphql.anilist.co"

    userName = None
    UserId = None

    def __init__(self, name):
        self.userName = name
        self.userId = self.getUserId(self.userName)

    #returns the requests object
    def sendReq(self,query,variables):
        req = requests.post(self.URL, json={'query': query, 'variables': variables})
        return req

    #takes the user name and returns user id
    #the user's account has to be public
    def getUserId(self, userName):
        query = '''
            query($userName:String){
                User(search:$userName){
                    id
                }
            }
        '''
        variables = {
            "userName" : self.userName
        }

        x = self.sendReq(query,variables).json()
        return x['data']['User']['id']
    

    def print(self):
        l = self.getWatchingList()
        for i in l:
            print(i)
    
    #sort the list in descending order based on remaining airtime
    def sortList(self,l):
        n = len(l)
        for i in range(n):
            for j in range(0, n-i-1):
                if l[j]['timeRem'] < l[j+1]['timeRem']:
                    l[j], l[j+1] = l[j+1], l[j]
        return l
    

    # returns user's currently watching anime details 
    # which are airing as a list of dictinaries
    def getWatchingList(self):
        query = '''
            query($userId:Int){
                Page(page:0,perPage:50){
                    mediaList(userId: $userId, status: CURRENT){
                        media{
                            coverImage{
                              large
                            }
                          	siteUrl
                            title{
                                english
                            }
                            nextAiringEpisode{
                                timeUntilAiring
                                episode
                            }
                        }
                    }
                }
            }
        '''
        variables = {
            "userId": self.userId
        }
        x = self.sendReq(query, variables).json()
        #stores required data in a list
        l = []
        for item in x["data"]["Page"]["mediaList"]:
            details = {}
            if item["media"]["nextAiringEpisode"] is not None:
                details["title"] = item["media"]["title"]["english"]
                details["epiNo"] = item["media"]["nextAiringEpisode"]["episode"]
                details["timeRem"] = item["media"]["nextAiringEpisode"]["timeUntilAiring"]
                details['img'] = item['media']['coverImage']['large']
                details['url'] = item["media"]['siteUrl']
                l.append(details)
                
        return self.sortList(l)



