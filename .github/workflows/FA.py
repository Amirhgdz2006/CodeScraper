import requests 
from time import sleep 
from random import uniform 

class Divar_new_detector:

    def __init__(self,min_sleep,max_sleep,sleep_threshold,num_iteration = 1,tokens_set = set()):
        
        self.min_sleep = min_sleep 

        self.max_sleep = max_sleep 

        self.sleep_threshold = sleep_threshold
        
        self.tokens_set = tokens_set

        self.token_url = "https://api.divar.ir/v8/posts-v2/web/"

        self.url = "https://api.divar.ir/v8/postlist/w/search"

        self.headers = { 
            "accept" : "application/json , text/plain , */*" , 
            "accept-encoding" : "gzip , deflate , br , zstd" , 
            "accept-language" : "en-US , en;q=0.9 , fa;q=0.8 , de;q=0.7" ,
            "content_type" : "application/json" ,
            "origin" : "https://divar.ir" ,  
            "referer" : "https://divar.ir/" ,
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36" ,
            "x-render-type" : "CSR" , 
            "x-screen-size" : "526x812" , 
            "x-standard-divar-error" : "true"    
            }
        self.primary_payload = {
            "city_ids" : ["1"]  , 
            "source_view" : "CATEGORY" , 
            "disable_recommendation" : False , 
            "map_state" : {
                "camera_info" : {
                    "bbox" : {}    
                }
            } , 
            "search_data" : {
                "form_data" : {
                    "data" : {
                        "category" : {
                            "str" : {
                                "value" : "real-estate"
                            }
                        }
                    }
                } , 
                "server_payload" : {
                    "@type" : "type.googleapis.com/widgets.SearchData.ServerPayload" , 
                    "additional_form_data" : {
                        "data" : {
                            "sort" : {
                                "str" : {
                                    "value" : "sort_date"
                                }
                            }
                        }
                    }
                }
            }  
        }
        if self.__class__.__name__ == "Divar_new_detector":
            self.primary_requests(num_iteration)
            print(f"new detector is executed for {num_iteration} times .")
    
    def tokens_set_update(self,response):
        for widget in response["list_widgets"]:
            if widget["widget_type"] == "POST_ROW":
                try :
                    token = widget["data"]["token"]
                    if  token not in self.tokens_set:

                        # demo 
                        # print(f"new token is found : {token}")
                        # scraping , data cleanup and insertion into database will be added 
                        
                        self.tokens_set.add(token)
                
                except Exception as e:
                    print(f"examination of tokens failed due to {e} !")

    def payload_update(self,response):
        pass 

    def primary_requests(self,num_iteration = 1):
        cnt = 0 
        while cnt < num_iteration :
            cnt += 1
            if cnt % self.sleep_threshold == 0 :
                sleep(uniform(self.min_sleep,self.max_sleep))
            
            response = requests.post(url = self.url , headers = self.headers , json = self.primary_payload)
            try : 
                response = response.json()
                self.payload_update(response)
                self.tokens_set_update(response)
                
            except :
                print(f"request failed due to {response.status_code}")

              
class Divar_old_detector(Divar_new_detector):

    def __init__(self,min_sleep,max_sleep,sleep_threshold):
        super().__init__(min_sleep,max_sleep,sleep_threshold)
 
        self.secondary_payload = {
            "city_ids" : ["1"]  , 
            "source_view" : "CATEGORY" , 
            "disable_recommendation" : False , 
            "map_state" : {
                "camera_info" : {
                    "bbox" : {}    
                }
            } , 
            "search_data" : {
                "form_data" : {
                    "data" : {
                        "category" : {
                            "str" : {
                                "value" : "real-estate"
                            }
                        }
                    }
                } , 
                "server_payload" : {
                    "@type" : "type.googleapis.com/widgets.SearchData.ServerPayload" , 
                    "additional_form_data" : {
                        "data" : {
                            "sort" : {
                                "str" : {
                                    "value" : "sort_date"
                                }
                            }
                        }
                    }
                }
            } ,
            "tokens" : None , 
            "has_next_page" : True , 
            "pelle" : {
                "elastic" : {
                    "tokens" : None , 
                    "documents" : None 
                }
            } , 
            "last_post_date_epoch" : None , 
            "search_id" : None , 
            "search_uid" : None , 
            "posts_metadata" : None 
            }

        self.primary_requests()
        self.secondary_requests()
        self.log()


    def payload_update(self,response):
        try :
            data  = response["action_log"]["server_side_info"]["info"]
            self.secondary_payload["tokens"] = data["tokens"]
            self.secondary_payload["has_next_page"] = data["has_next_page"] 
            self.secondary_payload["pelle"]["elastic"]["tokens"] = data["pelle"]["elastic"]["tokens"]
            self.secondary_payload["pelle"]["elastic"]["documents"] = data["pelle"]["elastic"]["documents"]
            self.secondary_payload["last_post_date_epoch"] = data["last_post_date_epoch"]
            self.secondary_payload["search_id"] = data["search_id"]
            self.secondary_payload["search_uid"] = data["search_uid"]
            self.secondary_payload["posts_metadata"] = data["posts_metadata"]
            
        except Exception as e: 
            print(f"payload update failed due to {e} !")

    def secondary_requests(self):
        cnt = 0 
        while self.secondary_payload["has_next_page"]:
    
            cnt += 1 
            if cnt % self.sleep_threshold == 0 :
                sleep(uniform(self.min_sleep,self.max_sleep))
            
            response = requests.post(url = self.url , headers = self.headers , json = self.secondary_payload)
            
            try :
                response = response.json()
                self.payload_update(response)
                self.tokens_set_update(response)
            
            except :
                print(f"request failed due to {response.status_code}")
    
    def log(self):
        print(f"number of collected ids : {len(self.tokens_set)}")
        print(f"sample id being collected : {max(self.tokens_set)}")

divar_old_detector = Divar_old_detector(0.3,0.5,100)
divar_new_detector = Divar_new_detector(0.3,0.5,100,50,divar_old_detector.tokens_set)