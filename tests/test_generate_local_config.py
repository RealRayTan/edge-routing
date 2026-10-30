import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from scripts.generate_local_config import generate


class GenerateLocalConfigTests(unittest.TestCase):
    def test_generates_valid_flclash_config(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / 'ip.txt').write_text('104.16.39.201:443#CF-MEDIA\n')
            work_dir = temp_path / '.work'
            work_dir.mkdir()
            (work_dir / 'node-profile.json').write_text(json.dumps({
                'type': 'vless',
                'uuid': 'test-uuid-1234',
                'server_port': 443,
                'tls': {'enabled': True, 'server_name': 'test.pages.dev'},
                'transport': {'type': 'ws', 'path': '/', 'headers': {'Host': 'test.pages.dev'}}
            }))
            clients_dir = temp_path / 'clients'
            clients_dir.mkdir()
            (clients_dir / 'clash.yaml').write_text('rule-providers:\n  dummy: test\nrules:\n  - DIRECT\n')

            with patch('scripts.generate_local_config.ROOT', temp_path):
                generate()

            out_file = clients_dir / 'flclash.local.yaml'
            self.assertTrue(out_file.exists())
            content = out_file.read_text()
            self.assertIn('104.16.39.201', content)
            self.assertIn('test-uuid-1234', content)
            self.assertIn('test.pages.dev', content)
            self.assertIn('rule-providers:', content)
            self.assertIn('rules:', content)
