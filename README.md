# Kat - a command-line Kattis assistant

This is a command line program for getting, testing and submitting Kattis attempts!

Credits to Kattis and their own python script for submitting files [(found here)](https://open.kattis.com/help/submit). Our submission script is heavily inspired by theirs.

## Installing:
1. First of all download this repository (either by zip or git) and make sure to extract it to a known location.
2. Install dependencies by running `pip3 install -r requirements.txt` inside the directory.
3. Add the directory to %PATH or `ln -s /path/to/kat/kattis.py /usr/bin/kat` (latter only works on unix systems)
4. To use most functionalities, add your personal configuration to this repository. Go to open.kattis.com > Help > How to submit > Download your personal configuaration file and download the resulting file to this folder.
## Usage:

### Get

```
kattis get <problem-name>
```

This downloads the sample input-output files for the problem and creates a directory for the problem. Inside, the test files are put in the subfolder `test`, and the `boilerplate.py` is copied into the folder as `<problem-name>.py`. Happy hacking!

### Test

```
kattis test <problem-name> [path-to-file]
```

This pipes every `.in`-file into the corresponding script, while recording the output. The output is compared to the corresponding `.ans`-files and supplied to a report, which tells you which tests failed and displaying failed output.

If multiple supported source files are present within the problem directory, you will be prompted to choose one. Alternativly you can supply the path to your chosen script as a second argument

### Submit

```
kattis submit <problem-name> [path-to-file]
```

This submits a given script to kattis for final judgement.
Remember to get your own configuration file from [here](https://open.kattis.com/help/submit).

If multiple supported source files are present within the problem directory, you will be prompted to choose one. Alternativly you can supply the path to your chosen script as a second argument