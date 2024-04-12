#open CMD
#open folder where your main.py is located
#run uvicorn main:app --reload
Last login: Thu Feb 29 14:02:04 on ttys000
(base) madhuriawachar@Madhuris-Air-7 ~ % activate fastapi

EnvironmentNameNotFound: Could not find conda environment: fastapi
You can list all discoverable environments with `conda info --envs`.


(base) madhuriawachar@Madhuris-Air-7 ~ % conda info --envs
# conda environments:
#
                         /Users/madhuriawachar/micromamba/envs/tf
base                  *  /Users/madhuriawachar/miniconda3
tensorflow               /Users/madhuriawachar/miniconda3/envs/tensorflow

(base) madhuriawachar@Madhuris-Air-7 ~ % conda info --envs
# conda environments:
#
                         /Users/madhuriawachar/micromamba/envs/tf
base                  *  /Users/madhuriawachar/miniconda3
fastapi_env              /Users/madhuriawachar/miniconda3/envs/fastapi_env
tensorflow               /Users/madhuriawachar/miniconda3/envs/tensorflow

(base) madhuriawachar@Madhuris-Air-7 ~ % ls
Applications
Desktop
Documents
Downloads
Figure_1.png
Figure_14.png
Kmeans_iris data.png
Library
Licence microsoft.pdf
Licence.pdf
ML
Movies
MtechThesis
Music
Pictures
Public
ReadMe.pdf
bias_var_reg.png
dataset_snake_vs_monkey
es654-spring2023-assignment2-madhuri_akbar
github-classroom
metrics.py
micromamba
miniconda3
ml assignment
nltk_data
norm_deg for 4.png
teach-ds-course-website
tree
try4.py
venv
withcls4.png
(base) madhuriawachar@Madhuris-Air-7 ~ % cd Documents
(base) madhuriawachar@Madhuris-Air-7 Documents % ls
-Differential-Privacy-to-Matrix-Factorization
2008.01916.pdf
M
Machine_Learning_Madhuri
Madhuri_Awachar(22210023) (1).pdf
Madhuri_Awachar(22210023).pdf
Mid sem - Madhuri (1).docx
Mid sem - Madhuri (2).docx
Mid sem - Madhuri copy.docx
Mid sem - Madhuri.docx
Mid sem - Madhuri.pdf
NLP-Natural-language-Processing-
New Folder With Items
New Folder With Items 2
Private reccomadation system
SS
Text-to-Image Generation and Text-and-Shape Guided 3D Human Avatar Generation
WhatsApp Image 2023-03-19 at 3.03.59 AM.jpeg
Zoom
assignment-4-akbar_madhuri-main
assignment-4-akbar_madhuri-main.zip
assignment1
assignment2
assignment5-sai-krishna-madhuri
assignment5_madhuri
cpp_practice
es654-spring2023-assignment2-madhuri_akbar
fastapi
federated learning
python
thirdai
(base) madhuriawachar@Madhuris-Air-7 Documents % cd fastapi
(base) madhuriawachar@Madhuris-Air-7 fastapi % uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/madhuriawachar/Documents/fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [38836] using StatReload
INFO:     Started server process [38840]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:62165 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:62178 - "GET /welcome HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:62206 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:62206 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:62215 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:62217 - "GET /Welcome?name=Madhuri HTTP/1.1" 200 OK
INFO:     127.0.0.1:62219 - "GET /Welcome?name=Madhuri HTTP/1.1" 200 OK



#dataset
https://www.kaggle.com/code/shubhamlipare/credit-card-fraud-detection-supervised-ml


implementation:
https://github.com/shivam1808/Credit-Card-Fraud-Detection/blob/master/Anamoly%20Detection.ipynb