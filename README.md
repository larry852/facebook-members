# facebook-members
Get members of group facebook


## Requirements

### Chrome driver
```sh
./install/install_chromedriver
```

## Run
```sh
git clone https://github.com/larry852/facebook-members
cd facebook-members
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
python main.py -u USERNAME -p PASSWORD -g ID_GROUP
```