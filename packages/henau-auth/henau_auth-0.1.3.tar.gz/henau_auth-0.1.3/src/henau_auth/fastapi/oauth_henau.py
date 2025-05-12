from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .jwt import verify_token, create_access_token
from starlette.responses import JSONResponse
import random


class HenauAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        login_router: str = "/login",
        excluded_routes: list[str] = None,
        get_user_func: callable = None,
        oauth2_user_func: callable = None,
        expires_delta: int = 3600,
        jwt_secret: str = "".join(
            [
                random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )
                for i in range(32)
            ]
        ),
        *args,
        **keywords,
    ) -> None:
        """_summary_

        Args:
            app (_type_): ASGI APP 应用对象
            login_router (str, optional): 登录路由. Defaults to "/login".
            excluded_routes (list[str], optional): 排除的路由. Defaults to None.
            get_user_func (callable, optional): 获取用户方法，不传将默认使用payload. Defaults to None.
            oauth2_user_func (callable, optional): 用户授权方法，接受code 返回用户信息载体. Defaults to None.
            expires_delta (int, optional): 令牌过期时间. Defaults to 3600.
            jwt_secret (str, optional): 令牌秘钥. Defaults to "".join( [ random.choice( "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" ) for i in range(32) ] ).
        """
        super().__init__(app, *args, **keywords)
        self.login_router = login_router
        self.excluded_routes = excluded_routes if excluded_routes else []
        self.get_user_func = get_user_func
        self.oauth2_user_func = oauth2_user_func
        self.jwt_secret = jwt_secret
        self.expires_delta = expires_delta

    async def auth(self , request: Request):
        if request.url.path == self.login_router:
            code = request.query_params.get("code")
            try:
                payload = self.oauth2_user_func(code)
            except Exception as e:
                return JSONResponse(status_code=401, content={"message": str(e)})
            request.state.payload = payload
            request.state.user = (
                self.get_user_func(payload) if self.get_user_func else payload
            )
            request.state.token = create_access_token(
                payload, expires_delta=self.expires_delta, jwt_secret=self.jwt_secret
            )
        else:
            if request.url.path not in self.excluded_routes:
                if request.headers.get("Authorization") is None:
                    return JSONResponse(status_code=401, content={"message": "未提供令牌"})
                else:
                    token = request.headers.get("Authorization").split(" ")[1]
                    try:
                        payload = verify_token(token, jwt_secret=self.jwt_secret)
                    except Exception as e:
                        return JSONResponse(
                            status_code=401, content={"message": "令牌错误"}
                        )
                    request.state.payload = payload
                    request.state.user = (
                        self.get_user_func(payload) if self.get_user_func else payload
                    )
    
    async def dispatch(self, request: Request, call_next):
        await self.auth(request)
        
        return await call_next(request)
