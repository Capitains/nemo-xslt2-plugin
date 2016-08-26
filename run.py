from nemo_xslttwo_plugin import SaxonShellTransform
import logging
from capitains_nautilus.flask_ext import NautilusRetriever
from flask_nemo import Nemo
from flask import Flask


saxon = SaxonShellTransform(
    "./jars/saxon.jar",
    "./tests/data/xsl/ciham.xsl"
)
nautilus = NautilusRetriever(
    folders=[
        "./tests/data/repo"
    ]
)
nautilus.logger.setLevel(logging.ERROR)

app = Flask("Nemo")
app.debug = True
nemo = Nemo(
    app=app,
    base_url="",
    retriever=nautilus,
    transform={
        "default": saxon.transform
    }
)

if __name__ == "__main__":
    app.run(debug=True)