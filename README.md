NOID-mint Python Package

## Installation
```
Make a new directory on your computer
$ mkdir manuscript_arks
Navigate into that directory
$ cd manuscript_arks
Clone the github repo above into that directory
$ git clone https://github.com/aprigge/NOID-mint
Use pip2 to create a virtual environment
$ pip2 install virtualenv
$ virtualenv venv
Activate the virtual environment
$ source venv/bin/activate
Confirm the python version is 2.7 by running 
$ python --version
Navigate down into the NOID-mint directory
$ cd NOID-mint
Install the requirements
$ pip2 install -r requirements.txt
Setup the noid script
Run $ python setup.py install


```

## Usage
* Generate noid
```



run 'python mss_ark_noid.py' in terminal. you will be prompted for:
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
