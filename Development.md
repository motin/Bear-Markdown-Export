## Development

### Run tests

Danger! The tests will operate on the current user's Bear notes.
It is advised to create a new system user and run the tests from there.

    python -m pytest
    
For debugging (`--basetmp tmp` makes the test data directory clones 
created in a folder named `tmp` in the current folder for easy inspection):

    python -m pytest -vv -s --basetemp tmp

Note: Some tests import notes, and there is no automatic 
clean-up of removing the imported notes after the tests have run.
Thus, you will need to manually remove all recently imported notes
between test-runs (use the `#.imported` tag).
