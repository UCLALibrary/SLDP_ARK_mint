NOID-mint Python Package

## Installation
```
create directory at command line

cd to that directory

setup virtual environment for Python 2.7: 

activate the environment: 

git clone https://github.com/aprigge/NOID-mint.git

in command line change directory to new folder: 'cd NOID-mint'

in command line 'python setup.py install'

in command line install requirements 'pip install -r requirements.txt'

```

## Usage
* Generate noid
```



run 'python scriptname' in terminal. you will be prompted for:
1. The directory name for the files
2. EZID login credientials
3. The ARK shoulder

the parent ark input and new item ark will be appended to the last two columns of the output csv file
```

## Testing
```
nosetests
```

## The NOID-Mint was forked from the following authors
* Virginia Tech Libraries - Digital Libraries Development developers
	* [Yinlin Chen](https://github.com/yinlinchen)
	* [Tingting Jiang](https://github.com/tingtingjh)
	* [Lee Hunter](https://github.com/whunter)

See also the list of [contributors](https://github.com/VTUL/NOID-mint/graphs/contributors) who participated in this project.

## Thanks
This tool was heavily influenced from [pynoid](https://github.com/no-reply/pynoid)
