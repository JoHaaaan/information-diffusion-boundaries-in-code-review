import unittest
import hashlib
import os

class TestGeneratedFiles(unittest.TestCase):
    RESULT_HASHES = {
        'microsoft.csv.bz2': '042fcda73f34c175983074e7888723d09801f394af740de3df0d7e55bd74836e',
        'microsoft.pickle.bz2': '62f0bc6da6afcf546317d13c588a68971ac78b2fe788a13b12df8a198050007a',
    }

    def test_generated_files(self):
        for filename, expected_hash in self.RESULT_HASHES.items():
            # Make sure the file exists before trying to open it
            if os.path.exists(f'./data/minimal_paths/{filename}'):
                with open(f'./data/minimal_paths/{filename}', 'rb') as file:
                    bytes = file.read()
                    readable_hash = hashlib.sha256(bytes).hexdigest()
                    self.assertEqual(readable_hash, expected_hash, f'Hash mismatch for {filename}')
            else:
                print(f"File {filename} does not exist")

if __name__ == '__main__':
    unittest.main()