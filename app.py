from flask import Flask
import sys
from github import Github, UnknownObjectException
import os
from collections import OrderedDict
from yaml import load, dump, Loader
import json, yaml

userrepo = None
user = None
delim = "/"
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg[-1] == delim:
    	arg = arg[:-1]
    user, userrepo = arg.split(delim)[-2:]    
else:
    print ("Error: Repo path not provided!")


g = Github()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Dockerized Flask App!!"

@app.route("/v1/<file_name>")
def fetch_file(file_name):
	try:		
		repo = g.get_repo(delim.join((user,userrepo)))
		filename, file_extension = os.path.splitext(file_name)
		if file_extension == ".json":
			file_name = file_name.replace("json", "yml")	
			repo_file = repo.get_file_contents(file_name)
			result = json.dumps(yaml.load(repo_file.decoded_content))		
			return result		
		else:
			repo_file = repo.get_file_contents(file_name)		
			return repo_file.decoded_content		
	except  UnknownObjectException:
		return "Error: Page not found!\n"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
