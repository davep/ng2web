###############################################################################
# Common make values.
app      := ng2web
run      := pipenv run
python   := $(run) python
lint     := $(run) pylint
coverage := $(run) coverage
test     := $(coverage) run -m unittest discover -v -t $(shell pwd)
mypy     := $(run) mypy
twine    := $(run) twine
build    := $(python) -m build
black    := $(run) black
mkdocs   := $(run) mkdocs

##############################################################################
# Run the app.
.PHONY: run
run:
	$(python) -m $(app)

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Install all dependencies
	pipenv sync --dev
	$(run) pre-commit install

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
	$(lint) $(app)

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
	$(mypy) --scripts-are-modules $(app)

.PHONY: stricttypecheck
stricttypecheck:	        # Perform a strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(app)

.PHONY: checkall
checkall: lint stricttypecheck test # Check all the things

##############################################################################
# Documentation.
.PHONY: docs
docs:				# Generate the system documentation
	echo GNDN for now

.PHONY: rtfm
rtfm:				# Locally read the library documentation
	$(mkdocs) serve

##############################################################################
# Package/publish.
.PHONY: package
package:			# Package the library
	$(build) -w

.PHONY: spackage
spackage:			# Create a source package for the library
	$(build) -s

.PHONY: packagecheck
packagecheck: package spackage		# Check the packaging.
	$(twine) check dist/*

.PHONY: testdist
testdist: packagecheck		# Perform a test distribution
	$(twine) upload --skip-existing --repository testpypi dist/*

.PHONY: dist
dist: packagecheck		# Upload to pypi
	$(twine) upload --skip-existing dist/*

##############################################################################
# Utility.
.PHONY: ugly
ugly:				# Reformat the code with black.
	$(black) $(app) tests

.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: clean
clean:				# Clean the build directories
	rm -rf build dist $(app).egg-info

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
