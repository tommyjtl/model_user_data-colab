import subprocess, shlex, os, sys, shutil, signal
import logging
import boto3
from botocore.exceptions import ClientError
import os
from datetime import datetime
from subprocess import Popen, PIPE

AWS_ACCESS_KEY_ID = "AKIA3S3ZMJJYVLPU3U5U"
AWS_SECRET_KEY_ID = "XFP2BfF6I/W7DHxBXLNsUJKg387owdh4zLUXt889"

class aws():
    def __init__(self):
        print("Preparing toolkits...")
        os.chdir("./toolkit")

        try:
            print("(Step 1 of 3) Getting all the tools we need... (Darknet, Darkflow, Conversion tool)")
            command = "git submodule update --init"
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
            while process.stdout.readline().strip().decode("utf-8") != '':
                # print(process.stdout.readline().strip().decode("utf-8"))
                pass
            process.terminate()
            try:
                process.wait(timeout=0.2)
                print('(Step 1 of 3) Done fetching all the tools.' + str(process.returncode))
            except subprocess.TimeoutExpired:
                print('subprocess did not terminate in time')

            print("(Step 2 of 3) Building darknet...")
            command = "make"
            os.chdir("./tools/darknet-colab/")
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
            # print("Process PID is: " + str(process.pid))
            while process.stdout.readline().strip().decode("utf-8") != '':
                pass
            process.terminate()
            try:
                process.wait(timeout=0.2)
                print('(Step 2 of 3) Done building darknet.', process.returncode)
            except subprocess.TimeoutExpired:
                print('subprocess did not terminate in time')
            os.chdir("../../")

            print("(Step 3 of 3) Building darkflow...")
            command = "python3 setup.py build_ext --inplace"
            os.chdir("./tools/darkflow-colab/")
            # print(shlex.split(command))
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
            # print("Process PID is: " + str(process.pid))
            while process.stdout.readline().strip().decode("utf-8") != '':
                pass
            process.terminate()
            try:
                process.wait(timeout=0.2)
                print('(Step 3 of 3) Done building darkflow...', process.returncode)
            except subprocess.TimeoutExpired:
                print('subprocess did not terminate in time')
            
            os.chdir("../../../")
            print("Done!")

        except KeyboardInterrupt:
            print("Keyboard Interrupted.")


    def log_writter(self, log, file_path):
        now = datetime.now()
        log_formatter = str("[" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "]\t" + str(log) + "\n")

        print(log_formatter)
        log_file = open(file_path, "a")
        log_file.write(log_formatter)
        log_file.close()


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

    def get_labeld_dataset(self, s3_bucket, s3_source_path, local_path="./"):
        print("Downloading your dataset: \"" + s3_source_path + "\" from AWS S3.")
        self.downloadDirectoryFroms3(s3_bucket, s3_source_path)
        print("Successfully downloaded!")

    def proccess_annotation(self, labeling_project_name, export_folder_name):
        os.chdir("./toolkit")
        command = "python process_annotation.py " + str(labeling_project_name) + " " + str(export_folder_name)
        # print(command)
        # python process_annotation.py "traffic-signs-labeling" "./processed-dataset/" "../sagemaker-labeling/sagemaker-labeled-dataset/"
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

        while process.stdout.readline().strip().decode("utf-8") != '':
            # print(process.stdout.readline().strip().decode("utf-8"))
            pass
        process.terminate()

        try:
            process.wait(timeout=0.2)
            # print('== subprocess exited with rc =' + str(process.returncode))
            print("Annotated dataset processed!")
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')

        os.chdir("../")

    def generate_config(self, project_path, project_name, total_objects):
        os.chdir("./toolkit")

        # print("python generate_conf.py " + str(project_path) + " " + str(project_name) + " " + str(total_objects))
        command = "python generate_conf.py " + str(project_path) + "/ " + str(project_name) + " " + str(total_objects)
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)

        while process.stdout.readline().strip().decode("utf-8") != '':
            pass
        process.terminate()
        try:
            process.wait(timeout=0.2)
            print('Configuration generated!' + str(process.returncode))
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')

        os.chdir("../")

    def run_train_command(self, command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        print("Process PID is: " + str(process.pid))
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                formatted_output = output.strip().decode("utf-8")
                if ("avg loss" in formatted_output) and ("rate" in formatted_output):
                    print(formatted_output)
                    iteration_times = int(formatted_output.split()[0][:-1])
                    avg_loss = float(formatted_output.split()[2])
                    # print(str(int(iteration_times)) + "," + str(float(formatted_output.split()[2])))
                    if avg_loss < 0.06: break
        # process.terminate()
        process.terminate()
        try:
            process.wait(timeout=0.2)
            print('== subprocess exited with rc =', process.returncode)
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')
        os.kill(int(process.pid)+1, signal.SIGKILL)

    def train(self):
        os.chdir("./toolkit/conf/")
        self.run_train_command("bash start-train.sh")
        os.chdir("../../")

    def validate(self):
        pass

    def export(self):
        pass