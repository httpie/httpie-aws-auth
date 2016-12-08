"""
AWS auth plugin for HTTPie.

"""
import os
import sys

from httpie import ExitStatus
from httpie.plugins import AuthPlugin
from httpie.compat import bytes
from awsauth import S3Auth


__version__ = '0.0.1'
__author__ = 'Jakub Roztocil'
__licence__ = 'BSD'


# https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-environment
KEY = 'AWS_ACCESS_KEY_ID'
SECRET = 'AWS_SECRET_ACCESS_KEY'


class BytesHeadersFriendlyS3Auth(S3Auth):
    def __call__(self, r):
        for k, v in r.headers.items():
            if isinstance(v, bytes):
                # HTTPie passes bytes but S3Auth excepts text, so unless we
                # decode it here, the signature will be incorrect:
                # https://github.com/tax/python-requests-aws/blob/46f2e90ea48e18d8f32c6473fecdf0da4ef04847/awsauth.py#L104
                r.headers[k] = v.decode('utf8')
        return super().__call__(r)


class AWSAuthPlugin(AuthPlugin):
    name = 'AWS auth'
    auth_type = 'aws'
    description = ''
    auth_require = False
    prompt_password = True

    def get_auth(self, username=None, password=None):
        # There's a differences between None and '': only use the
        # env vars when --auth, -a not specified at all, otherwise
        # the behaviour would be confusing to the user.
        access_key = os.environ.get(KEY) if username is None else username
        secret = os.environ.get(SECRET) if password is None else password
        if not access_key or not secret:
            missing = []
            if not access_key:
                missing.append(KEY)
            if not secret:
                missing.append(SECRET)
            sys.stderr.write(
                'httpie-aws-auth error: missing {1}\n'
                .format(self.name, ' and '.join(missing))
            )
            sys.exit(ExitStatus.PLUGIN_ERROR)

        return BytesHeadersFriendlyS3Auth(access_key, secret)
