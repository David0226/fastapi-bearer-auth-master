#from jose import JWTError, jwt
import jwt
import request
from fastapi import APIRouter

CLIENT_ID = '23cd2d50b8d338ef9bd0d8a542218c7436755e47'

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def test(request: Request):

    try:
        print(request.headers.get('Authorization'))
        payload = request.headers.get('Authorization').replace('Bearer ', '')
        print(payload)
    except:
        return {"error": "no token"}

    authd = jwt.decode(payload,
                       algorithms=['HS256'],
                       options={
                           "verify_signature": False,
                           "verify_aud": False
                       })
    print(authd)
    for key, value in authd.items():
        print(key, value)

    if authd['cid'] != CLIENT_ID:
        return {'error': 'invalid client id'}

    return {"Hello": "World"}
