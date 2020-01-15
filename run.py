import requests, threading, queue, time, os
from requests.exceptions import ConnectionError
from datetime import datetime

class Bruter():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    inputQueue = queue.Queue()

    def __init__(self):
        print(r"""
        Admin Page Login Bruter
        { Mazterin-Dev } > Security Gh0st <
        """)
        self.wordlist   = input("WordList   : ")
        self.site       = input("Site       : ")
        self.threads     = input("Threads ( Make ur CPU's Slowly ) : ")
        self.totalList  = len(list(open(self.wordlist, encoding='utf-8')))
    
    def get_info(self, web):
        try:
            req = requests.get(web,
                    headers={
                        'User-Agent': self.ua
                    },
                    verify=False
                )
            if req.status_code == 200:
                if "404" or "not found" in req.text:
                    return 'notfound'
                else:
                    return 'ok'
            elif req.status_code == 302 or req.status_code == 301:
                return 'move'
            else:
                return 'notfound'
        except ConnectionError:
            return 'error'
        except:
            return 'error'
    
    def check(self):
        global t
        while 1:
            web = self.inputQueue.get()
            result = self.get_info(web)
            timez = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if result == 'ok':
                print("[+] {} 200 OK {}".format(timez, web))
                os._exit(1)
            elif result == 'move':
                print("[+] {} 302/301 Moved {}".format(timez, web))
            elif result == 'notfound':
                print("[+] {} 404 Not Found {}".format(timez, web))
            else:
                print("ERROR! Connection TimeOut to the website. website down ?")
                os._exit(1)
            self.inputQueue.task_done()
    
    def run_thread(self):
        global t
        for i in range(int(self.threads)):
            t = threading.Thread(target=self.check)
            t.setDaemon(True)
            t.start()
        for x in open(self.wordlist, 'r', encoding='utf-8').readlines():
            self.inputQueue.put(str(self.site) + x.strip())
        self.inputQueue.join()

    def finish(self):
        print('')
        print('Checking', self.totalList, 'Wordlists has been completed perfectly')
        print('')
    
uo = Bruter()
uo.run_thread()
uo.finish()
