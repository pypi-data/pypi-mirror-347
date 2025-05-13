import ast
import inspect
from collections.abc import Callable, Generator
from functools import partial
from typing import (
    Annotated,
    Generic,
    ParamSpec,
    TypeGuard,
    TypeVar,
    cast,
    get_args,
    get_origin,
)

from devtools import debug
from fastapi import APIRouter, Depends, FastAPI, Query, params

from fastapi_exts.decorators import CBV, AsyncLogRecord, LogRecord


app = FastAPI()


cbv = CBV(app.router)


def lalal():
    from fastapi import HTTPException

    raise HTTPException(400)


@cbv
class A:
    v: str | None = Query()
    bb: str | None
    dd: str | None = Query()
    ee: str | None

    @cbv.responses(400)
    @cbv.get("/a")
    @AsyncLogRecord(
        success_handlers=[lambda x: print(x)],
        failure_handlers=[lambda x: print(x)],
        is_class_member=True,
    )
    async def a(self, a: int) -> str:
        return ""

    # @cbv.router.get("/b")
    # @classmethod
    # def b(cls, a: int) -> str: ...

    # @cbv.log_record()
    @cbv.responses(400)
    @cbv.get("/c")
    @staticmethod
    @LogRecord(
        success_handlers=[lambda x: print(x)],
        failure_handlers=[lambda x: print(x)],
    )
    def c(a: int, b=Depends(lalal)) -> str:
        return ""

    @property
    def d(self) -> str: ...

    @cbv.get("/lala/{bb}")
    def e(self): ...
