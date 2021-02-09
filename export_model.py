import glob, random, os, time, shutil, sys
import subprocess

# project_name = input("Please enter the name of your project: \n")

# current_directory_path = os.getcwd()
current_directory_path = str(sys.argv[1])

def clear_darflow_label():
	try:
		os.remove("./tools/darkflow-colab/labels.txt")
	except IOError as e:
		print(str(e))
	finally:
		print("Deleteing labels.txt from previous darkflow conversion.")

def copy_raw_to_darkflow():
	try:
		os.system("cp ./conf/" + project_name + ".names ./tools/darkflow-colab/labels.txt")
		print("cp ./conf/" + project_name + ".names ./tools/darkflow-colab/labels.txt")
		os.system("cp ./conf/" + project_name + ".cfg ./tools/darkflow-colab/cfg/" + project_name + ".cfg")
		print("cp ./conf/" + project_name + ".cfg ./tools/darkflow-colab/cfg/" + project_name + ".cfg")
		os.system("cp ./backup/" + project_name + "_last.weights ./tools/darkflow-colab/bin/" + project_name + ".weights")
		print("cp ./backup/" + project_name + "_last.weights ./tools/darkflow-colab/bin/" + project_name + ".weights")
	except IOError as e:
		print(str(e))
	finally:
		print("Done copying files to darkflow directory.")

def run_darkflow_convertion():
	batcmd="bash check_aws.sh"
	result = subprocess.check_output(batcmd, shell=True)
	# print(result.decode('unicode_escape').strip("\n"))
	if result.decode('unicode_escape').strip("\n") == "yes":
		print("this is an aws server, activating tensorflow env...")
		# exec_tensorflow_env = subprocess.check_output("source activate tensorflow_p36", shell=False)
		# print(exec_tensorflow_env.decode('unicode_escape').strip("\n"))
	elif result.decode('unicode_escape').strip("\n") == "no":
		print("this is not an aws server, just go with the flow...")

	os.chdir("./tools/darkflow-colab/")
	try:
		exec_darkflow_command = "./flow --model cfg/" + project_name + ".cfg --load bin/" + project_name + ".weights --savepb"
		print(exec_darkflow_command)
		os.system(exec_darkflow_command)
	except IOError as e:
		print(str(e))
	finally:
		print("Done converted model to tensorflow type.")

	os.chdir(current_directory_path)

def generate_test_images_for_conversion():
	try:
		os.mkdir("./tools/tflite2kmodel-colab/images/" + project_name)
		print("Exporting testing images from training dataset.")
		time.sleep(0.5)
		os.chdir("./data/")
		num_lines = sum(1 for line in open('train.txt'))
		f=open('train.txt')
		lines=f.readlines()
		cont_line = random.sample(range(num_lines), int(num_lines/4))
		for i in range(0,int(num_lines/4),1):
			content = lines[cont_line[i]]
			content = content.strip('\n')
			os.system("cp " + content + " ../tools/tflite2kmodel-colab/images/")
			# print(content)
		f.close()
		os.chdir(current_directory_path)
	except IOError as e:
		print(str(e))

def prepare_ncc_package():
	os.chdir("./tools/tflite2kmodel-colab/")
	try:
		f = open("ncc.zip")
		f.close()
	except IOError:
		print("File not existed, downloading ncc.")
		os.system("wget https://cocoroboai.s3-ap-southeast-1.amazonaws.com/ncc.zip")
		# os.system("wget https://help-x-cn-resource.s3.cn-north-1.amazonaws.com.cn/ncc.zip")
		os.system("unzip ncc.zip")
	finally:
		print("Done getting the ncc.")
		os.chdir(current_directory_path)

def copy_to_tfliteconversion():
	os.chdir(current_directory_path)
	print("Copy files to tflitetokmodel convertion directory...")
	os.system("cp ./tools/darkflow-colab/built_graph/" + project_name + ".meta ./tools/tflite2kmodel-colab/workspace/")
	os.system("cp ./tools/darkflow-colab/built_graph/" + project_name + ".pb ./tools/tflite2kmodel-colab/workspace/")

def exec_final_convertion():
	os.chdir("./tools/tflite2kmodel-colab/")
	os.system("toco --graph_def_file=workspace/"+project_name+".pb --input_format=TENSORFLOW_GRAPHDEF --output_format=TFLITE --output_file=workspace/"+project_name+".tflite --inference_type=FLOAT --input_type=FLOAT --input_arrays=input --output_arrays=output --input_shapes=1,224,224,3")
	# os.system("toco --graph_def_file=workspace/"+project_name+".pb --output_format=TFLITE --output_file=workspace/"+project_name+".tflite --inference_type=FLOAT --input_type=FLOAT --input_arrays=input --output_arrays=output --input_shapes=1,224,224,3")
	os.system("bash tflite2kmodel.sh workspace/"+project_name+".tflite")
	os.chdir(current_directory_path)
	os.system("cp ./tools/tflite2kmodel-colab/workspace/"+ project_name +".kmodel ./convert")

if __name__ == '__main__':
	generate_test_images_for_conversion()
	clear_darflow_label()
	copy_raw_to_darkflow()
	run_darkflow_convertion()
	copy_to_tfliteconversion()
	prepare_ncc_package()
	exec_final_convertion()
