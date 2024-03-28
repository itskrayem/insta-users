# import asyncio
# from typing import List
# from os import system
# from scapy.all import *
# import random
# import socket
# import struct

# def random_ip():
#     # Generate a random IPv4 address
#     return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# def write_file(arg: str) -> None:
#     with open('hits.txt', 'a', encoding='UTF-8') as f:
#         f.write(f'{arg}\n')

# def open_file() -> List[str]:
#     with open('usernames.txt', 'r', encoding='UTF-8') as f:
#         file_contents = [line.strip('\n') for line in f]
#     return file_contents

# class Checker:
#     HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
#     SEMAPHORE_LIMIT = 100  # Limit concurrency to 100 tasks
#     IP_CHANGE_INTERVAL = 1000  # Change IP every 1000 usernames

#     def __init__(self, usernames: List[str]):
#         self.to_check = usernames
#         self.request_count = 0
#         self.source_ip = random_ip()  # Initialize with a random IP address
#         self.semaphore = asyncio.Semaphore(self.SEMAPHORE_LIMIT)

#     async def _check(self, username: str) -> None:
#         try:
#             async with self.semaphore:
#                 self.request_count += 1
#                 if self.request_count % self.IP_CHANGE_INTERVAL == 0:
#                     self.source_ip = random_ip()  # Change IP every 1000 requests
#                 packet = IP(src=self.source_ip, dst='www.instagram.com') / TCP(dport=443)  # Craft TCP packet
#                 await asyncio.sleep(0)  # Sleep briefly to allow other tasks to run
#                 send(packet, verbose=False)  # Send packet asynchronously

#                 # Sniff response packets asynchronously
#                 response = sniff(filter=f"icmp and host {self.source_ip}", timeout=2, count=1)

#                 if response and response[0].type == 3:  # Check if ICMP destination unreachable response is received
#                     print('%s[AVAILABLE] https://www.instagram.com/%s%s' % ('\u001b[32;1m', username, '\u001b[0m'))
#                     write_file(username)
#                 else:
#                     print('%s[UNAVAILABLE] https://www.instagram.com/%s%s' % ('\u001b[31;1m', username, '\u001b[0m'))
#         except Exception as e:
#             print('[ERROR] ' + str(e))  # Convert the exception object to a string

#     async def start(self):
#         tasks = []
#         for i in self.to_check:
#             tasks.append(asyncio.create_task(self._check(i)))
#         system('clear')  # Clear the console screen
#         print('Loading.. This may take a while.')
#         await asyncio.gather(*tasks)

# if __name__ == '__main__':
#     system('title Instagram Username Checker by NightfallGT')
#     system('clear')  # Clear the console screen
#     username_list = open_file()
#     checker = Checker(username_list)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(checker.start())








# import asyncio
# import aiohttp
# from typing import List
# from os import system

# def open_file() -> List[str]:
#     with open('usernames.txt', 'r', encoding='UTF-8') as f:
#         file_contents = [line.strip('\n') for line in f]

#     return file_contents

# def write_file(arg: str) -> None:
#     with open('hits.txt', 'a', encoding='UTF-8') as f:
#         f.write(f'{arg}\n')

# class Checker:
#     HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
#     SEMAPHORE_LIMIT = 1000  # Adjust the concurrency level here
    
#     def __init__(self, usernames: List[str]):
#         self.to_check = usernames
#         self.checked_count = 0

#     async def _check(self, session: aiohttp.ClientSession, username: str) -> None:
#         try:
#             async with session.get('https://www.instagram.com/%s' % username) as response:
#                 r = await response.text()

#                 self.checked_count += 1
                
#                 if response.status == 404:
#                     print('%d. %s[AVAILABLE] https://www.instagram.com/%s%s' % (self.checked_count, '\u001b[32;1m', username, '\u001b[0m'))
#                     write_file(username)

#                 elif response.status == 200 and 'Login • Instagram' in r:
#                     print('%d. [!] Failed to check username. Try again later' % self.checked_count, username)

#                 else:
#                     print('%d. %s[UNAVAILABLE] https://www.instagram.com/%s%s' % (self.checked_count, '\u001b[31;1m', username, '\u001b[0m'))

