import configparser


class Settings:
    def __init__(self, config_file_path: str = "config.ini"):
        self._configparser_ = configparser.ConfigParser()
        self._config_file_name_path_ = config_file_path
        self._parsed_config_ = self._configparser_.read(self._config_file_name_path_)
        self._config_ = {}
        for v in self._configparser_["USER"]:
            self._config_[v] = self._configparser_["USER"][v]
        
    def update_value(self, key, value):
        # self.config[key] = value # TODO: Add this
        pass
    
    def get_value(self, value, fallback_value):
        return self._config_.get(value, fallback_value)
        
        
if __name__ == "__main__":
    settings = Settings()
    print(settings.get_value("2", "4"))
