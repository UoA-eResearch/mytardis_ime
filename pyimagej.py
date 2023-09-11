import imagej
import scyjava

from scyjava import jimport

ij = imagej.init('sc.fiji:fiji:2.14.0')
print(f"ImageJ version: {ij.getVersion()}")

scyjava.config.add_options('-Xmx6g')
ij = imagej.init()

System = jimport('java.lang.System')




## open .vsi file
# initialize ImageJ
ij = imagej.init(mode='interactive')

# open the .vsi image series
ij.IJ.run("Bio-Formats Importer", "open=/path/to/image.vsi autoscale color_mode=Default open_all_series rois_import=[ROI Manager] view=Hyperstack stack_order="XYCZT")
          
#You can obtain the individual ImagePlus images with the WindowManager. Accessible via ij.WindowManager after PyImageJ has been initialized with the legacy option.


import jpype
import scyjava
import jpype.imports
from jpype.types import *

scyjava.config.endpoints.append("ome:formats-gpl:6.7.0")
scyjava.start_jvm()
loci = jpype.JPackage("loci")
loci.common.DebugTools.setRootLevel("ERROR")

# Java class for reading images
from loci.formats import ImageReader

reader = ImageReader()
# Set the path to read from
reader.setId("good image 02.oib")
# See https://javadoc.scijava.org/Bio-Formats/loci/formats/ImageReader.html#openBytes-int-
reader.readBytes(0)
# Get metadata and convert to dict
metadata = dict(reader.getGlobalMetadata())