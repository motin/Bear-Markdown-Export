# encoding=utf-8
# python3.7

import subprocess

class TestIssue2():

    def test_export_of_only_a_tag_that_does_not_exist(self, datadir):
        result = subprocess.run(['python', 'bear_import.py',
                                 '--wait_before_import', '0',
                                 '--wait_on_no_files_found', '0',
                                 '--base_import_path', datadir,
                                 ], capture_output=True)
        output = result.stdout.decode("utf-8")
        if (result.returncode > 0):
            print("Command failed - stderr: ")
            print(result.stderr.decode("utf-8"))
        assert result.returncode == 0
        assert output.find('2 files imported') > -1
        result = subprocess.run(['python', 'bear_export_sync.py',
                                 '--sync', 'false',
                                 '--base_export_path', datadir,
                                 '--only_export_these_tags', 'a-tag-that-does-not-exist'
                                 ], capture_output=True)
        if (result.returncode > 0):
            print("Command failed - stderr: ")
            print(result.stderr.decode("utf-8"))
        assert result.returncode == 0
        output = result.stdout.decode("utf-8")
        assert output.find('No notes needed exports') == -1
        assert output.find('0 notes exported to') > -1

    def setup_export_of_only_a_tag_that_does_not_exist(self, method):
        base_import_path = self.TEST_FILES_DIR.join("issue-2")
        """ teardown any state that was previously setup with a setup_method
        call.
        """