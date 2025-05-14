#!/usr/bin/env python
# Python 3
# A wrapper around the amazing KNOXSS API (https://knoxss.pro/?page_id=2729) by Brute Logic (@brutelogic)
# Inspired by "knoxssme" by @edoardottt2
# Full help here: https://github.com/xnl-h4ck3r/knoxnl#readme
# Good luck and good hunting! If you really love the tool (or any others), or they helped you find an awesome bounty, consider BUYING ME A COFFEE! (https://ko-fi.com/xnlh4ck3r) ☕ (I could use the caffeine!)

import requests
import argparse
from signal import SIGINT, signal
import multiprocessing.dummy as mp
import multiprocessing
import time
from termcolor import colored
import yaml
import json
import os
import sys
from pathlib import Path
try:
    from . import __version__
except:
    pass
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter, Retry
import re
import time
from urllib.parse import urlparse
from dateutil import tz
import subprocess

# Global variables
stopProgram = False
latestApiCalls = "Unknown"
urlPassed = True
rateLimitExceeded = False
needToStop = False
needToRetry = False
dontDisplay = False
successCountXSS = 0
successCountOR = 0
safeCount = 0
errorCount = 0
requestCount = 0
skipCount = 0
outFile = None
fileIsOpen = False
todoFileName = ''
currentCount = {}
configPath = ''
inputValues = set()
blockedDomains = {}
HTTP_ADAPTER = None
retryAttempt = 0
apiResetPath = ''
timeAPIReset = None
forbiddenResponseCount = 0
latestVersion = ''
runtimeLog = ""

pauseEvent = mp.Event()

DEFAULT_API_URL = 'https://api.knoxss.pro'

# The default timeout for KNOXSS API to respond in seconds
DEFAULT_TIMEOUT = 600

# The default number of times to retry when having issues connecting to the KNOXSS API 
DEFAULT_RETRIES = 3

# The default number of seconds to wait when having issues connecting to the KNOXSS API before retrying
DEFAULT_RETRY_INTERVAL = 30

# The default backoff factor to use when retrying after having issues connecting to the KNOXSS API
DEFAULT_RETRY_BACKOFF_FACTOR = 1.5

# Yaml config values
API_URL = ''
API_KEY = ''
DISCORD_WEBHOOK = ''
DISCORD_WEBHOOK_COMPLETE = ''

# Object for an KNOXSS API response
class knoxss:
    Code = ''
    XSS = ''
    Redir = ''
    PoC = ''
    Calls = ''
    Error = ''
    POSTData = ''
    Timestamp = ''

def showVersion():
    global latestVersion
    try:
        if latestVersion == '':
            print('Current knoxnl version '+__version__+' (unable to check if latest)')
        elif __version__ == latestVersion:
            print('Current knoxnl version '+__version__+' ('+colored('latest','green')+')\n')
        else:
            print('Current knoxnl version '+__version__+' ('+colored('outdated','red')+')\n')
    except:
        pass
    
def showBanner():
    print()
    print(" _           "+colored("_ ___    ","red")+colored("__","yellow")+colored("      _","cyan"))
    print("| | ___ __   "+colored("V","red")+"_"+colored(r"V\ \  ","red")+colored("/ /","yellow")+colored("_ __","green")+colored(" | | ","cyan"))
    print(r"| |/ / '_ \ / _ \ "[:-1]+colored(r"\ \ "[:-1],"red")+colored("/ /","yellow")+colored(r"| '_ \ "[:-1],"green")+colored("| | ","cyan"))
    print("|   <| | | | (_) "+colored("/ /","red")+colored(r"\ \ "[:-1],"yellow")+colored("| | | |","green")+colored(" | ","cyan"))
    print(r"|_|\_\_| |_|\___"+colored("/_/  ","red")+colored(r"\_\ "[:-1],"yellow")+colored("_| |_|","green")+colored("_| ","cyan"))
    print(colored("                 by @Xnl-h4ck3r ","magenta"))
    print()
    try:
        currentDate = datetime.now().date()
        if currentDate.month == 12 and currentDate.day in (24,25):
            print(colored(" *** 🎅 HAPPY CHRISTMAS! 🎅 ***","green",attrs=["blink"]))
        elif currentDate.month == 10 and currentDate.day == 31:
            print(colored(" *** 🎃 HAPPY HALLOWEEN! 🎃 ***","red",attrs=["blink"]))
        elif currentDate.month == 1 and currentDate.day in  (1,2,3,4,5):
            print(colored(" *** 🥳 HAPPY NEW YEAR!! 🥳 ***","yellow",attrs=["blink"]))
        elif currentDate.month == 10 and currentDate.day == 10:
            print(colored(" *** 🧠 HAPPY WORLD MENTAL HEALTH DAY!! 💚 ***","yellow",attrs=["blink"]))
        print()
    except:
        pass
    print(colored('DISCLAIMER: We are not responsible for any use, and especially misuse, of this tool or the KNOXSS API','yellow'))
    print()
    showVersion()

# Functions used when printing messages dependant on verbose options
def verbose():
    return args.verbose

def showBlocked():
    global blockedDomains
    try:
        # Accumulate domains with a count more than the specified limit into a list
        domainsBlockedLimit = [domain for domain, count in blockedDomains.items() if count > args.skip_blocked-1]
        if domainsBlockedLimit:
            # Join the domains into a comma-separated string
            domainList = ', '.join(domainsBlockedLimit)
        
            print(colored('The following domains seem to be blocking KNOXSS and might be worth excluding for now:','yellow'),colored(domainList,'white'))
    except:
        pass
    
# Handle the user pressing Ctrl-C and programatic interupts
def handler(signal_received, frame):
    """
    This function is called if Ctrl-C is called by the user
    An attempt will be made to try and clean up properly
    """
    global stopProgram, needToStop, inputValues, blockedDomains, todoFileName
    stopProgram = True
    pauseEvent.clear()
    if not needToStop:
        print(colored('\n>>> "Oh my God, they killed Kenny... and knoXnl!" - Kyle','red'))
        # If there are any input values not checked, write them to a .todo file, unless the -nt/-no-todo arg was passed
        try:
            if len(inputValues) > 0 and not args.no_todo:
                try:
                    print(colored('\n>>> Just trying to save outstanding input to .todo file before ending...','yellow'))
                    with open(todoFileName, 'w') as file:
                        for inp in inputValues:
                            file.write(inp+'\n')
                    print(colored('All unchecked URLs have been written to','cyan'),colored(todoFileName+'\n', 'white'))
                except Exception as e:
                    print(colored('Error saving file ','cyan'),colored(todoFileName+'\n', 'white'),colored(':'+str(e),'red'))
        except:
            pass
        
        # If there were any domains that might be blocking KNOXSS, let the user know
        if args.skip_blocked > 0:
            showBlocked()
        
        # Try to close the output file before ending
        try:
            outFile.close()
        except:
            pass
        quit()
            
