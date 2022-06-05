import requests, json, random, time

from colorama import Fore
from selenium import webdriver
from selenium import *

with open("config.json") as f:
    config = json.load(f)
    token_file = config["token_file"]

    """

    Multiple invites can be used for the case that there is a
    bot preventing a mass amount of accounts from joining
    using the same invite.


    
    Make sure that invites are just the code and not the entire link

    Example: discord.gg/invite -> invite

    """

    invites_file = config["invites_file"]


with open(token_file) as f:
    tokens = f.read().split("\n")

with open(invites_file) as f:
    invites = f.read().split("\n")

def print_err(msg):
    print(Fore.RED + msg + Fore.RESET)

def print_yel(msg):
    print(Fore.YELLOW + msg + Fore.RESET)

def print_info(msg):
    print(Fore.GREEN + msg + Fore.RESET)

if input("Do you want to check the tokens first? (y/n) ").lower() == "y":
    for token in tokens:
        valid_tokens = []
        r = requests.post(f'https://discord.com/api/v6/invite/{random.randint(1, 999999)}', headers={'Authorization': token})

        if "You need to verify your account in order to perform this action." in r.text or "401: Unauthorized" in r.text:
            print_err(f"{token} is invalid")
        else:
            print_info(f"{token} is valid")
            valid_tokens.append(token)
    with open(token_file, "w") as f:
        f.write("\n".join(valid_tokens))
    print_info("Finished checking all tokens")
    tokens = valid_tokens

def make_login_script(token):
    return """document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"TOKEN"`; setTimeout(() =>{location.reload();}, 2500)""".replace("TOKEN", token)

def make_join_script(token, invite):
    return 'fetch("https://discord.com/api/v9/invites/invite-goes-here", {"headers": {"authorization": "token",},"body": "{}","method": "POST",});'.replace("invite-goes-here", invite).replace("token", token)

print_info("Opening chrome webdriver")
driver = webdriver.Chrome()
driver.get("https://discord.com/login")
print("Waiting 10 seconds for the page to load")
time.sleep(10)
print_info("\nStarting to join with all tokens\n")

for token in tokens:
    driver.execute_script(make_login_script(token))
    time.sleep(1)
    print_info(f"Logged in with {token}")
    invite = random.choice(invites)
    driver.execute_script(make_join_script(token, invite))
    print_yel(f"Attempted to join with token \"{token}\" and \"{invite}\"")
    time.sleep(.5)
