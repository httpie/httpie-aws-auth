"""
AWS auth plugin for HTTPie.

"""
import os
import sys

from httpie.status import ExitStatus
from httpie.plugins import AuthPlugin
from requests_aws4auth import AWS4Auth


__version__ = '0.0.3'
__author__ = 'Jakub Roztocil'
__licence__ = 'BSD'


# https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-environment
KEY = 'AWS_ACCESS_KEY_ID'
SECRET = 'AWS_SECRET_ACCESS_KEY'


class BytesHeadersFriendlyS3Auth(AWS4Auth):
    def __call__(self, r):
        for k, v in r.headers.items():
            if isinstance(v, bytes):
                # HTTPie passes bytes but S3Auth excepts text, so unless we
                # decode it here, the signature will be incorrect:
                # https://github.com/tax/python-requests-aws/blob/46f2e90ea48e18d8f32c6473fecdf0da4ef04847/awsauth.py#L104
                r.headers[k] = v.decode('utf8')
        return super(BytesHeadersFriendlyS3Auth, self).__call__(r)


class AWSAuthPlugin(AuthPlugin):
    name = 'AWS auth'
    auth_type = 'aws'
    description = 'Obtains AWS credentials from AWS_* environment variables or from `--auth KEY_ID:KEY`'
    auth_require = False
    prompt_password = True

    def get_auth(self, username=None, password=None):
        # There's a differences between None and '': only use the
        # env vars when --auth, -a not specified at all, otherwise
        # the behaviour would be confusing to the user.
        access_key = os.environ.get(KEY) if username is None else username
        secret = os.environ.get(SECRET) if password is None else password
        session_token = os.environ.get('AWS_SESSION_TOKEN', default=None)
        default_region = os.environ.get('AWS_DEFAULT_REGION', default="us-east-1")
        region = os.environ.get('AWS_REGION', default=default_region)
        service = "s3"
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

        return BytesHeadersFriendlyS3Auth(access_key, secret, region, service, session_token=session_token)
