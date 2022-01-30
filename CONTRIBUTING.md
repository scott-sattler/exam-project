# pre-commit
* Contributing to this repo requires usage of pre-commit hooks to automatically lint and autoformat code before commiting changes
* pre-commit hook configuration is defined at the top-level of this repo within .pre-commit-config.yaml
## Setup
* Install dev-requirements.txt from the root directory of this repo
  * `pip install -r dev-requirements.txt`
  * (alternatively, just pip install pre-commit)
    * `pip install pre-commit`
* Install the pre-commit hooks defined in .pre-commit-config.yaml from the root directory of this repo
  * `pre-commit install`
* From here on, this project's pre-commit hooks will be ran on each commit
## Usage
* To run the pre-commit hooks manually
  * `pre-commit run`
## Exclusions
* If you want Black to ignore a particular section of code, you can add the comments below before and after a block of code
  * `# fmt: off`
  * `# fmt: on`
* If you must bypass the pre-commit hooks, use `-n` on your commit
  * `git commit -n ...`