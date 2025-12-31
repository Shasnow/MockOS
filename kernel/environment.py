import dataclasses
import os

@dataclasses.dataclass
class MockOSEnv:
    OS_NAME: str = "MockOS"
    OS_VERSION: str = "1.0"
    ARCH: str = "amd64"
    HOSTNAME: str = "localhost"
    BASE_PATH: str = "mockos/"
    CWD: str = "/root"
    USR_NAME: str = "root"
    USR_HOME: str = "/root"
    PATH: list = dataclasses.field(default_factory=lambda: ["/bin", "/usr/bin"])
    PERMISSION: int = 0

    @property
    def prompt(self):
        return f"{self.USR_NAME}@{self.HOSTNAME}:{self.CWD.replace(self.USR_HOME, '~')}{'#' if self.PERMISSION == 0 else '$'} "

    def store(self):
        env = {}
        for field in dataclasses.fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)
            env[f"MOCKOS_{field_name}"] = str(field_value)
        return env

    @staticmethod
    def restore():
        env = MockOSEnv()
        for field in dataclasses.fields(env):
            field_name = field.name
            field_value = os.getenv(f"MOCKOS_{field_name}", field.default)
            if field.type == int:
                field_value = int(field_value)
            setattr(env, field_name, field_value)
        return env
        