# Show the chosen options and config settings
def showOptions():

    global urlPassed, fileIsOpen, API_URL, timeAPIReset
            
    try:
        print(colored('Selected config and settings:', 'cyan'))
        
        print(colored('Config file path:', 'magenta'), configPath)
        print(colored('KNOXSS API Url:', 'magenta'), API_URL)
        print(colored('KNOXSS API Key:', 'magenta'), API_KEY)    
        print(colored('Discord Webhook:', 'magenta'), DISCORD_WEBHOOK)   
        
        if args.burp_piper:
            print(colored('-i: ' + args.input, 'magenta'), 'Request passed from Burp Piper Extension')
        else:
            if urlPassed:
                print(colored('-i: ' + args.input, 'magenta'), 'The URL to check with KNOXSS API.')
            else:
                print(colored('Discord Webhook Complete:', 'magenta'), DISCORD_WEBHOOK_COMPLETE)  
                print(colored('-i: ' + args.input + ' (FILE)', 'magenta'), 'All URLs will be passed to KNOXSS API.')

        if fileIsOpen:
            print(colored('-o: ' + args.output, 'magenta'), 'The output file where successful XSS payloads will be saved.')
            print(colored('-ow: ' + str(args.output_overwrite), 'magenta'), 'Whether the output will be overwritten if it already exists.')
            print(colored('-oa: ' + str(args.output_all), 'magenta'), 'Whether the output all results to the output file, not just successful one\'s.')
        
        if not urlPassed:
            print(colored('-p: ' + str(args.processes), 'magenta'), 'The number of parallel requests made.')
        
        print(colored('-X: ' + args.http_method, 'magenta'), 'The HTTP method checked by KNOXSS API.')
        
        if args.http_method in ('POST','BOTH'):
            if args.post_data != '':
                print(colored('-pd: ' + args.post_data, 'magenta'), 'Data passed with a POST request.')
            else:
                if urlPassed:
                    try:
                        postData = args.input.split('?')[1]
                    except:
                        postData = ''
                    print(colored('-pd: ' + postData, 'magenta'), 'Data passed with a POST request.')
                else:
                    print(colored('-pd: {the URL query string}', 'magenta'), 'Data passed with a POST request.')
            
        if args.headers != '':
            print(colored('-H: ' + args.headers, 'magenta'), 'HTTP Headers passed with requests.')
            
        print(colored('-t: ' + str(args.timeout), 'magenta'), 'The number of seconds to wait for KNOXSS API to respond.')
  
        if args.retries == 0:
            print(colored('-r: ' + str(args.retries), 'magenta'), 'If having issues connecting to the KNOXSS API, the program will not sleep and not try to retry any URLs. ')
        else:
            print(colored('-r: ' + str(args.retries), 'magenta'), 'The number of times to retry when having issues connecting to the KNOXSS API. ')
        if args.retries > 0:
            print(colored('-ri: ' + str(args.retry_interval), 'magenta'), 'How many seconds to wait before retrying when having issues connecting to the KNOXSS API.')
            print(colored('-rb: ' + str(args.retry_backoff), 'magenta'), 'The backoff factor used when retrying when having issues connecting to the KNOXSS API.')
        
        if args.skip_blocked > 0:
            print(colored('-sb: ' + str(args.skip_blocked), 'magenta'), 'The number of 403 Forbidden responses from a target (for a given HTTP method + scheme + (sub)domain) before skipping.')
        
        if args.force_new:
             print(colored('-fn: True', 'magenta'), 'Forces KNOXSS to do a new scan instead of getting cached results.')
             
        if args.runtime_log:
             print(colored('-rl: True', 'magenta'), 'Provides a live runtime log of the KNOXSS scan.')

        if args.no_todo and not urlPassed:
             print(colored('-nt: True', 'magenta'), 'If the input file is not completed because of issues with API, connection, etc. the .todo file will not be created.')
             
        if timeAPIReset is not None:
            print(colored('KNOXSS API Limit Reset Time:', 'magenta'), str(timeAPIReset.strftime("%Y-%m-%d %H:%M")))  
            if args.pause_until_reset:
                print(colored('-pur: True', 'magenta'), 'If the API limit is reached, the program will pause and then continue again when it has been reset.')
        else:
            if args.pause_until_reset:
                print(colored('-pur: True', 'magenta'), 'NOT POSSIBLE: Unfortunately the API reset time is currently unknown, so the program cannot be paused and continue when the API limit is reached.')
        print()

    except Exception as e:
        print(colored('ERROR showOptions: ' + str(e), 'red'))

# If an API key wasn't supplied, or was invalid, then point the user to https://knoxss.pro
def needApiKey():
    # If the console can't display 🤘 then an error will be raised to try without
    try:
        print(colored('Haven\'t got an API key? Why not head over to https://knoxss.pro and subscribe?\nDon\'t forget to generate and SAVE your API key before using it here! 🤘\n', 'green')) 
    except:
        print(colored('Haven\'t got an API key? Why not head over to https://knoxss.pro and subscribe?\nDon\'t forget to generate and SAVE your API key before using it here!\n', 'green')) 
              
