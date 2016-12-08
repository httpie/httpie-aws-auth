httpie-aws-auth
===============

AWS / Amazon S3 auth plugin for `HTTPie <https://httpie.org/>`_.


Installation
============

.. code-block:: bash

    $ pip install --upgrade httpie-aws-auth


You should now see ``aws`` under ``--auth-type / -A`` in ``$ http --help`` output.


Usage
=====


Credentials on the CLI
----------------------

The syntax and behavior is the same as with the basic auth.


Specify both access key ID and secret
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    http --auth-type aws -a ACCESSKEYXXX:AWSSECRETKEYXXX http://bucket.s3.amazonaws.com/test


Specify only the key
~~~~~~~~~~~~~~~~~~~~

There'll be a password prompt:

.. code-block:: bash

    $ http -A aws -a ACCESSKEYXXX http://bucket.s3.amazonaws.com/test
    http: password for ACCESSKEYXXX@bucket.s3.amazonaws.com: <enter aws secret key>


Auth via the ``AWS_*`` environment variables
--------------------------------------------

The names are identical to what
`AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-environment>`_
and other tools use, so you might be already good to go.


.. code-block:: bash

    export AWS_ACCESS_KEY_ID=ACCESSKEYXXX
    export AWS_SECRET_ACCESS_KEY=AWSSECRETKEYXXX

    http -A aws http://bucket.s3.amazonaws.com/test


Implementation
--------------

This plugin uses https://github.com/tax/python-requests-aws
