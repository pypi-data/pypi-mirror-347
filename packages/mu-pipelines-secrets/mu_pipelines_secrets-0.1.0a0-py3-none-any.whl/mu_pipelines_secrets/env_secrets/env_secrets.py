import os
from typing import Any, NotRequired, TypedDict, cast

from mu_pipelines_interfaces.config_types.secrets.secrets_config import (
    SecretsConfigItem,
)
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.modules.secrets_module_interface import (
    SecretsModuleInterface,
)


class AdditionalAttributes(TypedDict):
    variable_name: NotRequired[str]


class EnvSecrets(SecretsModuleInterface):
    variable_name: str

    def __init__(
        self, config: SecretsConfigItem, configuration_provider: ConfigurationProvider
    ):
        super().__init__(config, configuration_provider)
        assert "additional_attributes" in config
        additional_attributes = cast(
            AdditionalAttributes, config["additional_attributes"]
        )

        assert "variable_name" in additional_attributes

        if additional_attributes["variable_name"] is not None:
            self.variable_name = additional_attributes["variable_name"]

    def get(self, context: Any) -> Any:
        secret_value: Any | None = os.environ.get(self.variable_name)
        if secret_value is None:
            raise AssertionError(f"secret not found: {self.variable_name}")
        return secret_value