def getConfig():
    # Try to get the values from the config file, otherwise use the defaults
    global API_URL, API_KEY, DISCORD_WEBHOOK, DISCORD_WEBHOOK_COMPLETE, configPath, HTTP_ADAPTER, apiResetPath
    try:
        
        # Put config in global location based on the OS.
        configPath = (
            Path(os.path.join(os.getenv('APPDATA', ''), 'knoxnl')) if os.name == 'nt'
            else Path(os.path.join(os.path.expanduser("~"), ".config", "knoxnl")) if os.name == 'posix'
            else Path(os.path.join(os.path.expanduser("~"), "Library", "Application Support", "knoxnl")) if os.name == 'darwin'
            else None
        )

        # Set up an HTTPAdaptor for retry strategy when making requests
        try:
            retry= Retry(
                total=2,
                backoff_factor=0.1,
                status_forcelist=[429, 500, 502, 503, 504],
                raise_on_status=False,
                respect_retry_after_header=False
            )
            HTTP_ADAPTER = HTTPAdapter(max_retries=retry)
        except Exception as e:
            print(colored('ERROR getConfig 2: ' + str(e), 'red'))
        
        configPath.absolute
        # Set config file path and apireset file path
        if configPath == '':
            apiResetPath = '.apireset'
            configPath = 'config.yml'
        else:
            apiResetPath = Path(configPath / '.apireset')
            configPath = Path(configPath / 'config.yml')
        config = yaml.safe_load(open(configPath))
        
        try:
            API_URL = config.get('API_URL')
        except Exception as e:
            print(colored('Unable to read "API_URL" from config.yml; defaults set', 'red'))
            API_KEY = DEFAULT_API_URL
        try:
            API_KEY = config.get('API_KEY')
            if args.api_key != '':
                API_KEY = args.api_key
                print(colored('NOTE: Overriding "API_KEY" from config.yml with passed API Key', 'cyan'), API_KEY + '\n')
            else:
                if API_KEY is None or API_KEY == 'YOUR_API_KEY':
                    print(colored('ERROR: You need to add your "API_KEY" to config.yml or pass it with the -A option.', 'red'))
                    needApiKey()
                    quit()
        except Exception as e:
            print(colored('Unable to read "API_KEY" from config.yml; We need an API key! - ' + str(e), 'red'))
            needApiKey()
            quit()
        
        # Set the Discord webhook. If passed with argument -dw / --discord-webhook then this will override the config value
        if args.discord_webhook != '':
            DISCORD_WEBHOOK = args.discord_webhook
        else:
            try:
                DISCORD_WEBHOOK = config.get('DISCORD_WEBHOOK').replace('YOUR_WEBHOOK','')
            except Exception as e:
                DISCORD_WEBHOOK = ''
        
        # Set the Discord webhook Complete. If passed with argument -dwc / --discord-webhook-complete then this will override the config value
        if args.discord_webhook_complete != '':
            DISCORD_WEBHOOK_COMPLETE = args.discord_webhook_complete
        else:
            try:
                DISCORD_WEBHOOK_COMPLETE = config.get('DISCORD_WEBHOOK_COMPLETE').replace('YOUR_WEBHOOK','')
            except Exception as e:
                DISCORD_WEBHOOK_COMPLETE = ''
        
    except Exception as e:
        try:
            if args.api_key == '':
                print(colored('Unable to read config.yml and API Key not passed with -A; Unable to use KNOXSS API! - ' + str(e), 'red'))
                needApiKey()
                quit()
            else:
                API_URL = DEFAULT_API_URL
                API_KEY = args.api_key
                print(colored('Unable to read config.yml; using default API URL and passed API Key', 'cyan'))
            DISCORD_WEBHOOK = args.discord_webhook    
            DISCORD_WEBHOOK_COMPLETE = args.discord_webhook_complete    
        except Exception as e:
            print(colored('ERROR getConfig 1: ' + str(e), 'red'))
            
# Call the KNOXSS API
def knoxssApi(targetUrl, headers, method, knoxssResponse):
    global latestApiCalls, rateLimitExceeded, needToStop, dontDisplay, HTTP_ADAPTER, inputValues, needToRetry, requestCount, runtimeLog
    try:
        apiHeaders = {'X-API-KEY' : API_KEY, 
                     'Content-Type' : 'application/x-www-form-urlencoded',
                     'User-Agent' : 'knoXnl tool by @xnl-h4ck3r'
                     }
        
        # Replace any & in the URL with encoded value so we can add other data using &
        targetData = targetUrl.replace('&', '%26')
    
        # Also encode + so it doesn't get converted to space
        targetData = targetData.replace('+', '%2B')
    
        # If processing a POST
        if method == 'POST' and args.http_method in ('POST','BOTH'):
            postData = ''
            
            # If the --post-data argument was passed, use those values
            if args.post_data != '':
                postData = args.post_data.replace('&', '%26').replace('+', '%2B')
                # If the target has query string parameters, remove them
                if '?' in targetUrl:
                    targetData = targetData.split('?')[0]
                    
            else: # post-data not passed
                # If the target has parameters, i.e. ? then replace it with &post=, otherwise add &post= to the end
                if '?' in targetUrl:
                    postData = targetData.split('?')[1]
                    targetData = targetData.split('?')[0]
    
        data = 'target=' + targetData
        
        # Add the post data if necessary
        if method == 'POST':
            data = data + '&post=' + postData
            
        # Add the Force New argument if requested
        if args.force_new:
            data = data + '&new=1'

        # Add the Runtime Log argument if requested
        if args.runtime_log:
            data = data + '&log=1'

        # Add Headers if required
        if headers != '':
            # Headers must be in format header1:value%0D%0Aheader2:value
            encHeaders = headers.replace(' ','%20')
            encHeaders = encHeaders.replace('|','%0D%0A')
            data = data + '&auth=' + encHeaders

        # Make a request to the KNOXSS API
        try:
            tryAgain = True
            while tryAgain:
                tryAgain = False
                fullResponse = None
                try:
                    try:
                        session = requests.Session()
                        session.mount('https://', HTTP_ADAPTER)
                    except Exception as e:
                        print(colored(':( There was a problem setting up a network session: ' + str(e), 'red'))
                        knoxssResponse.Error = 'Some kind of network error occurred before calling KNOXSS'
                        return
                    
                    # If a session timeout of 0 is passed, don't provide a timeout value.
                    requestCount = requestCount + 1
                    if args.timeout == 0:
                        resp = session.post(
                            url=API_URL,
                            headers=apiHeaders,
                            data=data.encode('utf-8')
                        )
                    else:
                        resp = session.post(
                            url=API_URL,
                            headers=apiHeaders,
                            data=data.encode('utf-8'),
                            timeout=args.timeout
                        )
                    fullResponse = resp.text.strip()
                except Exception as e:
                    if args.retries > 0:
                        needToRetry = True
                    if 'failure in name resolution' in str(e).lower():
                        knoxssResponse.Error = 'It appears the internet connection was lost. Please try again later.'
                    elif 'response ended prematurely' in str(e).lower():
                        knoxssResponse.Error = 'The response ended prematurely. This can sometimes happen if you use a VPN. The KNOXSS servers seem to block that.'
                    elif 'failed to establish a new connection' in str(e).lower():
                        knoxssResponse.Error = 'Failing to establish a new connection to KNOXSS. This can happen if there is an issue with the KNOXSS API or can happen if your machine is running low on memory.'
                    elif 'remote end closed connection' in str(e).lower() or 'connection aborted' in str(e).lower():
                        knoxssResponse.Error = 'The KNOXSS API dropped the connection.'
                    elif 'read timed out' in str(e).lower():
                        knoxssResponse.Error = 'The KNOXSS API timed out getting the response (consider changing -t value)'
                    else:
                        knoxssResponse.Error = 'Unhandled error: ' + str(e)
                
                # Display the data sent to API and the response
                if verbose():
                    print('KNOXSS API request:')
                    print('     Data: ' + data)
                    print('KNOXSS API response:')
                    print(fullResponse)
                
                try:    
                    knoxssResponse.Code = str(resp.status_code)
                except:
                    knoxssResponse.Code = 'Unknown'
                
                # Try to get the JSON response
                try:
                        
                    # If the error has "expiration time reset", and we haven't already tried before, set to True to try one more time
                    if 'expiration time reset' in fullResponse.lower():
                        if tryAgain:
                            tryAgain = False
                        else:
                            tryAgain = True
                    else:
                        # If the --runtime-log option was passed, then get the log from the response and separate from the JSON response.
                        if args.runtime_log:
                            jsonPart = ""

                            # Split the fullResponse by lines
                            lines = fullResponse.splitlines()

                            # Find the line containing "{" to separate runtime log and JSON response
                            separator_index = next((i for i, line in enumerate(lines) if '{' in line), None)

                            if separator_index is not None:
                                # Get all lines before the separator and combine into one string for runtimeLog
                                runtimeLog = "\n".join(lines[:separator_index]).strip()
                                
                                # Get the rest as the jsonResponse
                                jsonPart = "\n".join(lines[separator_index:]).strip()
                                    
                            # Get the JSON part of the response
                            jsonResponse = json.loads(jsonPart.strip())
                        else:
                            runtimeLog = ""
                            jsonResponse = json.loads(fullResponse)
                        
                        knoxssResponse.XSS = str(jsonResponse['XSS'])
                        knoxssResponse.Redir = str(jsonResponse['Redir'])
                        knoxssResponse.PoC = str(jsonResponse['PoC'])
                        knoxssResponse.Calls = str(jsonResponse['API Call'])
                        if knoxssResponse.Calls == '0':
                            knoxssResponse.Calls = 'Unknown'
                        knoxssResponse.Error = str(jsonResponse['Error'])
                        
                        # Only check for errors if the PoC is not given
                        if knoxssResponse.PoC != 'none' and ():
                            
                            # If service unavailable flag, or error says "please retry" then retry
                            if 'service unavailable' in knoxssResponse.Error.lower()  or "please retry" in knoxssResponse.Error.lower():
                                if args.retries > 0:
                                    needToRetry = True
                            # If the API rate limit is exceeded, flag to stop
                            elif knoxssResponse.Error == 'API rate limit exceeded.':
                                rateLimitExceeded = True
                                knoxssResponse.Calls = 'API rate limit exceeded!'
                                # Flag to stop if we aren't going to wait until the API limit is reset
                                if not (timeAPIReset is not None and args.pause_until_reset):
                                    needToStop = True
                            else: # remove the URL from the int input set
                                inputValues.discard(targetUrl)
                            
                        knoxssResponse.POSTData = str(jsonResponse['POST Data'])
                        knoxssResponse.Timestamp = str(jsonResponse['Timestamp'])
                    
                except Exception as e:
                    knoxssResponse.Calls = 'Unknown'
                    if fullResponse is None:
                        fullResponse = ''

                    # The response probably wasn't JSON, so check the response message
                    if fullResponse.lower() == 'incorrect apy key.' or fullResponse.lower() == 'invalid or expired api key.':
                        print(colored('The provided API Key is invalid! Check if your subscription is still active, or if you forgot to save your current API key. You might need to login on https://knoxss.pro and go to your Profile and click "Save All Changes".', 'red'))
                        needToStop = True
                        dontDisplay = True
                        
                    elif fullResponse.lower() == 'no api key provided.':
                        print(colored('No API Key was provided! Check config.yml', 'red'))
                        needToStop = True
                        dontDisplay = True

                    elif 'hosting server read timeout' in fullResponse.lower():
                        knoxssResponse.Error = 'Hosting Server Read Timeout'
                    
                    elif 'type of target page can\'t lead to xss' in fullResponse.lower(): 
                        knoxssResponse.Error = 'XSS is not possible with the requested URL'
                        inputValues.discard(targetUrl)
                    
                    elif fullResponse == '':
                        knoxssResponse.Error = 'Empty response from API'
                        
                    else:
                        print(colored('Something went wrong: '+str(e),'red'))
                        # remove the URL from the int input set
                        inputValues.discard(targetUrl)
                            
                if knoxssResponse.Calls != 'Unknown' and knoxssResponse.Calls != '':
                    latestApiCalls = knoxssResponse.Calls
                        
        except Exception as e:
            knoxssResponse.Error = 'FAIL'
            print(colored(':( There was a problem calling KNOXSS API: ' + str(e), 'red'))
            
    except Exception as e:
        print(colored('ERROR knoxss 1:  ' + str(e), 'red'))

