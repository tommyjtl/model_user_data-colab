import glob, random, os, time, sys

conf_directory_name = "conf"

# dataset_file_path = "/home/ec2-user/SageMaker/"
dataset_file_path = "../sagemaker-labeling/"

# project_path = input("Please enter the name of your project inside Google Drive: \n") 
# classes_count = input("Please enter the number of classes you would like to train: \n")

project_path = str(sys.argv[1])
classes_count = str(sys.argv[2])

# project_name = input("Please enter the name of your project: \n")
project_name = project_path
current_directory_path = os.getcwd()

# shenzhen_trash_classification_sign_dataset

def generate_cfg():
	print("\n1. Total classes is " + classes_count + ", " + project_name + ".cfg generated to conf directory")
	f = open(conf_directory_name+ "/" + project_name + ".cfg", "w")
	cfg_content = ["[net]\n", "batch=64\n", "subdivisions=8\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n", "\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches = 500200\n", "policy=steps\n", "steps=400000,450000\n", "scales=.1,.1\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[maxpool]\n", "size=2\n", "stride=2\n", "\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n", "\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "# filters=(classes + 5)*5\n", "filters="+str(int((float(classes_count)+5)*5))+"\n", "activation=linear\n", "\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes="+str(int(float(classes_count)))+"\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n", "\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n", "\n", "absolute=1\n", "thresh = .6\n", "random=1\n"]
	# ["[net]\n", "Training\n", "batch=64\n", "subdivisions=16\n", "width=224\n", "height=224\n", "channels=3\n", "momentum=0.9\n", "decay=0.0005\n", "angle=0\n", "saturation = 1.5\n", "exposure = 1.5\n", "hue=.1\n\n", "learning_rate=0.001\n", "burn_in=1000\n", "max_batches=" + str(int(float(classes_count))*2000) +"\n", "policy=steps\n", "steps=" + str(int(float(classes_count))*0.8) + "," + str(int(float(classes_count))*0.9) + "\n", "scales=.1,.1\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=16\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=32\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=64\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=128\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=256\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[maxpool]\n", "size=2\n", "stride=2\n\n", "[convolutional]\n", "batch_normalize=1\n", "filters=512\n", "size=3\n", "stride=1\n", "pad=1\n", "activation=leaky\n\n", "[convolutional]\n", "size=1\n", "stride=1\n", "pad=1\n", "filters=" + str((int(float(classes_count)) + 5) * 5) + "\n", "activation=linear\n\n", "[region]\n", "anchors = 0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828\n", "bias_match=1\n", "classes=" + str(int(float(classes_count))) + "\n", "coords=4\n", "num=5\n", "softmax=1\n", "jitter=.2\n", "rescore=0\n\n", "object_scale=5\n", "noobject_scale=1\n", "class_scale=1\n", "coord_scale=1\n\n", "absolute=1\n", "thresh = .6\n", "random=1"]
	f.writelines(cfg_content)
	f.close()

def generate_data():
	print("2. " + project_name + ".data generated to conf directory\n")
	f = open(conf_directory_name+ "/" + project_name + ".data", "w")
	data_content = [
		"classes="+ str(int(float(classes_count))) +"\n",
		"train  = " + current_directory_path + "/data/train.txt\n",
		"valid  = " + current_directory_path + "/data/test.txt\n",
		"names = " + current_directory_path + "/conf/" + project_name + ".names\n",
		"backup = " + current_directory_path + "/backup\n"
	]
	f.writelines(data_content)
	f.close()

def generate_names():
	os.chdir(dataset_file_path + project_path)
	names_file_name = ""
	for names_file in glob.glob("*.names"):
		names_file_name = names_file
		# print(names_file_name)
	f = open(names_file_name,"r+")
	read_original_names = f.readlines()
	print(read_original_names)
	f.close()
	os.chdir(current_directory_path)
	f2 = open(conf_directory_name+ "/" + project_name + ".names", "w")
	f2.writelines(read_original_names)
	f.close()

def generate_training_bash():
	f = open(conf_directory_name+ "/" +  "start-train.sh", "w")
	bash_content = ["../tools/darknet-colab/darknet detector train "+ project_name +".data "+project_name+".cfg darknet19_448.conv.23\n"]
	f.writelines(bash_content)
	f.close()

def generate_testing_bash():
	os.chdir("./data/")
	num_lines = sum(1 for line in open('train.txt'))
	f=open('train.txt')
	lines=f.readlines()
	cont_line = random.sample(range(num_lines), 1)
	for i in range(0,1,1):
		content = lines[cont_line[i]]
		content = content.strip('\n')
		print(content)
		os.system("cp " + content + " ../test/" + project_name + "_test.jpg")
		# print(content)
	f.close()
	# ../tools/darknet-colab/darknet detector test trash.data trash.cfg ../../trash_weights_backup/trash_last.weights ../test/plastic_18.jpg
	f = open("../conf/test-train.sh", "w")
	bash_content = [
	"cd "+current_directory_path+"/tools/darknet-colab\n",
	"./darknet detector test ../../" + conf_directory_name + "/" + project_name + ".data ../../" + conf_directory_name + "/" + project_name+".cfg ../../backup/" + project_name + "_last.weights ../../test/" + project_name + "_test.jpg\n",
	"cd "+current_directory_path+"\n"
	]
	f.writelines(bash_content)
	f.close()
	os.chdir(current_directory_path)

def generate_subprocess_check_py():
	f = open(conf_directory_name+ "/train.py", "w")
	train_check_content = [
		"import subprocess, shlex, os, signal\n",
		"\n",
		"def run_command(command):\n",
		"	process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)\n",
		"	print(\"Process PID is: \" + str(process.pid))\n",
		"	while True:\n",
		"		output = process.stdout.readline()\n",
		"		if output == '' and process.poll() is not None:\n",
		"			break\n",
		"		if output:\n",
		"			formatted_output = output.strip().decode(\"utf-8\")\n",
		"			if (\"avg loss\" in formatted_output) and (\"rate\" in formatted_output):\n",
		"				print(formatted_output)\n",
		"				iteration_times = int(formatted_output.split()[0][:-1])\n",
		"				avg_loss = float(formatted_output.split()[2])\n",
		"				# print(str(int(iteration_times)) + \",\" + str(float(formatted_output.split()[2])))\n",
		"				if avg_loss < 0.06: break\n",
		"	# process.terminate()\n",
		"	process.terminate()\n",
		"	try:\n",
		"		process.wait(timeout=0.2)\n",
		"		print('== subprocess exited with rc =', process.returncode)\n",
		"	except subprocess.TimeoutExpired:\n",
		"		print('subprocess did not terminate in time')\n",
		"	os.kill(int(process.pid)+1, signal.SIGKILL)\n",
		"\n",
		"try:\n",
		"	run_command(\"bash start-train.sh\")\n",
		"except KeyboardInterrupt:\n",
		"	print(\"Keyboard Interrupted.\")\n",
		"\n",
		"print(\"\"\"\n",
		"  ____                   _ \n",
		" |  _ \\  ___  _ __   ___| |\n",
		" | | | |/ _ \\| '_ \\ / _ \\ |\n",
		" | |_| | (_) | | | |  __/_|\n",
		" |____/ \\___/|_| |_|\\___(_)\n",
		"	\"\"\")\n"
	]
	f.writelines(train_check_content)
	f.close()

if __name__ == '__main__':
	# shenzhen_trash_classification_sign_dataset
	os.system("cp -a "+ dataset_file_path +project_path + "/. data/")
	generate_cfg()
	generate_data()
	generate_names()
	generate_training_bash()
	os.chdir("./data/")
	exec(open("generate_train-test.py").read())
	os.chdir(current_directory_path)
	generate_testing_bash()
	generate_subprocess_check_py()
