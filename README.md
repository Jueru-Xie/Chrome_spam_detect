# Spam manager chrome extension

This spam management tool is built to manage and reply to spams and other emails in bulk. It has 2 main functions: bulk reply and auto labeling.

## Installation

#### Frontend install
1. Go to extension setting in Chrome
2. Click on Load Unpacked, and choose the frontend folder
#### backend install
3. Go to backend and Install python Flask 

   ```bash
   pip install Flask
   ```
4. Run flask server

   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   flask run
   ```

## Usage

Open the extension by clicking on extension icon (The icon will only appear when you are in a Gmail tab).

### Reply in bulk
To reply in bulk, choose a label to reply to, and choose to use an existing template or manually input the title and body. 

To manully input the title and body(recommended), write the title and body in the cooresponding field, switch the "choose a template type" to be "Manual inputs".

To use a template, create a json file following the format in the example reply.json, input the name of the json file in the extension popup, and switch the "choose a template type" to be "Json template".

Click "Execute"

### Auto labeling 
To use the auto labeling function, input the desired name for the new label, input a keyword for the email wanted to be put in the label, and input the begin and end range for the search.

Click "Execute"


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
