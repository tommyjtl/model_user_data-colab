import subprocess, shlex, os, sys, shutil
import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime

AWS_ACCESS_KEY_ID = "AKIA3S3ZMJJYVLPU3U5U"
AWS_SECRET_KEY_ID = "XFP2BfF6I/W7DHxBXLNsUJKg387owdh4zLUXt889"

class aws():
    def __init__(self):
        print("Preparing toolkits...")
        os.chdir("./toolkit")
        log_file = open("out.log", "w+")
        try:
            try:
                from subprocess import DEVNULL
            except ImportError:
                DEVNULL = open(os.devnull, 'wb')

            command = "python setup.py"
            # process = subprocess.Popen(shlex.split(command))
            process = subprocess.Popen(shlex.split(command), stdout=DEVNULL, stderr=DEVNULL)
            while True:
                print(process)
                '''
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                elif output:
                    formatted_output = output.strip().decode("utf-8")

                    now = datetime.now()
                    log_file.write("[ " + str(now.strftime("%d/%m/%Y %H:%M:%S")) + " ] " + str(formatted_output))

                    if formatted_output == '':
                        break
                else: break
                '''
            process.terminate()
            log_file.close()
        except BaseException as e:
            print(str(e))

    def downloadDirectoryFroms3(self, bucketName, remoteDirectoryName):
        s3_resource = boto3.resource('s3', region_name='ap-southeast-1', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY_ID)
        bucket = s3_resource.Bucket(bucketName) 
        for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
            if not os.path.exists(os.path.dirname(obj.key)):
                os.makedirs(os.path.dirname(obj.key))
            try:
                bucket.download_file(obj.key, obj.key) # save to same path
            except BaseException as e:
                if "[Errno 21]" not in str(e):
                    print(e)
                else: pass
        return True

    def get_labeld_dataset(self, s3_source_path, local_path="./"):
        print("Downloading your dataset: \"" + s3_source_path + "\" from AWS S3.")
        self.downloadDirectoryFroms3("cocorobo-training-test", s3_source_path)
        print("Successfully downloaded!")
        # shutil.copytree(src, dest, copy_function = shutil.copy)
        # os.
        # return True

    def generate_config(self, project_name, count):
        pass

    def train(self, iteration=3000):
        pass

    def validate(self):
        pass

    def export(self):
        pass