#         except Exception as e:
#             print('%d. [ERROR] ' % self.checked_count + str(e))  # Convert the exception object to a string
           
#     async def start(self):
#         tasks = []
#         async with aiohttp.ClientSession(headers=self.HEADERS) as session:
#             for username in self.to_check:
#                 tasks.append(asyncio.create_task(self._check(session, username)))
#             system('clear')  # Clear the console screen
#             print('Loading.. This may take a while.')
#             await asyncio.gather(*tasks)
#             await session.close()  # Close the session to release resources

# if __name__ == '__main__':
#     system('title Instagram Username Checker by NightfallGT')
#     system('clear')  # Clear the console screen
#     username_list = open_file() 
#     checker = Checker(username_list)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(checker.start())








import asyncio
import aiohttp
from typing import List, Dict
from os import system

def open_file() -> Dict[str, List[str]]:
    grouped_usernames = {}
    with open('usernames.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            username = line.strip('\n')
            first_char = username[0]
            if first_char not in grouped_usernames:
                grouped_usernames[first_char] = []
            grouped_usernames[first_char].append(username)

    return grouped_usernames

def write_file(arg: str) -> None:
    with open('hits.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')

class Checker:
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
    SEMAPHORE_LIMIT = 1000  # Adjust the concurrency level here
    
    def __init__(self, username_groups: Dict[str, List[str]]):
        self.username_groups = username_groups
        self.checked_count = 0

    async def _check(self, session: aiohttp.ClientSession, username: str) -> None:
        try:
            async with session.get('https://www.instagram.com/%s' % username) as response:
                r = await response.text()

                self.checked_count += 1
                
                if response.status == 404:
                    print('%d. %s[AVAILABLE] https://www.instagram.com/%s%s' % (self.checked_count, '\u001b[32;1m', username, '\u001b[0m'))
                    write_file(username)

                elif response.status == 200 and 'Login • Instagram' in r:
                    print('%d. [!] Failed to check username. Try again later' % self.checked_count, username)

                else:
                    print('%d. %s[UNAVAILABLE] https://www.instagram.com/%s%s' % (self.checked_count, '\u001b[31;1m', username, '\u001b[0m'))

        except Exception as e:
            print('%d. [ERROR] ' % self.checked_count + str(e))  # Convert the exception object to a string
           
    async def start(self):
        async with aiohttp.ClientSession(headers=self.HEADERS) as session:
            for group_key, group_value in self.username_groups.items():
                system('clear')  # Clear the console screen
                print(f'Loading group starting with {group_key}.. This may take a while.')
                for start_index in range(0, len(group_value), self.SEMAPHORE_LIMIT):
                    tasks = []
                    for username in group_value[start_index:start_index+self.SEMAPHORE_LIMIT]:
                        tasks.append(asyncio.create_task(self._check(session, username)))
                    await asyncio.gather(*tasks)
            print("All groups processed.")

if __name__ == '__main__':
    system('title Instagram Username Checker by NightfallGT')
    system('clear')  # Clear the console screen
    username_groups = open_file() 
    checker = Checker(username_groups)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checker.start())








##with multithreading and queueing

# import aiohttp
# import asyncio
# import threading
# from queue import Queue
# from typing import List, Dict
# from os import system

# QUEUE_STATE_FILE = "queue_state.txt"

# def open_file() -> Dict[str, List[str]]:
#     grouped_usernames = {}
#     with open('usernames.txt', 'r', encoding='UTF-8') as f:
#         for line in f:
#             username = line.strip('\n')
#             first_char = username[0]
#             if first_char not in grouped_usernames:
#                 grouped_usernames[first_char] = []
#             grouped_usernames[first_char].append(username)

#     return grouped_usernames

# def write_file(arg: str) -> None:
#     with open('hits.txt', 'a', encoding='UTF-8') as f:
#         f.write(f'{arg}\n')

# class Checker:
#     HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
#     SEMAPHORE_LIMIT = 1000  # Adjust the concurrency level here

#     def __init__(self, username_groups: Dict[str, List[str]]):
#         self.username_groups = username_groups
#         self.queue = Queue()
#         self.load_queue_state()

