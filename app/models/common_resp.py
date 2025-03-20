from typing import Union
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse, Response


class CommonResp(BaseModel):
    code: int
    message: str
    data: list | dict | str | None


def resp_200(*, data: Union[list, dict, str, None] = None) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CommonResp(code=200, message="success", data=data).model_dump(),
    )


def resp_400(*, data: str = None, message: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=CommonResp(code=400, message=message, data=data).model_dump(),
    )


def resp_500(*, data: str = None, message: str = "INTERNAL SERVER ERROR") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=CommonResp(code=500, message=message, data=data).model_dump(),
    )


def resp(
    *,
    code: int = 200,
    data: Union[list, dict, str, None] = None,
    message: str = "success",
) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CommonResp(code=code, message=message, data=data).model_dump(),
    )
