import argparse
import os
#import datetime
import json
import tqdm
import requests
#import logging
from libs.strings import *
from libs.networks import model_detect
import libs.preprocessing as preprocessing
import libs.postprocessing as postprocessing
from EditorServices.uploadapp.logger import (logging,logs)
from datetime import date
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv(".env")


finalresponse = []

def __work_mode__(path: str):
    """Determines the desired mode of operation"""
    if os.path.isfile(path):  # Input is file
        logging.info("::file found >")
        return "file"
    if os.path.isdir(path):  # Input is dir
        logging.info(":: dir found >")
        return "dir"
    else:
        return "no"


def __save_image_file__(img, file_name, output_path, wmode):
    """
    Saves the PIL image to a file
    :param img: PIL image
    :param file_name: File name
    :param output_path: Output path
    :param wmode: Work mode
    """
    # create output directory if it doesn't exist
    
    
    folder = os.path.dirname(output_path)
    
    if folder != '':
        os.makedirs(folder, exist_ok=True)
    if wmode == "file":
        
        
        
        file_name_out = os.path.splitext(output_path)
        if file_name_out:
            logging.info("path >>>".format(output_path))
            # Change file extension to png
            logging.info(file_name_out)
            file_name = file_name_out[0] + '.png'
            finalresponse.append(file_name)
            logging.info(file_name)
            # Save image
            logging.info("going to save custom image in database and media".format(file_name))
            #img.save(os.path.join(output_path, file_name))
            img.save(file_name)
        else:
            try:
                # Save image
                logging.info("going to save image in database and media")
                img.save(output_path)
            except OSError as e:
                if str(e) == "cannot write mode RGBA as JPEG":
                    raise logging.info("Error! "
                                  "Please indicate the correct extension of the final file, for example: .png")
                else:
                    raise e
    else:
        # Change file extension to png
        file_name = os.path.splitext(file_name)[0] + '.png'
        # Save image
        logging.info("going to save input image in database and media")
        img.save(os.path.join(output_path, file_name))


def process(input_path, output_path, model_name="u2net",\
            preprocessing_method_name="bbd-fastrcnn", postprocessing_method_name="rtb-bnb"):
    """
    Processes the file.
    :param input_path: The path to the image / folder with the images to be processed.
    :param output_path: The path to the save location.
    :param model_name: Model to use.
    :param postprocessing_method_name: Method for image preprocessing
    :param preprocessing_method_name: Method for image post-processing
    """
    logging.info("process.task >>> started")
    returnData =False
    if input_path is None or output_path is None:
        raise Exception("Bad parameters! Please specify input path and output path.")

    model = model_detect(model_name)  # Load model
    logging.info("going to run process by model %s"%model)
    if not model:
        logging.info("Warning! You specified an invalid model type. "
                       "For image processing, the model with the best processing quality will be used. "
                       "(u2net)")
        model_name = "u2net"  # If the model line is wrong, select the model with better quality.
        logging.info("model name is {}".format(model_name))
        model = model_detect(model_name)  # Load model
    logging.info("preprocessing_method background removal process started")
    preprocessing_method = preprocessing.method_detect(preprocessing_method_name)
    logging.info("postprocessing_method background process started")
    postprocessing_method = postprocessing.method_detect(postprocessing_method_name)
    wmode = __work_mode__(input_path)  # Get work mode

    logging.info(">>>task.process processing completed. task.status success")
    
    returnData = False
    if wmode == "file":  # File work mode
        image = model.process_image(input_path, preprocessing_method, postprocessing_method)
        __save_image_file__(image, os.path.basename(input_path), output_path, wmode)
        returnData = True
        logging.info("sucess.task >>>> True ")

    elif wmode == "dir":  # Dir work mode
        # Start process
        files = os.listdir(input_path)
        for file in tqdm.tqdm(files, ascii=True, desc='Remove Background', unit='image'):
            file_path = os.path.join(input_path, file)
            image = model.process_image(file_path, preprocessing_method, postprocessing_method)
            __save_image_file__(image, file, output_path, wmode)
            logging.info("sucess.task >>>> True ")
            returnData = True
    else:
         logging.info("Bad input parameter! Please indicate the correct path to the file or folder.")
         returnData =False
         logging.info("task.status >>>> failed")
    print ("Image Editor task.status True")
    
    print (returnData)
    if returnData is True:
        url =os.getenv("APIURL","Error Found in url")
        logging.info("API url >> {}".format(url))
        image = finalresponse[0]
        logging.info("o/p image and file id is {} ".format(image,fileId))
    #    now = datetime.now()
     #   createdBy = now.strftime("%d/%m/%Y %H:%M:%S")
    
        data = MultipartEncoder(
                fields={
                    'id' : fileId,
                    'file': (os.path.basename(image), open(image, 'rb'), 'text/plain')
                }
            )
        logging.info("content type is {}".format(data.content_type))
        response = requests.post(url,
                                    data=data,
                                    headers={
                                        'Content-Type': data.content_type
                                 }
                  )
            
        logging.info(response.status_code)
        json_res = json.loads(response.text)
            
        print (json_res)
        logging.info("API response {}".format(json_res))
        if response.status_code != 200:
            #payload["error"] = logs
            logging.error("error found %s"%str(logs),100,ex=True)
        
        else:
            logging.info("total operation performed {}".format(logs))
            logging.info("API response.status success")
            #responseApi = requests.post(url=url, data=payload, headers=headers)
            #logging.info(" {}".format(json.dumps(responseApi.text)))
            #}
    else:
        logging.info("script task.status >>  failed")



def cli():
    """CLI"""
    parser = argparse.ArgumentParser(description=DESCRIPTION, usage=ARGS_HELP)
    parser.add_argument('-i', required=True,
                        help="Path to input file or dir.", action="store", dest="input_path")
    parser.add_argument('-id', required=True,
                        help="identifier", action="store", dest="identifier")
    parser.add_argument('-o', required=True,
                        help="Path to output file or dir.", action="store", dest="output_path")
    parser.add_argument('-m', required=False,
                        help="Model name. Can be {} . U2NET is better to use.".format(MODELS_NAMES),
                        action="store", dest="model_name", default="u2net")
    parser.add_argument('-prep', required=False,
                        help="Preprocessing method. Can be {} . `bbd-fastrcnn` is better to use."
                        .format(PREPROCESS_METHODS),
                        action="store", dest="preprocessing_method_name", default="bbd-fastrcnn")
    parser.add_argument('-postp', required=False,
                        help="Postprocessing method. Can be {} ."
                             " `rtb-bnb` is better to use.".format(POSTPROCESS_METHODS),
                        action="store", dest="postprocessing_method_name", default="rtb-bnb")
    args = parser.parse_args()
    # Parse arguments
    logging.set_log_file("")
    input_path = args.input_path
    output_path = args.output_path
    model_name = args.model_name
    preprocessing_method_name = args.preprocessing_method_name
    postprocessing_method_name = args.postprocessing_method_name
    global fileId
    fileId = args.identifier
    if model_name == "test":
        print(input_path, output_path, model_name, preprocessing_method_name, postprocessing_method_name)
    else:
        process(input_path, output_path, model_name, preprocessing_method_name, postprocessing_method_name)

    


if __name__ == "__main__":
    cli()
    logging.exit_log()
