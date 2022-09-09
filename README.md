NOID-mint Python Package

## Installation
```
1. Make a new directory on your computer
	$ mkdir manuscript_arks
	
2. Navigate into that directory
	$ cd manuscript_arks
	
3. Clone the github repo above into that directory
	$ git clone https://github.com/UCLALibrary/SLDP_ARK_mint

4. Navigate into the new SDLP_ARK_mint directory
	$ cd SLDP_ARK_mint
	
5. Create a virtual environment
	$ python3 -m venv ENV

6. Activate the virtual environment
	$ source ENV/bin/activate

7. Confirm the python version is 3.x by running 
	$ python --version

8. Install the requirements
	$ pip install -r requirements.txt

9. Setup the noid script
	Run $ python setup.py install
```

## Usage
* Generate noid
```
run 'python sinai_work_page_ark.py' in terminal. you will be prompted for:
1. The directory name for the files, including the works.csv file
2. The ARK shoulder
3. EZID login credientials

the parent ark input and new item ark will be added to the existing columns.
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
