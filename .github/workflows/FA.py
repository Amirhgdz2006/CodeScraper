import requests 
from time import sleep 
from random import uniform 

class Divar_old_detector:

    def __init__(self):
        self.token_url = "https://api.divar.ir/v8/posts-v2/web/"

        self.tokens_set = set()

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

        self.primary_request()
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

    def tokens_set_update(self,response):
        for widget in response["list_widgets"]:
            if widget["widget_type"] == "POST_ROW":
                try : 
                    self.tokens_set.add(widget["data"]["token"]) 

                except Exception as e:
                    print(f"addition of token failed due to {e} !")


    def primary_request(self):
        response = requests.post(url = self.url , headers = self.headers , json = self.primary_payload)
        try : 
            response = response.json()
            self.payload_update(response)
            self.tokens_set_update(response)
        except : 
            print(response.status_code)

    def secondary_requests(self):
        cnt = 0 
        while self.secondary_payload["has_next_page"]:
            
            cnt += 1 
            if cnt % 100 == 0 :
                sleep(uniform(0.3,0.5))
            
            response = requests.post(url = self.url , headers = self.headers , json = self.secondary_payload)
            
            try :
                response = response.json()
                self.payload_update(response)
                self.tokens_set_update(response)
            
            except :
                print(response.status_code)
    
    def log(self):
        print(f"number of collected ids : {len(self.tokens_set)}")
        print(f"sample id being collected : {max(self.tokens_set)}")

        

divar_old_detector = Divar_old_detector()