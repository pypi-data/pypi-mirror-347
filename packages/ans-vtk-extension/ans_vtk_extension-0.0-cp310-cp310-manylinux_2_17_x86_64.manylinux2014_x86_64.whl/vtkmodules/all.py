""" This module loads the entire VTK library into its namespace.  It
also allows one to use specific packages inside the vtk directory.."""

from __future__ import absolute_import

# --------------------------------------
from .vtkCommonCore import *
from .vtkCommonMath import *
from .vtkCommonTransforms import *
from .vtkCommonDataModel import *
from .vtkCommonExecutionModel import *
from .vtkFiltersGeometry import *
from .vtkWebCore import *
from .vtkCommonSystem import *
from .vtkCommonMisc import *
from .vtkFiltersCore import *
from .vtkFiltersGeneral import *
from .vtkIOCore import *
from .vtkImagingCore import *
from .vtkIOImage import *
from .vtkParallelCore import *
from .vtkIOXMLParser import *
from .vtkIOXML import *
from .vtkRenderingCore import *
from .vtkRenderingContext2D import *
from .vtkRenderingFreeType import *
from .vtkRenderingSceneGraph import *
from .vtkRenderingVtkJS import *
from .vtkIOExport import *
from .vtkWebGLExporter import *
from .vtkInteractionStyle import *
from .vtkFiltersSources import *
from .vtkInteractionWidgets import *
from .vtkViewsCore import *
from .vtkViewsInfovis import *
from .vtkChartsCore import *
from .vtkCommonColor import *
from .vtkFiltersExtraction import *
from .vtkFiltersStatistics import *
from .vtkFiltersImaging import *
from .vtkFiltersModeling import *
from .vtkImagingGeneral import *
from .vtkImagingSources import *
from .vtkInfovisCore import *
from .vtkInfovisLayout import *
from .vtkImagingColor import *
from .vtkTestingRendering import *
from .vtkFiltersHyperTree import *
from .vtkSerializationManager import *
from .vtkRenderingLabel import *
from .vtkRenderingLOD import *
from .vtkRenderingImage import *
from .vtkRenderingHyperTreeGrid import *
from .vtkRenderingUI import *
from .vtkRenderingOpenGL2 import *
from .vtkRenderingContextOpenGL2 import *
from .vtkImagingMath import *
from .vtkRenderingVolume import *
from .vtkRenderingVolumeOpenGL2 import *
from .vtkIOExportPDF import *
from .vtkRenderingGL2PSOpenGL2 import *
from .vtkIOExportGL2PS import *
from .vtkFiltersCellGrid import *
from .vtkIOCellGrid import *
from .vtkIOLegacy import *
from .vtkDomainsChemistry import *
from .vtkIOGeometry import *
from .vtkFiltersHybrid import *
from .vtkFiltersVerdict import *
from .vtkInteractionImage import *
from .vtkCommonComputationalGeometry import *
from .vtkImagingHybrid import *
from .vtkFiltersTexture import *
from .vtkRenderingAnnotation import *
from .vtkDomainsChemistryOpenGL2 import *
from .vtkFiltersReduction import *


# useful macro for getting type names
from .util.vtkConstants import vtkImageScalarTypeNameMacro

# import convenience decorators
from .util.misc import calldata_type

# import the vtkVariant helpers
from .util.vtkVariant import *