def checkForAlteredParams(url):
    # Show a warning if it looks like the user has tampered with the parameter values before sending to knoxnl. Some indications of this are using FUZZ and also Gxss.
    # Show a warning if any XSS payloads appear to be included in the URL already
    try:
        if '=FUZZ' in url or '=Gxss' in url:
            print(colored('WARNING: It appears the URL may have been manually changed by yourself (or another tool) first. KNOXSS might not work as expected without the default values of parameters (some parameters might be value sensitive). Just pass original URLs to knoxnl.', 'yellow'))
        regexCheck = r'<[A-Z]+|alert([^\}]*)|javascript:'
        regexCheckCompiled = re.compile(regexCheck, re.IGNORECASE)
        if regexCheckCompiled.search(url):
            print(colored('WARNING: It appears the URL may already include some XSS payload. If that\'s correct, KNOXSS won\'t work as expected since it\'s not meant to receive XSS payloads, but to provide them.', 'yellow'))
    except Exception as e:
        print(colored('ERROR checkForAlteredParams 1:  ' + str(e), 'red'))
        
def processInput():
    global urlPassed, latestApiCalls, stopProgram, inputValues, todoFileName
    try:
        latestApiCalls = 'Unknown'

        # if the Burp Piper Extension argument was passed, assume the input is passed by stdin 
        if args.burp_piper:
            try:
                # Get URL and 
                firstLine = sys.stdin.readline()
                # Get HOST header
                secondLine = sys.stdin.readline()
                args.input = 'https://'+secondLine.split(' ')[1].strip()+firstLine.split(' ')[1].strip()
                # Get first header after HOST
                headers = ''
                header = sys.stdin.readline()
                # Get all headers
                while header.strip() != '':
                    if header.lower().find('cookie') >= 0 or header.lower().find('api') >= 0 or header.lower().find('auth') >= 0:
                        headers = headers + header.strip()+'|'
                    header = sys.stdin.readline()
                args.headers = headers.rstrip('|')
                # Get the POST body
                postBody = ''
                postBodyLine = sys.stdin.readline()
                while postBodyLine.strip() != '':
                    postBody = postBody + postBodyLine.strip()
                    postBodyLine = sys.stdin.readline()
                postBody = postBody.replace('&', '%26')
                args.post_data = postBody
                
            except Exception as e:
                print(colored('ERROR: Burp Piper Extension input expected: ' + str(e), 'red'))
                exit()
        else:
            # Check that the -i argument was passed
            if not args.input:
                print(colored('ERROR: The -i / --input argument must be passed (unless calling from Burp Piper extension with -bp / --burp-piper). The input can be a single URL or a file or URLs.', 'red'))
                exit()
            
            # Set .todo file name in case we need later
            # If the existing filename already has ".YYYYMMDD_HHMMSS.todo" at the end, then remove it before creating the new name
            originalFileName = args.input
            pattern = r'\.\d{8}_\d{6}\.todo$'
            if re.search(pattern, originalFileName):
                originalFileName = re.sub(pattern, '', originalFileName)
            todoFileName = originalFileName+'.'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.todo'
                     
            # If the -i (--input) can be a standard file (text file with URLs per line),
            # if the value passed is not a valid file, then assume it is an individual URL
            urlPassed = False
            try:
                inputFile = open(args.input, 'r')
                firstLine = inputFile.readline()
            except IOError:
                urlPassed = True
            except Exception as e:
                print(colored('ERROR processInput 2: ' + str(e), 'red'))
        
        if verbose():
            showOptions()
        
        inputArg = args.input
        if urlPassed:
            print(colored('Calling KNOXSS API...\n', 'cyan'))
            # Check if input has scheme. If not, then add https://
            if '://' not in inputArg:
                print(colored('WARNING: Input "'+inputArg+'" should include a scheme. Using https by default...', 'yellow'))
                inputArg = 'https://'+inputArg
            # Check for non default values of parameters
            checkForAlteredParams(inputArg)

            processUrl(inputArg)
        else: # It's a file of URLs
            try:
                # Open file and put all values in input set
                with open(inputArg, 'r') as inputFile:
                    lines = inputFile.readlines()          
                for line in lines:
                    if line.strip() != '':
                        inputValues.add(line.strip())

                print(colored('Calling KNOXSS API for '+str(len(inputValues))+' targets...\n', 'cyan'))
                if not stopProgram:
                    p = mp.Pool(args.processes)
                    p.map(processUrl, inputValues)
                    p.close()
                    p.join()

            except Exception as e:
                print(colored('ERROR processInput 3: ' + str(e), 'red'))
                
    except Exception as e:
        print(colored('ERROR processInput 1: ' + str(e), 'red'))

