import json
import logging
from math import ceil
from typing import Any, Optional

# External Packages
import ollama
from PIL import Image

# Internal Packages
from ..._util import CreatorRole, MessageBlock, TokenUsage
from ..._tool import ToolMetadata

logger = logging.getLogger(__name__)


class OllamaCore:
    """`OllamaCore` is designed to be the base class for any `Core` class aiming to itegrate with LLM through Ollama.
    It offer functionality to pull the desired model from Ollama's server if it's not available locally.

    Attributes:
    * CONN_STRING (str)

    Methods:
    * __available(None) -> bool
    * __try_pull_model(None) -> None
    * calculate_token_count(
            msgs: list[MessageBlock | dict[str, Any]], tools: list[ToolMetadata] | None = None,
            images: list[str] | None = None, image_detail: str | None = None
        ) -> int
    * load_csv(cls, input_path: str) -> None
    * calculate_image_tokens(width: int, height: int) -> int
    """

    csv_path: str | None = None
    ASCII_CONVERSION_FACTOR: float = 4
    NON_ASCII_CONVERSION_FACTOR: float = 1.5

    def __init__(self, connection_string: str, model_name: str):
        self.__connection_string = connection_string
        self.__model_name = model_name
        if not self.__available():
            self.__try_pull_model()

    @property
    def CONN_STRING(self) -> str:
        return self.__connection_string

    def __available(self) -> bool:
        try:
            client = ollama.Client(host=self.CONN_STRING)
            lst = list(client.list())[0]
            _, m, *_ = lst
            for _m in m:
                if _m.model == self.__model_name:
                    logger.debug("Found %s => %s", self.__model_name, _m)
                    return True
            return False
        except ollama.RequestError as ore:
            logger.error(
                "RequestError: %s", str(ore), exc_info=True, stack_info=True
            )
            raise
        except Exception as e:
            logger.error(
                "Exception: %s", str(e), exc_info=True, stack_info=True
            )
            raise

    def __try_pull_model(self):
        """
        Attempt to pull the required model from ollama's server.

        **Raises:**
            ollama.ResponseError: pull model manifest: file does not exist
        """
        try:
            client = ollama.Client(host=self.CONN_STRING)
            _ = client.pull(self.__model_name, stream=False)
        except ollama.RequestError as oreqe:
            logger.error(
                "RequestError: %s", str(oreqe), exc_info=True, stack_info=True
            )
            raise
        except ollama.ResponseError as orespe:
            logger.error(
                "ResponseError: %s",
                str(orespe),
                exc_info=True,
                stack_info=True
            )
            raise
        except Exception as e:
            logger.error(
                "Exception: %s (%s)",
                str(e),
                type(e),
                exc_info=True,
                stack_info=True
            )
            raise

    @staticmethod
    def build_profile(model_name: str) -> dict[str, bool | int | str]:
        """
        Build the profile dict based on information found OllamaCore.csv_path

        These are the models which the developer has experience with.
        If `model_name` is not found in the csv file, default value will be applied.
        """
        profile: dict[str, bool | int | str] = {"name": model_name}
        # If OllamaCore.csv_path is set
        if OllamaCore.csv_path:
            with open(OllamaCore.csv_path, "r", encoding="utf-8") as csv:
                header = csv.readline()
                columns = header.strip().split(",")
                while True:
                    line = csv.readline()
                    if not line:
                        break
                    values = line.strip().split(",")
                    if values[0] == model_name:
                        for column, value in zip(columns[1:], values[1:]):
                            if column == "context_length":
                                profile[column] = int(value)
                            elif column == "max_output_tokens":
                                profile[column] = 2048 if value == "" else int(
                                    value
                                )
                            elif column == "remarks":
                                profile[column] = value
                            elif value == "TRUE":
                                profile[column] = True
                            else:
                                profile[column] = False
                        break
        # If OllamaCore.csv_path is not set or some fields are missing
        # Assign default values
        if "context_length" not in profile:
            # Most supported context length
            profile["context_length"] = 2048
        if "tool" not in profile:
            # Assume supported
            profile["tool"] = True
        if "text_generation" not in profile:
            # Assume supported
            profile["text_generation"] = True

        return profile

    @classmethod
    def load_csv(cls, input_path: str):
        COLUMNS_STRING = "name,context_length,max_output_tokens,text_generation,tool,text_input,image_input,audio_input,text_output,image_output,audio_output,remarks"
        EXPECTED_COLUMNS = set(COLUMNS_STRING.split(","))
        # Begin validation
        with open(input_path, "r", encoding="utf-8") as csv:
            header = csv.readline()
            header = header.strip()
            columns = header.split(",")
            # Expect no columns is missing
            diff = EXPECTED_COLUMNS.difference(set(columns))
            if diff:
                raise ValueError(
                    f"Missing columns in {input_path}: {', '.join(diff)}"
                )
            # Expect all columns are in exact order
            if header != COLUMNS_STRING:
                raise ValueError(
                    f"Invalid header in {input_path}: \n{header}\n{COLUMNS_STRING}"
                )

            for line in csv:
                values = line.strip().split(",")
                name: str = values[0]
                for column, value in zip(columns, values):
                    if column in ["name", "remarks"]:
                        assert isinstance(
                            value, str
                        ), f"{name}.{column} must be a string."
                    elif column in [
                        "context_length", "max_output_tokens"
                    ] and value:
                        try:
                            _ = int(value)
                        except ValueError:
                            logger.warning(
                                f"{name}.{column} must be an integer."
                            )
                            raise
                    elif value:
                        assert value.lower() in [
                            "true",
                            "false",
                        ], f"{name}.{column} must be a boolean."
        # End validation
        OllamaCore.csv_path = input_path

    def calculate_token_count(
        self,
        msgs: list[MessageBlock | dict[str, Any]],
        tools: list[ToolMetadata] | None = None,
        images: list[str] | None = None,
    ) -> int:
        """Calculate the token count for the given messages and tools.
        Efficient but not accurate. Child classes should implement a more accurate version.

        Args:
            msgs (list[MessageBlock | dict]): A list of messages.
            tools (list[ToolMetadata] | None, optional): A list of tools. Defaults to None.
            images (list[str] | None): A list of images. Defaults to None.

        Returns:
            int: The token count. Number of characters divided by `CONVERSION_FACTOR` + token count for images

        Notes:
        * Remove whitespaces
        * If contain non-ascii character, conversion_factor = 1.5, else conversion_factor = 4
        """
        character_count: int = 0
        has_non_ascii = False
        for msg in msgs:
            # Incase the dict does not comply with the MessageBlock format
            # "images" tag is not processed in this loop
            if "content" in msg and msg["content"]:
                cleaned_content = msg["content"].replace("\n", "")
                cleaned_content = cleaned_content.replace(" ", "")
                character_count += len(cleaned_content)
                if has_non_ascii is False:
                    try:
                        cleaned_content.encode("ascii")
                    except UnicodeEncodeError:
                        has_non_ascii = True
            if "role" in msg and msg["role"] == CreatorRole.TOOL.value:
                if "name" in msg:
                    character_count += len(msg["name"])

        if tools:
            for tool in tools:
                character_count += len(json.dumps(tool))

        if has_non_ascii:
            conversion_factor = OllamaCore.NON_ASCII_CONVERSION_FACTOR
        else:
            conversion_factor = OllamaCore.ASCII_CONVERSION_FACTOR

        text_token_count = ceil(character_count / conversion_factor)
        image_token_count = 0
        if images:
            for image_path in images:
                with Image.open(image_path) as img:
                    width, height = img.size
                    image_token_count += self.calculate_image_tokens(
                        width, height
                    )

        logger.debug(
            "Token Estimation:\nText: %d\nImage: %d",
            text_token_count,
            image_token_count,
        )
        return text_token_count + image_token_count

    @staticmethod
    def calculate_image_tokens(width: int, height: int) -> int:
        """
        Calculate the token needed to process the image.

        Temporary adopt OpenAI's calculation.

        **Args:**
            width (int): Width of the image.
            height (int): Height of the image.

        **Returns:**
            int: The token needed to process the image.

        **Notes:**
        * Different models handle image differently, and there are no official docs on this.
        * https://platform.openai.com/docs/guides/vision/calculating-costs
        * TODO: Caching.
        """
        if width == 512 and height == 512:
            return 85

        tiles_width = ceil(width / 512)
        tiles_height = ceil(height / 512)
        total_tokens = 85 + 170 * (tiles_width * tiles_height)
        return total_tokens

    @staticmethod
    def update_usage(
        response: dict[str, Any],
        token_usage: TokenUsage | None = None
    ) -> TokenUsage:
        """Transforms CompletionUsage to TokenUsage. This is a adapter function."""
        if token_usage is None:
            token_usage = TokenUsage(input_tokens=0, output_tokens=0)

        input_tokens: Optional[int] = response.get("prompt_eval_count", None)
        output_tokens: Optional[int] = response.get("eval_count", None)
        if input_tokens is None and output_tokens is None:
            raise RuntimeError("Both input_tokens and output_tokens are None.")

        token_usage.input_tokens += input_tokens    # type: ignore
        token_usage.output_tokens += output_tokens    # type: ignore
        logger.debug("Token Usage: %s", token_usage)
        return token_usage


TOOL_PROMPT = """
Utilize tools to solve the problems. 
Results from tools will be kept in the context. 
Calling the tools repeatedly is highly discouraged.
"""
