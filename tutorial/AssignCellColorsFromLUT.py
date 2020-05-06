"""
https://vtk.org/Wiki/VTK/Examples/Python/Visualization/AssignColorsCellFromLUT
https://vtk.org/Wiki/VTK/Examples/Cxx/Visualization/AssignCellColorsFromLUT
"""

from __future__ import print_function
import vtk


def MakeLUT(tableSize):
    """
    Make a lookup table from a set of named colors
    """

    nc = vtk.vtkNamedColors()

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(tableSize)
    # lut.SetTableRange(0.0, 10.0)
    lut.Build()

    #Fill in a few known colors, the rest will be generated if needed
    lut.SetTableValue(0, nc.GetColor4d("Black"))
    lut.SetTableValue(1, nc.GetColor4d("Banana"))
    lut.SetTableValue(2, nc.GetColor4d("Tomato"))
    lut.SetTableValue(3, nc.GetColor4d("Wheat"))
    lut.SetTableValue(4, nc.GetColor4d("Lavender"))
    lut.SetTableValue(5, nc.GetColor4d("Flesh"))
    lut.SetTableValue(6, nc.GetColor4d("Raspberry"))

    return lut


def MakeLUTFromCTF(tableSize):
    '''
    Use a color transfer Function to generate the colors in the lookup table.
    :param: tableSize - The table size
    :return: The lookup table.
    '''
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    # Green to tan.
    ctf.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
    ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(1.0, 0.677, 0.492, 0.093)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(tableSize)
    lut.Build()

    for i in range(0,tableSize):
        rgb = list(ctf.GetColor(float(i)/tableSize))+[1]
        lut.SetTableValue(i,rgb)

    return lut



def MakeCellData(tableSize, lut, colors):
    '''
    Create the cell data using the colors from the lookup table.
    :param: tableSize - The table size
    :param: lut - The lookup table.
    :param: colors - A reference to a vtkUnsignedCharArray().
    '''
    for i in range(1,tableSize):
        rgb = [0.0, 0.0, 0.0]
        #Get the interpolated color. Of course you can use any function whose range is [0...1]
        #In this case we are just using the cell (Id + 1)/(tableSize - 1) to get the interpolated color.
        lut.GetColor(float(i) / (tableSize - 1), rgb)

        ucrgb = list(map(int, [x * 255 for x in rgb]))
        colors.InsertNextTuple3(ucrgb[0], ucrgb[1], ucrgb[2])
        s = '['+ ', '.join(['{:0.6f}'.format(x) for x in rgb]) + ']'
        print(s, ucrgb)


def main():


    nc = vtk.vtkNamedColors()
    resolution = 3
    tableSize = max(resolution * resolution + 1, 10)


    plane11 = vtk.vtkPlaneSource()
    plane11.SetXResolution(resolution)
    plane11.SetYResolution(resolution)
    plane11.Update()

    lut1 = MakeLUT(tableSize)
    # lut1 = MakeLUTFromCTF(tableSize)


    colorData1 = vtk.vtkUnsignedCharArray()
    colorData1.SetName('colors') # Any name will work here.
    colorData1.SetNumberOfComponents(3)
    print('Using a lookup table from a set of named colors.')

    MakeCellData(tableSize, lut1, colorData1)
    plane11.GetOutput().GetCellData().SetScalars(colorData1)



    # Set up actor and mapper
    mapper11 = vtk.vtkPolyDataMapper()
    mapper11.SetInputConnection(plane11.GetOutputPort())

    mapper11.SetScalarModeToUseCellData()
    mapper11.Update()

    actor11 = vtk.vtkActor()
    actor11.SetMapper(mapper11)

    ren11 = vtk.vtkRenderer()
    ren11.AddActor(actor11)
    ren11.SetBackground(nc.GetColor3d('MidnightBlue'))

    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(800, 800)
    renWin.AddRenderer(ren11)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    renWin.Render()

    return iren


if __name__ == '__main__':
    
    
    iren = main()
    iren.Start()
    