def discordNotify(target,poc,vulnType):
    global DISCORD_WEBHOOK
    try:
        embed = {
            "description": "```\n"+poc+"\n```",
            "title": "KNOXSS POC for "+target,
            "color": 42320,  # Green
            "fields": [
                {
                    "name": "",
                    "value": "[☕ Buy me a coffee, Thanks!](https://ko-fi.com/xnlh4ck3r)", 
                    "inline": False
                }
            ]
        }
        data = {
            "content": vulnType + " found by knoxnl! 🤘",
            "username": "knoxnl",
            "embeds": [embed],
            "avatar_url": "https://avatars.githubusercontent.com/u/84544946"
        }
        try:
            result = requests.post(DISCORD_WEBHOOK, json=data)
            if 300 <= result.status_code < 200:
                print(colored('WARNING: Failed to send notification to Discord - ' + result.json(), 'yellow'))
        except Exception as e:
            print(colored('WARNING: Failed to send notification to Discord - ' + str(e), 'yellow'))
    except Exception as e:
        print(colored('ERROR discordNotify 1: ' + str(e), 'red'))

def discordNotifyComplete(input, description, incomplete):
    global DISCORD_WEBHOOK_COMPLETE
    try:
        if incomplete:
            title = "INCOMPLETE FOR FILE `"+input+"`"
            embed_color = 16711722  # Red
        else:
            title = "COMPLETE FOR FILE `"+input+"`"
            embed_color = 42320  # Green

        embed = {
            "description": description,
            "title": title,
            "color": embed_color,
            "fields": [
                {
                    "name": "",
                    "value": "[☕ Buy me a coffee, Thanks!](https://ko-fi.com/xnlh4ck3r)", 
                    "inline": False
                }
            ]
        }

        data = {
            "content": "knoxnl finished!",
            "username": "knoxnl",
            "avatar_url": "https://avatars.githubusercontent.com/u/84544946",
            "embeds": [embed],
        }

        try:
            result = requests.post(DISCORD_WEBHOOK_COMPLETE, json=data)
            if 300 <= result.status_code < 200:
                print(colored('WARNING: Failed to send notification to Discord - ' + result.json(), 'yellow'))
        except Exception as e:
            print(colored('WARNING: Failed to send notification to Discord - ' + str(e), 'yellow'))

    except Exception as e:
        print(colored('ERROR discordNotifyComplete 1: ' + str(e), 'red'))
        
def getAPILimitReset():
    global apiResetPath, timeAPIReset
    try:
        # If the .apireset file exists then get the API reset time
        if os.path.exists(apiResetPath):
            # Read the timestamp from the file
            with open(apiResetPath, 'r') as file:
                timeAPIReset = datetime.strptime(file.read().strip(), '%Y-%m-%d %H:%M')
    
        # If the timestamp is more than 24 hours ago, then delete the file and set the timeAPIReset back to None
        if timeAPIReset is not None and (datetime.now() - timeAPIReset) > timedelta(hours=24):
            timeAPIReset = None
            # If the .apireset file already exists then delete it
            if os.path.exists(apiResetPath):
                os.remove(apiResetPath)

    except Exception as e:
        print(colored('ERROR getAPILimitReset 1: ' + str(e), 'red'))
        
def setAPILimitReset(timestamp):
    global apiResetPath, latestApiCalls, timeAPIReset
    try:
        # Convert the timestamp to the local timezone and add 24 hours and 5 minutes
        timestamp = datetime.strptime(timestamp, '%a, %d %b %Y %H:%M:%S %z')
        localTimezone = tz.tzlocal()
        localTimestamp = timestamp.astimezone(localTimezone)
        timeAPIReset = localTimestamp + timedelta(hours=24, minutes=5)

        # If the .apireset file already exists then delete it
        if os.path.exists(apiResetPath):
            os.remove(apiResetPath)
            
        # Write the new API limit reset time to the .apireset file, and set the global variable
        with open(apiResetPath, 'w') as file:
            file.write(timeAPIReset.strftime('%Y-%m-%d %H:%M'))
        
    except Exception as e:
        print(colored('ERROR setAPILimitReset 1: ' + str(e), 'red'))
        
