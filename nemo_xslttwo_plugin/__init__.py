from subprocess import Popen, PIPE
import tempfile
from lxml import etree
import logging
import os


class XSLError(Exception):
    pass


def shell(cmd):
    """ Execute the external command and get its exitcode, stdout and stderr.

    :param cmd: List of command member to send to shell
    :type cmd: [str]
    :return: Output and Error as tuples
    """
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


class SaxonShellTransform(object):
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

    def __init__(self, saxon, xslt, cache=None, logger=None):
        self.__saxon__ = os.path.abspath(saxon)
        self.__xslt__ = os.path.abspath(xslt)
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


class SaxonStreamTransform(SaxonShellTransform):
    """ XSLT2 Transformer for Nemo using a shell command line and streamed content

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
    DELIMINATOR = b"\n--/END_OF_XML/--\n"

    def __init__(self, saxon, xslt, cache=None, logger=None):
        super(SaxonStreamTransform, self).__init__(saxon, xslt, cache, logger)

        # Code Adaption from github.com/Connexions/cnx-mathml2svg
        saxon_filename, self.saxon_dirname = os.path.basename(saxon), os.path.dirname(saxon)
        self.__transform__ = [
            "java", "-cp",
            "{jarname}:.:{jardir}".format(jarname=saxon_filename, jardir=self.saxon_dirname),
            "net.sf.saxon.Transform", "-s:-",
            "-xsl:{xsl}".format(xsl=self.__xslt__)
            # "-deliminator:{deli}".format(deli=type(self).DELIMINATOR.decode().replace("\n", ""))
        ]

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
        process = Popen(
            self.__transform__,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            close_fds=True,
            cwd=self.saxon_dirname
        )
        xml = etree.tostring(xmlcontent, encoding="utf-8")
        output, error = process.communicate(xml)
        if error:
            raise XSLError(error.decode())
        else:
            if self.cache:
                self.cache.set(urn, output)
            return output.decode("utf-8")
