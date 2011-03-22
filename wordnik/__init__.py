import wordnik

## populate exceptions
RestfulError        = wordnik.RestfulError
InvalidRelationType = wordnik.InvalidRelationType
NoAPIKey            = wordnik.NoAPIKey
MissingParameters   = wordnik.MissingParameters

## populate globals
DEFAULT_URL    = wordnik.DEFAULT_URL
DEFAULT_FORMAT = wordnik.DEFAULT_FORMAT

Wordnik = wordnik.Wordnik
Wordnik._populate_methods()
