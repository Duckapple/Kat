# Kat - a command-line Kattis assistant

This is a command line program for getting, testing and submitting Kattis attempts!

Credits to Kattis and their own python script for submitting files [(found here)](https://open.kattis.com/help/submit). In a future update, this will be downloaded from Kattis on runtime instead of included here, in order to not infringe any potential rights.

## Usage:

### Get

```
kattis get <problem-name>
```

This downloads the sample input-output files for the problem and creates a directory for the problem. Inside, the test files are put in the subfolder `test`, and the `boilerplate.py` is copied into the folder as `<problem-name>.py`. Happy hacking!

### Test

```
kattis test <problem-name>
```

This pipes every `.in`-file into the corresponding script, while recording the output. The output is compared to the corresponding `.ans`-files and supplied to a report, which tells you which tests failed and displaying failed output.

### Submit

```
kattis submit <problem-name>
```

This uses the Kattis submit.py script to submit your work. Remember to get your own configuration file from [here](https://open.kattis.com/help/submit).