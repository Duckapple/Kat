# Kat - a command-line Kattis assistant

This is a command-line program for getting, testing, and submitting Kattis problem attempts!

Credit goes to Kattis and their python script for submitting files [found here](https://open.kattis.com/help/submit). Our submission script is heavily inspired by theirs.

Logo provided by [@CptF1nn](https://github.com/CptF1nn)

## Installing

### Mac & Linux

To easily download and link the program, use the following command:

```sh
curl -sSLf https://raw.githubusercontent.com/Duckapple/Kat/master/install.sh | sh
```

(or alternatively, open the file and execute the individual statements inside)

## Usage

To get a list of commands and usage, use `kattis --help` and `kattis [command] --help` once installed.

### Get

```txt
kattis get problem [problem ...]
```

This downloads the sample input-output files for the problem and creates a directory for the problem. Inside, the test files are put in the subfolder `test`, and an initial script file is waiting for your solution. To specify your language of choice for a single problem, use the command `-l LANGUAGE`. Happy hacking!

### Test/watch

```txt
kattis test/watch problem [file]
```

`test` pipes every `.in`-file into the corresponding script, while recording the output. The output is compared to the corresponding `.ans`-files and supplied to a report, which tells you which tests failed and displaying failed output.

If multiple supported source files are present within the problem directory, you are prompted to choose one. Alternatively, you can supply the path to your chosen script as a second argument

If you use `watch` instead of `test`, then a file watcher is used on the primary script file, making the tests run when you save the file.

### Submit

```txt
kattis submit problem [file]
```

This submits a given script to kattis for final judgement.
Remember to get your configuration file from [here](https://open.kattis.com/help/submit).

If multiple supported source files are present within the problem directory, you are prompted to choose one. Alternatively, you can supply the path to your chosen script as a second argument.

### Archive/Unarchive

```
kattis archive/unarchive problem [problem ...]
```

Move a problem (or several) between a `./.archive` folder and the current folder. 

### List

```
kattis list [-p PAGE] [-l LIMIT] [-c] [sorting/filter [sorting/filter ...]]
```

List problems from the Kattis instance.

`--compact` shows only the names of the problems.

Possible sortings:
 - Leaving it out sorts problems alphabetically by display name
 - `easiest` sorts easiest problem first, by points
 - `hardest` sorts hardest problem first

If you add several filters, then they are used in a union style (`unsolved solved` would allow every problem again)

Possible filters:
 - `unsolved` allows any problem not solved, same as `tried untried`
 - `solved` allows any solved problem
 - `tried` allows problems tried before
 - `untried` allows problem never even tried before

### Contest

```
kattis contest [-c CONTEST_URL] get [-s] [-o] [-l LANGUAGE]
```

Get all problems from a contest, optionally submitting already completed problems.

You can provide only the ID of a contest if you have the hostname in the config, otherwise the whole URL should be provided.

### Read

```
kattis read [-c] problem [problem ...]
```

Read the problem descriptions in your browser.

`--console` prints the description in the console, but test cases and embedded LaTeX takes up a lot of space, making it hard to use.

### Work

```
kattis work [-h] [-oafs] [sorting/filter [sorting/filter ...]]
```

This command initiates a loop where you can run commands by just typing their command, and where problems are automatically opened according to filters and sorting for the `list` command. You can specify arguments for `submit` and `get` to this command, which will be applied when running them in the loop.

## Boilerplates

If you add a script file for your favourite language to the `boilerplate` folder, it is copied into every new problem you initialize with the `get` command. That way, you can quickly get started on solving problems. 

## Configuration

Once you have used almost any command once, configurations have appeared in your `.kattisrc`.
The great part about them is that they are very extensible, allowing you to register additional languages and the like.

### User

You probably wouldn't want to change the username or token fields manually, but here you can. These fields are the primary reason for getting the `.kattisrc` from the Kattis instance.

### Kattis

This section contains information about which kattis instance you are currenctly using. If you want to change the hostname, you should either remove the other options (relying on known fallback-routes shared among Kattis instances) or replace the hostname in each.

### Kat

The primary config options for the Kat tool, and the ones you would like to change the most often.

`language` designates the language used for creating the initial script file in the `get` command.

`openfilecommand` (WIP) designates a way to open a file after `get` or `unarchive`, letting you work just a bit faster on problems.

`workcommand` specifies which arguments you would want to call the `work` command with, since there are an awful lot of arguments possible.

### File associations

Here, you can associate a file type with a specific language. This is used as the sole source of truth when determining language, so make sure it works with your Kattis instance before editing this config.

### Initialize commands

These commands are used to initialize problem folders for languages which cannot use only script files.
If you use a build system you would like to use for a language in Kattis, then here is where that command goes.

### Run commands

These commands tell Kat how to run and test your submission attempt.
Without a command for your language, the `test` and `run` commands do not work.

There are some indicators which are replaced when running the command:
 - `@f` is replaced with the file name
 - `@c` is replaced with the problem name

### Compile commands

These commands tell Kat that script files should be compiled before being run.

See the section on Run commands above for info on indicators.

For C++ support it is required that a C++ compiler exists in PATH and is specified under `[Compile commands]` in your `.kattisrc`.
By default the compiler used is `g++`.

### Naming

Some languages, like Java, enforce a naming convention for their files.
If any other language enforces capital first letter, then add it here.

Currently, only PascalCase is supported, create an issue or edit the `namingSchemeConverters` in `helpers/fileUtils.py` to add more cases.
