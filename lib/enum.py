# Java's Enum
# NOTE: adding an Enum type to Python is still an open PEP:
# http://www.python.org/dev/peps/pep-0435/
def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

