import argparse
from subprocess import PIPE, CalledProcessError, check_call, Popen,call
from operator import eq
import json
from dotenv import load_dotenv
import os,re,sys
import ast

def background_removal(command):

    try:
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output_cmd, output_errors = process.communicate()

        if eq(process.returncode, int(0)):
            logging.info("updating powershell response.")
            json_dump = ast.literal_eval(json.dumps(output_cmd, \
                                                    ensure_ascii=False).encode('utf8'))
            return_response = json.loads(json_dump, encoding='utf8')
            print ("script has been successfully completed")
            return True
        else:
            return False

    except CalledProcessError as e:
        print ("Fatal error found")