def processOutput(target, method, knoxssResponse):
    global latestApiCalls, successCountXSS, successCountOR, outFile, currentCount, rateLimitExceeded, urlPassed, needToStop, dontDisplay, blockedDomains, needToRetry, forbiddenResponseCount, errorCount, safeCount, requestCount, skipCount, runtimeLog
    try:
        if knoxssResponse.Error != 'FAIL':
                
            if knoxssResponse.PoC != 'none' and knoxssResponse.Error != 'none':
                if not args.success_only:
                    knoxssResponseError = knoxssResponse.Error
                    # If there is a 403, it maybe because the users IP is blocked on the KNOXSS firewall
                    if knoxssResponse.Code == "403":
                       knoxssResponseError = '403 Forbidden - Check http://knoxss.pro manually and if you are blocked, contact Twitter/X @KN0X55 or brutelogic@null.net'
                       needToStop = True
                    # If there is "InvalidChunkLength" in the error returned, it means the KNOXSS API returned an empty response
                    elif 'InvalidChunkLength' in knoxssResponseError:
                        knoxssResponseError = 'The API Timed Out'
                        if args.retries > 0:
                            needToRetry = True
                    # If the error has "can\'t test it (forbidden)" it means the a 403 was returned by the target
                    elif 'can\'t test it (forbidden)' in knoxssResponseError:
                        knoxssResponseError = 'Target returned a "403 Forbidden". There could be WAF in place.'
                        # If requested to skip blocked domains after a limit, then save them
                        if args.skip_blocked > 0:
                            try:
                                parsedTarget = urlparse(target)
                                domain = '(' + method + ') ' + str(parsedTarget.scheme + '://' + parsedTarget.netloc)
                                pauseEvent.set()
                                blockedDomains[domain] = blockedDomains.get(domain, 0) + 1
                                pauseEvent.clear()
                            except:
                                pass
                        
                    # If method is POST, remove the query string from the target and show the post data in [ ] 
                    if method == 'POST':
                        try:
                            querystring = target.split('?')[1]
                        except:
                            querystring = ''
                        target = target.split('?')[0]
                        if args.post_data:
                            target = target + ' ['+args.post_data+']'
                        else:
                            if querystring != '':
                                target = target + ' [' + querystring + ']'                            
                    
                    if not dontDisplay:        
                        xssText = '[ ERR! ] - (' + method + ') ' + target + '  KNOXSS ERR: ' + knoxssResponseError
                        errorCount = errorCount + 1
                        if urlPassed:
                            print(colored(xssText, 'red'))
                        else:
                            print(colored(xssText, 'red'), colored('['+latestApiCalls+']','white'))
                        if args.output_all and fileIsOpen:
                            outFile.write(xssText + '\n')
            else:
                # If it is a new reset time then replace the .apireset file
                if knoxssResponse.Timestamp != '' and latestApiCalls.startswith('1/'):
                    setAPILimitReset(knoxssResponse.Timestamp)
                    
                if knoxssResponse.XSS == 'true':
                    xssText = '[ XSS! ] - (' + method + ') ' + knoxssResponse.PoC
                    if urlPassed:
                        print(colored(xssText, 'green'))
                    else:
                        print(colored(xssText, 'green'), colored('['+latestApiCalls+']','white'))
                    successCountXSS = successCountXSS + 1
                    
                    # If there was an Open Redirect too, then increment that count
                    if knoxssResponse.Redir == 'true':
                        vulnType = 'XSS (and OR)'
                    else:
                        vulnType = 'XSS'
                        
                    # Send a notification to discord if a webhook was provided
                    if DISCORD_WEBHOOK != '':
                        discordNotify(target,knoxssResponse.PoC,vulnType)
                        
                    # Write the successful XSS details to file
                    if fileIsOpen:
                        outFile.write(xssText + '\n')
                        
                elif knoxssResponse.Redir == 'true':
                    orText = '[ OR ! ] - (' + method + ') ' + knoxssResponse.PoC
                    if urlPassed:
                        print(colored(orText, 'green'))
                    else:
                        print(colored(orText, 'green'), colored('['+latestApiCalls+']','white'))
                    successCountOR = successCountOR + 1
                    
                    # Send a notification to discord if a webhook was provided
                    if DISCORD_WEBHOOK != '':
                        discordNotify(target,knoxssResponse.PoC, 'Open Redirect')
                        
                    # Write the successful OR details to file
                    if fileIsOpen:
                        outFile.write(orText + '\n')
                        
                else:
                    if not args.success_only:
                        xssText = '[ NONE ] - (' + method + ') ' + target
                        safeCount = safeCount + 1
                        if urlPassed:
                            print(colored(xssText, 'yellow'))
                        else:
                            print(colored(xssText, 'yellow'), colored('['+latestApiCalls+']','white'))
                        if args.output_all and fileIsOpen:
                            outFile.write(xssText + '\n') 
            
            # If --runtime-log option selected, show the log. If verbose is selected, then don't display them
            # because it will already be displayed as part of the response
            if args.runtime_log and not args.verbose:
                print(runtimeLog)
                   
    except Exception as e:
        print(colored('ERROR showOutput 1: ' + str(e), 'red'))

# Process one URL        
def processUrl(target):
    
    global stopProgram, latestApiCalls, urlPassed, needToStop, needToRetry, retryAttempt, rateLimitExceeded, timeAPIReset, skipCount, apiResetPath
    try:    
        # If the event is set, pause for a while until its unset again
        while pauseEvent.is_set() and not stopProgram and not needToStop:
            time.sleep(1)
        
        if not stopProgram and not needToStop:
            
            # If the API Limit was exceeded, and we want to wait until the limit is reset pause all processes until that time
            if rateLimitExceeded and timeAPIReset is not None and args.pause_until_reset:
                # Set the event to pause all processes
                pauseEvent.set()
                print(colored(f'WAITING UNTIL {str(timeAPIReset.strftime("%Y-%m-%d %H:%M"))} WHEN THEN API LIMIT HAS BEEN RESET...','yellow'))
                time_difference = (timeAPIReset - datetime.now()).total_seconds()
                timeAPIReset = None
                os.remove(apiResetPath)
                time.sleep(time_difference)
                print(colored('API LIMIT HAS BEEN RESET. RESUMING...','yellow'))
                # Reset the event for to unpause all processes
                pauseEvent.clear()
                    
            # If we need to try again because of an KNOXSS error, then delay
            if needToRetry and args.retries > 0:
                if retryAttempt < args.retries:
                    # Set the event to pause all processes
                    pauseEvent.set()
                    needToRetry = False
                    if retryAttempt == 0:
                        delay = args.retry_interval * 1.0
                    else:
                        delay = args.retry_interval * (retryAttempt * args.retry_backoff)
                    if retryAttempt == args.retries:
                        print(colored('WARNING: There are issues with KNOXSS API. Sleeping for ' + str(delay) + ' seconds before trying again. Last retry.', 'yellow'))
                    else:
                        print(colored('WARNING: There are issues with KNOXSS API. Sleeping for ' + str(delay) + ' seconds before trying again.', 'yellow'))
                    retryAttempt += 1
                    time.sleep(delay)
                    # Reset the event for the next iteration
                    pauseEvent.clear()
                else:
                    needToStop = True
                   
            target = target.strip()
            # Check if target has scheme. If not, then add https://
            if '://' not in target:
                print(colored('WARNING: Input "'+target+'" should include a scheme. Using https by default...', 'yellow'))
                target = 'https://'+target
            
            # If the domain has already been flagged as blocked, then skip it and remove from the input values so not written to the .todo file
            parsedTarget = urlparse(target)
 
            headers = args.headers.strip()
            knoxssResponse=knoxss()        

            if args.http_method in ('GET','BOTH'): 
                method = 'GET'
                domain = '(' + method + ') ' + str(parsedTarget.scheme + '://' + parsedTarget.netloc)
                
                # If skipping blocked domains was requested, check if the domain is in blockedDomains, if not, add it with count 0
                if args.skip_blocked > 0:
                    while pauseEvent.is_set():
                        time.sleep(1)
                    pauseEvent.set()
                    if domain not in blockedDomains:
                        blockedDomains[domain] = 0
                    pauseEvent.clear()
                
                # If skipping blocked domains was requested and the domain has been blocked more than the requested number of times, then skip, otherwise process  
                if args.skip_blocked > 0 and blockedDomains[domain] > args.skip_blocked-1:
                    print(colored('[ SKIP ] - ' + domain + ' has already been flagged as blocked, so skipping ' + target, 'yellow', attrs=['dark']))
                    skipCount = skipCount + 1
                    inputValues.discard(target)
                else:
                    knoxssApi(target, headers, method, knoxssResponse)
                    processOutput(target, method, knoxssResponse)
        
            if args.http_method in ('POST','BOTH'): 
                method = 'POST'
                domain = '(' + method + ') ' + str(parsedTarget.scheme + '://' + parsedTarget.netloc)
                
                # If skipping blocked domains was requested, check if the domain is in blockedDomains, if not, add it with count 0
                if args.skip_blocked > 0:
                    while pauseEvent.is_set():
                        time.sleep(1)
                    pauseEvent.set()
                    if domain not in blockedDomains:
                        blockedDomains[domain] = 0
                    pauseEvent.clear()
                
                # If skipping blocked domains was requested and the domain has been blocked more than the requested number of times, then skip, otherwise process  
                if args.skip_blocked > 0 and blockedDomains[domain] > args.skip_blocked-1:
                    print(colored('[ SKIP ] - ' + domain + ' has already been flagged as blocked, so skipping ' + target, 'yellow', attrs=['dark']))
                    skipCount = skipCount + 1
                    inputValues.discard(target)
                else:
                    knoxssApi(target, headers, method, knoxssResponse)
                    processOutput(target, method, knoxssResponse)

    except Exception as e:
        pauseEvent.clear()
        print(colored('ERROR processUrl 1: ' + str(e), 'red'))   

