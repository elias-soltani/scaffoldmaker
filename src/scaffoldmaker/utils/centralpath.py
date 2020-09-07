"""
Utility functions for generating a central path used to generate cylinders and tubes.
"""

from scaffoldmaker.meshtypes.meshtype_1d_path1 import extractPathParametersFromRegion
from scaffoldmaker.utils import interpolation as interp


def getCentralPathNodes(region, centralPath, printNodes=False):
    """
    Get nodes on the central path and print them as a table if required.
    :param region: Zinc region to define model in.
    :param centralPath: 1D scaffold created using meshtype_1d_path1
    :param printNodes: If true, prints the table of node coordinates and derivatives.
    :return: coordinates and derivatives
    """
    tmpRegion = region.createRegion()
    centralPath.generate(tmpRegion)
    cx, cd1, cd2, cd12 = extractPathParametersFromRegion(tmpRegion)
    if printNodes:
        for i in range(len(cx)):
            print(i, '[', cx[i], ',', cd1[i], ',', cd2[i], ',', cd12[i], '],')
    del tmpRegion

    return cx, cd1, cd2, cd12


def smoothD1Derivatives(cx, cd1):
    """
    Smooth d1 derivatives. Fix all directions.
    :param cx: coordinates along the path.
    :param cd1: d1 derivatives.
    :return: smooth d1.
    """
    sd1 = interp.smoothCubicHermiteDerivativesLine(cx, cd1, fixAllDirections=True,
                                                   magnitudeScalingMode=interp.DerivativeScalingMode.HARMONIC_MEAN)
    return sd1


def calculateTotalLength(cx, sd1, printArcLength=False):
    """
    Calculate total length of a curve
    :param cx: coordinates along the path.
    :param sd1: d1 derivatives.
    :param printArcLength: If true, print a table of elements arc lengths.
    :return:
    """
    totalLength = 0.0
    elementsCountIn = len(cx) - 1
    for e in range(elementsCountIn):
        arcLength = interp.getCubicHermiteArcLength(cx[e], sd1[e], cx[e + 1], sd1[e + 1])
        if printArcLength:
            print(e+1, arcLength)
        totalLength += arcLength

    return totalLength


def sampleCentralPath(cx, cd1, cd2, cd12, elementsCount):
    """
    Sample elements along the path
    :param cx: coordinates along the path.
    :param cd1: d1 derivatives.
    :param cd2: d2 derivatives.
    :param cd12: rate of change of d2 along d1.
    :param elementsCount: number of elements to be created.
    :return: coordinates and derivatives sampled along the path.
    """
    sx, sd1, se, sxi, ssf = interp.sampleCubicHermiteCurves(cx, cd1, elementsCount)
    sd2, sd12 = interp.interpolateSampleCubicHermite(cd2, cd12, se, sxi, ssf)

    return sx, sd1, sd2, sd12
