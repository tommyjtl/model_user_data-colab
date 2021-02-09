import json, os, subprocess, shutil, time, sys

# Declare some paths:
labeling_project_name = str(sys.argv[1]) # "traffic-signs-labeling"
export_folder_name = str(sys.argv[2]) #"../processed-dataset/"
source_folder_name = "../"+labeling_project_name+"/"
# labeling_project_name = str(sys.argv[1])
# export_folder_name = str(sys.argv[2])
# source_folder_name = str(sys.argv[3])

# Remove previous files 
try:
	list_files = subprocess.run(["rm", "-r", export_folder_name], stdout=None)
except BaseException as e:
	pass

if "processed-dataset" in os.listdir("./"): pass
else:  os.mkdir(export_folder_name) # create a processed dataset folder

# Get object names from `data.json` 
lables_file_location = source_folder_name + labeling_project_name + "/annotation-tool/data.json"
read_labels_file_open = open(lables_file_location, "r")
read_labels_file = read_labels_file_open.readlines()

for each in range(0,len(read_labels_file)): 
	read_labels_file[each] = json.loads(read_labels_file[each])

read_labels = read_labels_file[0]["labels"]
export_labels = [None] * len(read_labels)

for i in range(0,len(read_labels)):
	export_labels[i] = read_labels[i]["label"] + "\n"

export_labels[len(read_labels)-1] = export_labels[len(read_labels)-1].strip("\n")
print("Exporting names file: " + str(export_labels))
time.sleep(1)

# Create `.names` file in the processed dataset folder
export_labels_file = open(export_folder_name + labeling_project_name + ".names", "w") 
export_labels_file.writelines(export_labels) 

read_labels_file_open.close()
export_labels_file.close() 

# Read annotation file for each images into a list
annotation_file_location = source_folder_name + labeling_project_name + "/manifests/output/output.manifest"
read_all_annotation = open(annotation_file_location, 'r').readlines()

# Convert str to json
for each in range(0,len(read_all_annotation)): 
	read_all_annotation[each] = json.loads(read_all_annotation[each])

# Read corresponding image from annotaion
# See how to calculate the yolo txt: https://github.com/AlexeyAB/Yolo_mark/issues/60
for each in range(0, len(read_all_annotation)):
	write_txt_file = open(export_folder_name + read_all_annotation[each]["source-ref"].split("/")[-1].split(".")[0] + '.txt', 'w') 

	txt_file_list = [None] * len(read_all_annotation[each][labeling_project_name]["annotations"])
	for i in range(0, len(read_all_annotation[each][labeling_project_name]["annotations"])):
		x = round(read_all_annotation[each][labeling_project_name]["annotations"][i]["left"] / read_all_annotation[each][labeling_project_name]["image_size"][0]["height"], 6)
		y = round(read_all_annotation[each][labeling_project_name]["annotations"][i]["top"] / read_all_annotation[each][labeling_project_name]["image_size"][0]["height"], 6)
		height = round(read_all_annotation[each][labeling_project_name]["annotations"][i]["height"] / read_all_annotation[each][labeling_project_name]["image_size"][0]["height"], 6)
		width = round(read_all_annotation[each][labeling_project_name]["annotations"][i]["width"] / read_all_annotation[each][labeling_project_name]["image_size"][0]["width"], 6)
		txt_file_list[i] = str(read_all_annotation[each][labeling_project_name]["annotations"][i]["class_id"]) + " " + str(x) + " " + str(y) + " " + str(height) + " " + str(width)
	for i in range(0, len(txt_file_list)):
		if i != len(txt_file_list) - 1:
			txt_file_list[i] = txt_file_list[i] + "\n"
	
	write_txt_file.writelines(txt_file_list) 
	write_txt_file.close()

	print(read_all_annotation[each]["source-ref"].split("/")[-1].split(".")[0] + " generated:", txt_file_list)

# Copy image files to the target folder
for file in os.listdir(source_folder_name):
	if "jpg" in file:
		shutil.copy(source_folder_name + file, export_folder_name)

# Compare jpg and txt to see if there are missing txt for its corresponding image
for file in os.listdir(export_folder_name):
	if "jpg" in file:
		if os.path.exists(export_folder_name + file.split(".")[0] + ".txt") == False:
			print(export_folder_name + file.split(".")[0] + ".txt does not existed.")
