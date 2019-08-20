# 2019-08-21
### 0. Generalized datasets, models module.
#### 0.1. Created google dirve json files
`google_drive_datasets.json`, `and google_drive_models.json` added.
Adding new datasets or model in this list will be able to download and load easily.

#### 0.2. Changed method. no jsonfiles.

### 1. Fully automatic monitoring of models, datasets upload in google drive.
#### 1.1. google drive monitoring spreadsheet.

below codes edits `datasets_list.csv` file by list up all files in 
datasets folder in google drive, by monitoring with spreadsheet scripts in
every 1min interval.

```javascript
function listDir() {
  var folderName = 'datasets';
  var folder = DriveApp.getFoldersByName(folderName).next();
  var files = folder.getFiles();
  var sheet = SpreadsheetApp.getActiveSheet();
  sheet.clear()
  
  var file;
  var name;
  var fileName;
  var fileId;
  
  sheet.appendRow(['name', 'filename', 'id']);
  while(files.hasNext()){
    file = files.next();
    fileName = file.getName();
    name = fileName.split('.')[0]
    fileId = file.getId();
    sheet.appendRow([name, fileName, fileId]);
  }
  
  
  var purrsongFolder = DriveApp.getFoldersByName('purrsong').next();
  var csvFile = convertRangeToCsvFile_(fileName, sheet);
  var csvFileName = folderName+'_list.csv';
  var csvFiles = purrsongFolder.getFilesByName(csvFileName);
  if(csvFiles.hasNext()){
      csvFiles.next().setContent(csvFile);
  }

};

function convertRangeToCsvFile_(csvFileName, sheet) {
  // get available data range in the spreadsheet
  var activeRange = sheet.getDataRange();
  try {
    var data = activeRange.getValues();
    var csvFile = undefined;

    // loop through the data in the range and build a string with the csv data
    if (data.length > 1) {
      var csv = "";
      for (var row = 0; row < data.length; row++) {
        for (var col = 0; col < data[row].length; col++) {
          if (data[row][col].toString().indexOf(",") != -1) {
            data[row][col] = "\"" + data[row][col] + "\"";
          }
        }

        // join each row's columns
        // add a carriage return to end of each row, except for the last one
        if (row < data.length-1) {
          csv += data[row].join(",") + "\r\n";
        }
        else {
          csv += data[row];
        }
      }
      csvFile = csv;
    }
    return csvFile;
  }
  catch(err) {
    Logger.log(err);
    Browser.msgBox(err);
  }
}
```

#### 1.2. Usage
1. Add `*.tar.gz` dataset to google drive `purrsong/datasets` folder
2. Add `*.h5` model to google drive `purrsong/models` folder
3. wait few minutes since list is updated every 1min
4. check available datasets or models by
```python
import purrsong as ps
ps.list_datasets()
ps.list_models()
```
5. load datasets, or models
```python
import purrsong as ps
data = ps.load_dataset('cat')
bbs = ps.load_model('bbs')
```


# 2019-08-19
### 0. Created functions for datasets or modelsets
#### 0.1. `datasets`, `modelsets`, `utils` folder added
```
PURRSONG
├── purrsong
    ├── datasets                # NEW 
        ├── __init__.py.py      # NEW 
        └── cats.py             # NEW 
    ├── modelsets               # NEW 
        ├── __init__.py         # NEW 
        ├── bbs.py              # NEW 
        └── lmks.py             # NEW 
    ├── utils                   # NEW 
        ├── __init__.py         # NEW 
        ├── downloader.py       # NEW 
        └── extractor.py        # NEW 
    ├── __init__.py
    └── api.py                  # NEW, this is imported in __init__.py
├── ...
└── test.py                     # NEW, all test is perfomred here
```
> `cats.py` is responsible for downloading and extracting `cats.tar.gz` from google drive
> `bbs.py` is responsible for downloading `bbs.h5` from google drive 
> `lmks.py` is responsible for downloading `lmks.h5` from google drive 

__Using `api.py` I made it simpler to access above files directory__ 
```python
# Example
import purrsong as ps
data = ps.load_cats()
bbs = ps.load_bbs()
lmks = ps.load_lmks()

# Result
print(data)
>>> C:\Users\Jay\.purrsong\datasets\cats.tar
print(bbs)
>>> C:\Users\Jay\.purrsong\modelsets\bbs.h5
print(lmks)
>>> C:\Users\Jay\.purrsong\modelsets\lmks.h5
```

### 1. Version upgraded to 0.1.0 since new functions added

1. added `datasets`, `modelsets`, `utils`, `api.py`.
2. change `purrsong.__init__.py` version (__version__ = '0.1.0')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.1.0-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`

### 2. git create branch test
```git
git branch test
git checkout test
git commit
git push
```

### 3. working with git branch
#### 3.1. 
```git
git branch develop
git checkout develop
git commit
git push
```

# 2019-08-18
### 0. Add cat.zip downloder
#### 0.1. desired output
Expected behavior with below codes
```python
from purrsong.datasets import cats
cats.load_data()
```
> Download cats.zip(2GB) if not exists in `~/.purrsong/datasets/cats.zip
> Load datasets after download or with existing dataset