# Validate the -p argument 
def processes_type(x):
    x = int(x) 
    if x < 1 or x > 5:
        raise argparse.ArgumentTypeError('The number of processes must be between 1 and 5')     
    return x

def updateProgram():
    try:
        # Execute pip install --upgrade knoxnl
        subprocess.run(['pip', 'install', '--upgrade', 'knoxnl'], check=True)
        print(colored(f'knoxnl successfully updated {__version__} -> {latestVersion} (latest) 🤘', 'green'))
    except subprocess.CalledProcessError as e:
        print(colored(f'Unable to update knoxnl to version {latestVersion}: {str(e)}', 'red'))
                                       
# Run knoXnl
def main():
    global args, latestApiCalls, urlPassed, successCountXSS, successCountOR, fileIsOpen, outFile, needToStop, todoFileName, blockedDomains, latestVersion, safeCount, errorCount, requestCount, skipCount, DISCORD_WEBHOOK_COMPLETE
    
    # Tell Python to run the handler() function when SIGINT is received
    signal(SIGINT, handler)

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='knoXnl - by @Xnl-h4ck3r: A wrapper around the KNOXSS API by Brute Logic (requires an API key)'    
    )
    parser.add_argument(
        '-i',
        '--input',
        action='store',
        help='Input to send to KNOXSS API: a single URL, or file of URLs.',
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        help='The file to save the successful XSS and payloads to. If the file already exist it will just be appended to unless option -ow is passed.',
        default='',
    )
    parser.add_argument(
        '-ow',
        '--output-overwrite',
        action='store_true',
        help='If the output file already exists, it will be overwritten instead of being appended to.',
    )
    parser.add_argument(
        '-oa',
        '--output-all',
        action='store_true',
        help='Output all results to file, not just successful one\'s.',
    )
    parser.add_argument(
        '-X',
        '--http-method',
        action='store',
        help='Which HTTP method to use, values GET, POST or BOTH (default: GET). If BOTH is chosen, then a GET call will be made, followed by a POST.',
        default='GET',
        choices=['GET','POST','BOTH']
    )
    parser.add_argument(
        '-pd',
        '--post-data',
        help='If a POST request is made, this is the POST data passed. It must be in the format \'param1=value&param2=value&param3=value\'. If this isn\'t passed and query string parameters are used, then these will be used as POST data if POST Method is requested.',
        action='store',
        default='',
    )
    parser.add_argument(
        '-H',
        '--headers',
        help='Add custom headers to pass with HTTP requests. Pass in the format \'Header1:value1|Header2:value2\' (e.g. separate different headers with a pipe | character).',
        action='store',
        default='',
    )
    parser.add_argument(
        '-A',
        '--api-key',
        help='The KNOXSS API Key to use. This will be used instead of the value in config.yml',
        action='store',
        default='',
    )
    parser.add_argument(
        '-s',
        '--success-only',
        action='store_true',
        help='Only show successful XSS payloads in the CLI output.',
    )
    parser.add_argument(
        '-p',
        '--processes',
        help='Basic multithreading is done when getting requests for a file of URLs. This argument determines the number of processes (threads) used (default: 3)',
        action='store',
        type=processes_type,
        default=3,
        metavar="<integer>",
    )
    parser.add_argument(
        '-t',
        '--timeout',
        help='How many seconds to wait for the KNOXSS API to respond before giving up (default: '+str(DEFAULT_TIMEOUT)+' seconds). If set to 0, then timeout will be used.',
        default=DEFAULT_TIMEOUT,
        type=int,
        metavar="<seconds>",
    )
    parser.add_argument(
        '-bp',
        '--burp-piper',
        action='store_true',
        help='Set if called from the Burp Piper extension.',
    )
    parser.add_argument(
        '-dw',
        '--discord-webhook',
        help='The Discord Webhook to send successful XSS notifications to. This will be used instead of the value in config.yml',
        action='store',
        default='',
    )
    parser.add_argument(
        '-dwc',
        '--discord-webhook-complete',
        help='The Discord Webhook to send completion notifications to when a file has been used as input  (whether finished completely or stopped in error). This will be used instead of the value in config.yml.',
        action='store',
        default='',
    )
    parser.add_argument(
        '-r',
        '--retries',
        help='The number of times to retry when having issues connecting to the KNOXSS API (default: '+str(DEFAULT_RETRIES)+'). If set to 0 then then it will not sleep or try to retry any URLs.',
        default=DEFAULT_RETRIES,
        type=int,
    )
    parser.add_argument(
        '-ri',
        '--retry-interval',
        help='How many seconds to wait before retrying when having issues connecting to the KNOXSS API (default: '+str(DEFAULT_RETRY_INTERVAL)+' seconds)',
        default=DEFAULT_RETRY_INTERVAL,
        type=int,
        metavar="<seconds>",
    )
    parser.add_argument(
        '-rb',
        '--retry-backoff',
        help='The backoff factor used when retrying when having issues connecting to the KNOXSS API (default: '+str(DEFAULT_RETRY_BACKOFF_FACTOR)+')',
        default=DEFAULT_RETRY_BACKOFF_FACTOR,
        type=float,
    )
    parser.add_argument(
        '-pur',
        '--pause-until-reset',
        action='store_true',
        help='If the API Limit reset time is known and the API limit is reached, wait the required time until the limit is reset and continue again. The reset time is only known if knoxnl has run for request number 1 previously. The API rate limit is reset 24 hours after request 1.',
    )
    parser.add_argument(
        '-sb',
        '--skip-blocked',
        help='The number of 403 Forbidden responses from a target (for a given HTTP method + scheme + (sub)domain) before skipping. This is useful if you know the target has a WAF. The default is zero, which means no blocking is done.',
        default=0,
        type=int,
    )
    parser.add_argument(
        '-fn',
        '--force-new',
        action='store_true',
        help='Forces KNOXSS to run a new scan instead of getting cached results.',
    )
    parser.add_argument(
        '-rl',
        '--runtime-log',
        action='store_true',
        help='Provides a live runtime log of the KNOXSS scan.',
    )
    parser.add_argument(
        '-nt',
        '--no-todo',
        action='store_true',
        help='Do not create the .todo file if the input file is not completed because of issues with API, connection, etc.',
    )
    parser.add_argument(
        '-up',
        '--update',
        action='store_true',
        help='Update knoxnl to the latest version.',
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    parser.add_argument('--version', action='store_true', help="Show version number")
    args = parser.parse_args()

    # If --version was passed, display version and exit
    if args.version:
        print(colored('knoxnl - v' + __version__,'cyan'))
        sys.exit()

    # Get the latest version
    try:
        resp = requests.get('https://raw.githubusercontent.com/xnl-h4ck3r/knoxnl/main/knoxnl/__init__.py',timeout=3)
        latestVersion = resp.text.split('=')[1].replace('"','')
    except:
        pass
                        
    showBanner()

    # If --update was passed, update to the latest version
    if args.update:
        try:
            if latestVersion == '':
                print(colored('Unable to check the latest version. Check your internet connection.', 'red'))
            elif __version__ != latestVersion:
                updateProgram()
                sys.exit()
        except Exception as e:
            print(colored(f'ERROR: Unable to update - {str(e)}','red'))
             
    # If no input was given, raise an error
    if sys.stdin.isatty():
        if args.input is None:
            print(colored('You need to provide an input with -i argument or through <stdin>.', 'red'))
            sys.exit()
            
    # Get the config settings from the config.yml file
    getConfig()
    
    # Get the API reset time from the .apireset file
    getAPILimitReset()

    # If -o (--output) argument was passed then open the output file
    if args.output != "":
        try:
            # If the filename has any "/" in it, remove the contents after the last one to just get the path and create the directories if necessary
            try:
                output_path = os.path.abspath(os.path.expanduser(args.output))
                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            except Exception as e:
                pass
            # If argument -ow was passed and the file exists, overwrite it, otherwise append to it
            if args.output_overwrite:
                outFile = open(os.path.expanduser(args.output), "w")
            else:
                outFile = open(os.path.expanduser(args.output), "a")
            fileIsOpen = True
        except Exception as e:
            print(colored('WARNING: Output won\'t be saved to file - ' + str(e) + '\n', 'red'))
                                
    try:

        processInput()
        
        completeDescription = ""
        
        # Show the user the latest API quota       
        if latestApiCalls is None or latestApiCalls == '':
            latestApiCalls = 'Unknown'
        if timeAPIReset is not None:
            message = '\nAPI calls made so far today - ' + latestApiCalls + ' (API Limit Reset Time: ' +str(timeAPIReset.strftime("%Y-%m-%d %H:%M")) + ')\n'
            print(colored(message, 'cyan'))
            completeDescription = message
        else:
            message = '\nAPI calls made so far today - ' + latestApiCalls + '\n'
            print(colored(message, 'cyan'))
            completeDescription = message
           
        # If a file was passed, there is a reason to stop, write the .todo file and let the user know about it (unless -nt/--no-todo was passed)
        if needToStop and not urlPassed and not args.burp_piper and not args.no_todo:
            try:
                with open(todoFileName, 'w') as file:
                    for inp in inputValues:
                        file.write(inp+'\n')
                print(colored('Had to stop due to errors. All unchecked URLs have been written to','cyan'),colored(todoFileName+'\n', 'white'))
                completeDescription = completeDescription + 'Had to stop due to errors. All unchecked URLs have been written to `'+todoFileName+'`\n'
            except Exception as e:
                message = 'Was unable to write .todo file: '+str(e)+'\n'
                print(colored(message,'red'))
                completeDescription = completeDescription + message
        
        if args.skip_blocked > 0:
            showBlocked()
        
        # Report number of None, Error and Skipped results
        if args.skip_blocked > 0:
            message = f'Requests made to KNOXSS API: {str(requestCount)} (XSS!: {str(successCountXSS)}, OR!: {str(successCountOR)}, NONE: {str(safeCount)}, ERR!: {str(errorCount)}, SKIP: {str(skipCount)})'
            print(colored(message,'cyan'))
        else:
            message = f'Requests made to KNOXSS API: {str(requestCount)} (XSS!: {str(successCountXSS)}, OR!: {str(successCountOR)}, NONE: {str(safeCount)}, ERR!: {str(errorCount)})'
            print(colored(message,'cyan'))
        completeDescription = completeDescription + message + '\n'
             
        # Report if any successful XSS or Open Redirect was found this time. 
        # If the console can't display 🤘 then an error will be raised to try without
        try:
            message = ""
            if successCountOR == 1:
                openRedirectTerm = 'Open Redirect'
            else: 
                openRedirectTerm = 'Open Redirects'
            if successCountXSS > 0 and successCountOR > 0:
                message = '🤘 '+str(successCountXSS)+' successful XSS found and '+str(successCountOR)+' successful '+openRedirectTerm+' found! 🤘\n'
                print(colored(message,'green'))
            else:
                if successCountXSS > 0:
                    message = '🤘 '+str(successCountXSS)+' successful XSS found! 🤘\n'
                    print(colored(message,'green'))
                elif successCountOR > 0:
                    message = '🤘 No successful XSS, but '+str(successCountOR)+' successful '+openRedirectTerm+' found! 🤘\n'
                    print(colored(message,'green'))
                else:
                    message = 'No successful XSS or '+openRedirectTerm+' found... better luck next time! 🤘\n'
                    print(colored(message,'cyan'))
        except:
            print(colored('ERROR: ' + str(e), 'red'))   
        completeDescription = completeDescription + message
        
        # If the output was sent to a file, close the file
        if fileIsOpen:
            try:
                outFile.close()
            except Exception as e:
                print(colored("ERROR: Unable to close output file: " + str(e), "red"))
        
        # If a file was passed as input and the Discord webhook for Completion was given, then send an appropriate notification
        if not urlPassed and not args.burp_piper and DISCORD_WEBHOOK_COMPLETE != '':
            discordNotifyComplete(args.input,completeDescription,needToStop)
                        
    except Exception as e:
        print(colored('ERROR main 1: ' + str(e), 'red'))
        
if __name__ == '__main__':
    main()
