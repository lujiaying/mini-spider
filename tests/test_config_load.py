import os

from tools import config_load

class TestConfigLoader():
    temp_conf_file = "./temp.conf"

    def setUp(self):
        with open(TestConfigLoader.temp_conf_file, 'w') as fwrite:
            fwrite.write('[spider]\n')
            fwrite.write('url_list_file: ./urls\n')
            fwrite.write('crawl_timeout: 2\n')
        self.config_loader = config_load.ConfigLoader()
        assert 0 == self.config_loader.read(TestConfigLoader.temp_conf_file)

    def tearDown(self):
        if os.path.exists(TestConfigLoader.temp_conf_file):
            os.remove(TestConfigLoader.temp_conf_file)

    def test_get(self):
        assert './urls' == self.config_loader.get('spider', 'url_list_file')
        assert '2' == self.config_loader.get('spider', 'crawl_timeout')
