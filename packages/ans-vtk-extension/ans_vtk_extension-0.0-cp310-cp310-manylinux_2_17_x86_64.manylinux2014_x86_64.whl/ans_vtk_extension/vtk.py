"""This is the vtk module"""

# this module has the same contents as vtkmodules.all
from vtkmodules.vtkCommonCore import *
from vtkmodules.vtkCommonMath import *
from vtkmodules.vtkCommonTransforms import *
from vtkmodules.vtkCommonDataModel import *
from vtkmodules.vtkCommonExecutionModel import *
from vtkmodules.vtkFiltersGeometry import *
from vtkmodules.vtkWebCore import *
from vtkmodules.vtkCommonSystem import *
from vtkmodules.vtkCommonMisc import *
from vtkmodules.vtkFiltersCore import *
from vtkmodules.vtkFiltersGeneral import *
from vtkmodules.vtkIOCore import *
from vtkmodules.vtkImagingCore import *
from vtkmodules.vtkIOImage import *
from vtkmodules.vtkParallelCore import *
from vtkmodules.vtkIOXMLParser import *
from vtkmodules.vtkIOXML import *
from vtkmodules.vtkRenderingCore import *
from vtkmodules.vtkRenderingContext2D import *
from vtkmodules.vtkRenderingFreeType import *
from vtkmodules.vtkRenderingSceneGraph import *
from vtkmodules.vtkRenderingVtkJS import *
from vtkmodules.vtkIOExport import *
from vtkmodules.vtkWebGLExporter import *
from vtkmodules.vtkInteractionStyle import *
from vtkmodules.vtkFiltersSources import *
from vtkmodules.vtkInteractionWidgets import *
from vtkmodules.vtkViewsCore import *
from vtkmodules.vtkViewsInfovis import *
from vtkmodules.vtkChartsCore import *
from vtkmodules.vtkCommonColor import *
from vtkmodules.vtkFiltersExtraction import *
from vtkmodules.vtkFiltersStatistics import *
from vtkmodules.vtkFiltersImaging import *
from vtkmodules.vtkFiltersModeling import *
from vtkmodules.vtkImagingGeneral import *
from vtkmodules.vtkImagingSources import *
from vtkmodules.vtkInfovisCore import *
from vtkmodules.vtkInfovisLayout import *
from vtkmodules.vtkImagingColor import *
from vtkmodules.vtkTestingRendering import *
from vtkmodules.vtkFiltersHyperTree import *
from vtkmodules.vtkSerializationManager import *
from vtkmodules.vtkRenderingLabel import *
from vtkmodules.vtkRenderingLOD import *
from vtkmodules.vtkRenderingImage import *
from vtkmodules.vtkRenderingHyperTreeGrid import *
from vtkmodules.vtkRenderingUI import *
from vtkmodules.vtkRenderingOpenGL2 import *
from vtkmodules.vtkRenderingContextOpenGL2 import *
from vtkmodules.vtkImagingMath import *
from vtkmodules.vtkRenderingVolume import *
from vtkmodules.vtkRenderingVolumeOpenGL2 import *
from vtkmodules.vtkIOExportPDF import *
from vtkmodules.vtkRenderingGL2PSOpenGL2 import *
from vtkmodules.vtkIOExportGL2PS import *
from vtkmodules.vtkFiltersCellGrid import *
from vtkmodules.vtkIOCellGrid import *
from vtkmodules.vtkIOLegacy import *
from vtkmodules.vtkDomainsChemistry import *
from vtkmodules.vtkIOGeometry import *
from vtkmodules.vtkFiltersHybrid import *
from vtkmodules.vtkFiltersVerdict import *
from vtkmodules.vtkInteractionImage import *
from vtkmodules.vtkCommonComputationalGeometry import *
from vtkmodules.vtkImagingHybrid import *
from vtkmodules.vtkFiltersTexture import *
from vtkmodules.vtkRenderingAnnotation import *
from vtkmodules.vtkDomainsChemistryOpenGL2 import *
from vtkmodules.vtkFiltersReduction import *


# useful macro for getting type names
from vtkmodules.util.vtkConstants import vtkImageScalarTypeNameMacro

# import convenience decorators
from vtkmodules.util.misc import calldata_type

# import the vtkVariant helpers
from vtkmodules.util.vtkVariant import *

# clone parts of vtkmodules to make this look like a package
import vtkmodules as _vtk_package
__path__ = _vtk_package.__path__
__version__ = _vtk_package.__version__
del _vtk_package
