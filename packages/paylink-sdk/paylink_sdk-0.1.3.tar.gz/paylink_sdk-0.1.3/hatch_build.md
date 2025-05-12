##  Prepare the Package for Release
hatch build

## Upload the Package to PyPI
twine upload dist/*
