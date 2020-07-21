#import argparse
from subprocess import PIPE, CalledProcessError, check_call, Popen,call
from operator import eq
#import json
from dotenv import load_dotenv
#import os,re,sys
#import ast
from uploadapp.logger import (logs,logging)

def background_removal(command):

    try:
       # logging.set_log_file("")
        logging.info("subprocess calling main script")
        
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output_cmd, output_errors = process.communicate()


        if eq(process.returncode, int(0)):
          #  logging.info("updating powershell response.")
          #  json_dump = ast.literal_eval(json.dumps(output_cmd, \
            #                                        ensure_ascii=False).encode('utf8'))
           # return_response = json.loads(json_dump, encoding='utf8')
            logging.info("task.status success")
            return True
        else:
            logging.info("task.status False")
            return False

    except CalledProcessError as e:
        logging.info("Fatal error found")
        return False

    
