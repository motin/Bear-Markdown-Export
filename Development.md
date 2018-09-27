## Development

### Run tests

Danger! The tests will operate on the current user's Bear notes.
It is adviced to create a new system user and run the tests from there.

    python -m pytest
    
For debugging:

    python -m pytest -vv -s --basetemp tmp
