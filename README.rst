The certmonger_comodo_helper is a helper for `certmonger <https://www.freeipa.org/page/Certmonger>`_ that submits and
retrieves certificates from the Comodo API. It is written in python and requires the suds python
library, it should be compatible with both python 3 (using suds-jurko) and 2.

Because of the limitations of setuptools configuration files cannot (well they can, but I don't want to assume) be
placed into the 'proper' directories. For proper installation look at the RPM spec file or just use an
RPM.

For configuration files please reference etc/README.rst


