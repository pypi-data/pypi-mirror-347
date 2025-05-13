import httpx
import pydantic
import typing
import typing_extensions


class File(typing_extensions.TypedDict):
    """
    File
    """

    file: typing_extensions.Required[httpx._types.FileTypes]


class _SerializerFile(pydantic.BaseModel):
    """
    Serializer for File handling case conversions
    and file omissions as dictated by the API
    """

    model_config = pydantic.ConfigDict(
        populate_by_name=True,
    )

    file: typing.Optional[typing.Any] = pydantic.Field(
        alias="file", default=None, exclude=True
    )

    @staticmethod
    def get_files_from_typed_dict(
        item: File,
    ) -> typing.List[typing.Tuple[str, httpx._types.FileTypes]]:
        files: typing.List[typing.Tuple[str, httpx._types.FileTypes]] = []

        file = item.get("file", None)
        if isinstance(file, list):
            files.extend([("file", f) for f in file])
        elif file is not None:
            files.append(("file", file))

        return files
