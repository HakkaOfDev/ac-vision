import yaml


class ConfigLoader:

    def __init__(self) -> None:
        self.loadConfigs()

    def loadConfigs(self):
        with open("components/tools/config/config.yml", "r") as file:
            self.config = yaml.safe_load(file)


config = ConfigLoader().config