#     def load_queue_state(self):
#         try:
#             with open(QUEUE_STATE_FILE, "r") as f:
#                 for line in f:
#                     self.queue.put(line.strip())
#         except FileNotFoundError:
#             pass

#     def save_queue_state(self):
#         with open(QUEUE_STATE_FILE, "w") as f:
#             while not self.queue.empty():
#                 item = self.queue.get()
#                 f.write(item + "\n")

#     async def _check(self, session: aiohttp.ClientSession) -> None:
#         while True:
#             username = self.queue.get()
#             if username is None:
#                 break
#             try:
#                 async with session.get('https://www.instagram.com/%s' % username) as response:
#                     r = await response.text()

#                     if response.status == 404:
#                         print(f'[AVAILABLE] https://www.instagram.com/{username}')
#                         write_file(username)

#                     elif response.status == 200 and 'Login • Instagram' in r:
#                         print(f'[ERROR] Failed to check username {username}. Try again later')

#                     else:
#                         print(f'[UNAVAILABLE] https://www.instagram.com/{username}')

#             except Exception as e:
#                 print(f'[ERROR] {str(e)}')

#             self.queue.task_done()

#     async def start(self):
#       async with aiohttp.ClientSession(headers=self.HEADERS) as session:
#           tasks = [self._check(session) for _ in range(threading.active_count())]
  
#           for group_key, group_value in self.username_groups.items():
#               print(f'Loading group starting with {group_key}.. This may take a while.')
#               for username in group_value:
#                   self.queue.put(username)
#                   if self.queue.qsize() >= self.SEMAPHORE_LIMIT:
#                       self.save_queue_state()
#                       await asyncio.sleep(1)  # Sleep to give time for the state to be saved
  
#           for _ in range(threading.active_count()):
#               self.queue.put(None)
  
#           await asyncio.gather(*tasks)


# if __name__ == '__main__':
#     system('title Instagram Username Checker by NightfallGT')
#     system('clear')  # Clear the console screen
#     username_groups = open_file() 
#     checker = Checker(username_groups)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(checker.start())






# import aiohttp
# import asyncio
# import threading
# from typing import List, Dict
# from os import system

# def open_file() -> Dict[str, List[str]]:
#     grouped_usernames = {}
#     with open('usernames.txt', 'r', encoding='UTF-8') as f:
#         for line in f:
#             username = line.strip('\n')
#             first_char = username[0]
#             if first_char not in grouped_usernames:
#                 grouped_usernames[first_char] = []
#             grouped_usernames[first_char].append(username)

#     return grouped_usernames

# def write_file(arg: str) -> None:
#     with open('hits.txt', 'a', encoding='UTF-8') as f:
#         f.write(f'{arg}\n')

# class Checker:
#     HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
#     SEMAPHORE_LIMIT = 1000  # Adjust the concurrency level here

#     def __init__(self, username_groups: Dict[str, List[str]]):
#         self.username_groups = username_groups

#     async def _check(self, session: aiohttp.ClientSession, username: str) -> None:
#         try:
#             async with session.get('https://www.instagram.com/%s' % username) as response:
#                 r = await response.text()

#                 if response.status == 404:
#                     print(f'[AVAILABLE] https://www.instagram.com/{username}')
#                     write_file(username)

#                 elif response.status == 200 and 'Login • Instagram' in r:
#                     print(f'[ERROR] Failed to check username {username}. Try again later')

#                 else:
#                     print(f'[UNAVAILABLE] https://www.instagram.com/{username}')

#         except Exception as e:
#             print(f'[ERROR] {str(e)}')

#     async def start(self):
#         async with aiohttp.ClientSession(headers=self.HEADERS) as session:
#             tasks = []
#             for group_key, group_value in self.username_groups.items():
#                 print(f'Loading group starting with {group_key}.. This may take a while.')
#                 for username in group_value:
#                     tasks.append(self._check(session, username))
#             await asyncio.gather(*tasks)


# if __name__ == '__main__':
#     system('title Instagram Username Checker by NightfallGT')
#     system('clear')  # Clear the console screen
#     username_groups = open_file() 
#     checker = Checker(username_groups)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(checker.start())