#### 0.2. what to do
1. add `datasets` folder
2. add `__init__.py`, `cats.py`, `downloader.py` under `datasets` folder
```
purrsong
├── ...
└── purrsong
    ├── __init__.py
    └── datasets
        ├── __init__.py
        ├── downloader.py
        └── cats.py
```
3. code `downloader.py`
```python 
import requests

def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/a/korea.ac.kr/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    directory = os.path.join(os.path.expanduser('~'), '.purrsong','datasets')
    os.makedirs(directory, exist_ok=True)

    CHUNK_SIZE = 1024*1024

    with open(os.path.join(directory, destination), "wb") as f:
        for MB, chunk in enumerate(response.iter_content(CHUNK_SIZE), start=1):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                print(f'{MB:} MB Downloaded,', end='\r')
```

4. code `cats.py`
```python
import os
from downloader import download_file_from_google_drive

def load_data():
    file_id = '1n9AzQxoXQx8fGdew_7tuuFRTopmRzGas'
    download_file_from_google_drive(file_id,'cats.zip')
```

#### 0.3. updated package
General procedure, when update
1. change `purrsong` module
2. change `purrsong.__init__.py` version (__version__ = '0.0.4')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.4-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`


#### 0.4. Error detected, failed to `import downloader`
How to fix
change 
```python 
from downloader import download_file_from_google_drive
```
```python 
from purrsong.downloader import download_file_from_google_drive
```

1. change `cats.py`
2. change `purrsong.__init__.py` version (__version__ = '0.0.5')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.5-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`

#### 0.5 Error detected, failed to `import downloader`
How to fix
change 
```python 
from purrsong.downloader import download_file_from_google_drive
```
```python 
from purrsong.datasets.downloader import download_file_from_google_drive
```

1. change `cats.py`
2. change `purrsong.__init__.py` version (__version__ = '0.0.6')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.6-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`

#### 0.6 Error detected, failed to `import os`
How to fix
`import os` in `downloader.py`?

1. change `downloader.py`
2. change `purrsong.__init__.py` version (__version__ = '0.0.7')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.7-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`


# 2019-08-17
### 0. Create this repo with
* LICENSE : GNU v3
* .gitignore : python
* README.md : for description of this repo

### 1. Create new environment with anaconda
anaconda version `4.7.10`
```
conda create -n purrsong python=3.6
conda activate purrsong
```

### 2. Install libraries for development ###
```
pip install tensorflow
pip install opencv-python
```

### 3. Install libraries for PyPI upload ###
[Instructions(Korean)](https://medium.com/@onlytojay/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B0%B0%ED%8F%AC-%ED%8C%A8%ED%82%A4%EC%A7%80-%EB%A7%8C%EB%93%A4%EA%B8%B0-%EC%A4%91%EA%B0%84%EA%B2%80%ED%86%A0-a2dade70c247)
```
pip install setuptools # Requirement already satisfied (--> conda env default provided)
pip install wheel # Requirement already satisfied (--> conda env default provided)
pip install twine
```

### 4. Clone this repo, add setup.py, setup.cfg
#### 4.1. cloned this repo
```
git clone https://github.com/jeakwon/purrsong.git
```

#### 4.2. added `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name                = 'purrsong',
    version             = '0.0.1',
    description         = 'purrsong',
    author              = 'jeakwon',
    author_email        = 'onlytojay@gmail.com',
    url                 = 'https://github.com/jeakwon/ccpy',
    packages            = find_packages(exclude = []),
    keywords            = ['purrsong'],
    python_requires     = '>=3.6',
    license             = 'LICENSE.txt',
    install_requires    =  [],
)
```

#### 4.3. added `setup.cfg`
```
[metadata]
description-file = README.md
```

#### 4.4. current folder structure
```
purrsong
├── .gitignore
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py
```

#### 4.5. git commit, push

### 5. Create empty PyPI package
#### 5.1. created `.whl` file
In the prompt, with `(purrsong)` env activated in `purrsong` directory, 
```
python setup.py bdist_wheel
```

#### 5.2. uploaded `.whl` file
Uploaded wheel with `twine` module
```
twine upload dist\purrsong-0.0.1-py3-none-any.whl
```
For your information, twine requires PyPI id/pw. register PyPI first.

#### 5.3. check upload
```
pip install purrsong
```

### 6. Add purrsong module
#### 6.1. added `purrsong` folder with `__init__.py`
```
purrsong
├── purrsong            # add folder
    └── __init__.py     # add __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── setup.cfg
└── setup.py
```

#### 6.2. updated package
General procedure, when update
1. change `purrsong` module
2. change `setup.py` version (ex: 0.0.1->0.0.2)
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.2-py3-none-any.whl`
5. git push

#### 6.3. upgraded existing purrsong
```
pip install --upgrade purrsong
```

after sucessful upgrade, activate python kernel
```python
import purrsong
```
No error -> success

### 7. display for PyPI package 
added below code for PyPI display
```python
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # ...
    long_description                = long_description,
    long_description_content_type   = 'text/markdown'
)
```

### 8. Version control change
#### 8.1. adding __version__ in `purrsong/__init__.py`
__`__init__.py`__
```python
__version__ = 0.03
```

#### 8.2. change `setup.py` version from manual to automatic
__`setup.py`__
```python
import purrsong # add this line
setup(
    version = purrsong.__version__, # add this line
)
```

#### 8.3. updated package
General procedure, when update
1. change `purrsong` module
2. change `purrsong.__init__.py` version (__version__ = '0.0.3')
3. `python setup.py bdist_wheel` (creates new .whl)
4. `twine upload dist\purrsong-0.0.3-py3-none-any.whl`
5. git push
6. `pip install --upgrade purrsong`

#### 8.4. check update
```python
import purrsong
purrsong.__version__
>>> '0.0.3'
```