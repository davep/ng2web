###############################################################################
# Common make values.
library   := ng2web
run       := pipenv run
python    := $(run) python
lint      := $(run) pylint
pyreverse := $(run) pyreverse
mypy      := $(run) mypy
coverage  := $(run) coverage
test      := $(coverage) run -m unittest discover -v -t $(shell pwd)
twine     := $(run) twine

###############################################################################
# Get the OS so we can make some decisions about other things.
UNAME := $(shell uname)

###############################################################################
# Set up the command to open a file; normally for viewing.
ifeq ($(UNAME),Darwin)
open_file := open
endif
ifeq ($(UNAME),Linux)
open_file := xdg-open
endif

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Install all dependencies
	pipenv sync --dev

.PHONY: resetup
resetup:			# Recreate the virtual environment from scratch
	rm -rf $(shell pipenv --venv)
	pipenv sync --dev

.PHONY: depsoutdated
depsoutdated:			# Show a list of outdated dependencies
	pipenv update --outdated

.PHONY: depsupdate
depsupdate:			# Update all dependencies
	pipenv update --dev

.PHONY: depsshow
depsshow:			# Show the dependency graph
	pipenv graph

##############################################################################
# Checking/testing/linting/etc.
.PHONY: lint
lint:				# Run Pylint over the library
	$(lint) $(library) tests

.PHONY: test
test:				# Run unit tests
	$(test) tests

.PHONY: coverage
coverage:			# Show the current code coverage
	@$(coverage) report | awk '/^TOTAL/ { print "Coverage: " $$4 }'

.PHONY: coveragehtml		# Create a HTML report of the current code coverage
coveragehtml:
	$(coverage) html

.PHONY: coveragerep
coveragerep: coveragehtml       # Create and view a report of the current code coverage
	$(open_file) .coverage_report/index.html

.PHONY: coveragetxt
coveragetxt:			# Show a test-based code coverage report
	$(coverage) report

.PHONY: typecheck
typecheck:			# Perform static type checks with mypy
	$(mypy) --scripts-are-modules $(library) tests $(wildcard bin/[a-z]*)

.PHONY: stricttypecheck
stricttypecheck:	        # Perform a strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(library) tests $(wildcard bin/[a-z]*)

.PHONY: checkall
checkall: dscheck lint stricttypecheck test coverage # Check all the things

##############################################################################
# Documentation.
.PHONY: docs
docs:				# Generate the system documentation
	cd docs; rm -rf source; rm -rf build; mkdir source build
	cd docs/source; $(run) sphinx-apidoc -F -f -e -M -H $(library) -o . ../../$(library) ../../setup.py
	cp docs/template/* docs/source
	cd docs; $(run) make html

.PHONY: rtfm
rtfm: docs			# Locally read the library documentation
	$(open_file) docs/build/html/index.html

##############################################################################
# Package/publish.
.PHONY: package
package:			# Package the library
	$(python) setup.py bdist_wheel

.PHONY: spackage
spackage:			# Create a source package for the library
	$(python) setup.py sdist

.PHONY: packagecheck
packagecheck: package		# Check the packaging.
	$(twine) check dist/*

.PHONY: testdist
testdist: packagecheck		# Perform a test distribution
	$(twine) upload --skip-existing --repository testpypi dist/*

.PHONY: dist
dist: packagecheck		# Upload to pypi
	$(twine) upload --skip-existing dist/*

##############################################################################
# Utility.
.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: clean
clean:				# Clean the build directories
	rm -rf build dist $(library).egg-info

.PHONY: help
help:				# Display this help
	@grep -Eh "^[a-z]+:.+# " $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.+# "}; {printf "%-20s %s\n", $$1, $$2}'

##############################################################################
# Housekeeping tasks.
.PHONY: housekeeping
housekeeping:			# Perform some git housekeeping
	git fsck
	git gc --aggressive
	git remote update --prune

### Makefile ends here
