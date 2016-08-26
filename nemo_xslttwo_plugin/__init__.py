from subprocess import Popen, PIPE
import tempfile
from lxml import etree
import logging


class XSLError(Exception):
    pass


def shell(cmd, stdin=None):
    """ Execute the external command and get its exitcode, stdout and stderr.
    """

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


class SaxonShellTransform(object):

    def __init__(self, saxon, xslt, cache=None, logger=None):
        """ XSLT2 Transformer for Nemo using a shell command line and temporary file

        :param saxon: Path to SaxonHE.jar file
        :type saxon: str
        :param xslt: Path to the XSLT to use
        :type xslt: str
        :param cache: Cache Handler
        :type cache: capitains_nautilus.cache.BaseCache
        :param logger: Logging Handler
        :type logger: logging.Logger

        :ivar saxon: Path to SaxonHE.jar file
        :type saxon: str
        :ivar xslt: Path to the XSLT to use
        :type xslt: str
        :ivar cache: Cache Handler
        :type cache: capitains_nautilus.cache.BaseCache or werkzeug.contrib.cache.BaseCache
        :ivar logger: Logging Handler
        :type logger: logging.Logger

        """
        self.__saxon__ = saxon
        self.__xslt__ = xslt
        self.__cache__ = cache
        if logger:
            self.__logger__ = logger
        else:
            self.__logger__ = logging.getLogger(__name__)

    @property
    def cache(self):
        return self.__cache__

    @property
    def xslt(self):
        return self.__xslt__

    @property
    def saxon(self):
        return self.__saxon__

    @property
    def logger(self):
        return self.__logger__

    def transform(self, _, xmlcontent, urn):
        """ Transform some XML Content using a shell.

        :param _: Unused variable fed by Nemo (Work metadata from Nemo)
        :param xmlcontent: XML Node representing the text
        :param urn: Urn of the passage, used as key for caching
        :return: Transformed Source
        :rtype: str
        """
        if self.cache:
            cached = self.cache.get(urn)
            if cached:
                return cached.decode("utf-8")
        error, output = None, None
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        if len(xmlcontent):
            tmpfile.write(etree.tostring(xmlcontent, encoding="utf-8"))
            tmpfile.flush()
            command = [
                "java", "-jar", self.saxon, "-s:{}".format(tmpfile.name), "-xsl:{}".format(self.xslt), "-expand:off"
            ]
            output, err = shell(command)
            if len(output) == 0:
                error = err
        if error:
            raise XSLError(error)
        else:
            if self.cache:
                self.cache.set(urn, output)
            return output.decode("utf-8")
