import configparser

from settings import Settings


class Config:
    def __init__(self, config_file_path: str = "config.ini"):
        self._config_file_path_ = config_file_path
        self._configparser_ = configparser.ConfigParser()
        self._config_files_ = self._configparser_.read(self._config_file_path_)

    def update(self, setting: Settings, value) -> None:
        self._configparser_["USER"][setting.value] = str(value)
        with open(self._config_file_path_, "w") as config_file:
            self._configparser_.write(config_file)

    def get(self, setting: Settings, fallback_value=None):
        return self._configparser_["USER"].get(setting.value, fallback_value)

    def restore_default_config(self):
        self._configparser_["USER"].clear()
        with open(self._config_file_path_, "w") as config_file:
            self._configparser_.write(config_file)


if __name__ == "__main__":
    config = Config()

    print(config.get(Settings.MUSIC_VOLUME))

    config.update(Settings.MUSIC_VOLUME, "20")

    print(config.get(Settings.MUSIC_VOLUME))

    config.restore_default_config()

    print(config.get(Settings.MUSIC_VOLUME))

    config.update(Settings.MUTE_GAME_ON_FOCUS_LOSS, True)
    config.update(Settings.MUSIC_VOLUME, 50)
    config.update(Settings.SFX_VOLUME, 20)
    config.update(Settings.DECREASE_VOLUME_DURING_GAME_PAUSE, False)
    config.update(Settings.GAME_PAUSE_NORMAL_VOLUME_PERCENTAGE, 70)
