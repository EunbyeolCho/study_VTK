"""
https://vtk.org/Wiki/VTK/Examples/Python/Visualization/AssignColorsCellFromLUT
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
    lut.Build()

    #Fill in a few known colors, the rest will be generated if needed
    lut.SetTableValue(0, nc.GetColor4d("Black"))
    lut.SetTableValue(1, nc.GetColor4d("Banana"))
    lut.SetTableValue(2, nc.GetColor4d("Tomato"))
    lut.SetTableValue(3, nc.GetColor4d("Lavender"))

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
        lut.GetColor(float(i) / (tableSize - 1),rgb)
        ucrgb = list(map(int, [x * 255 for x in rgb]))
        colors.InsertNextTuple3(ucrgb[0], ucrgb[1], ucrgb[2])
        s = '['+ ', '.join(['{:0.6f}'.format(x) for x in rgb]) + ']'
        print(s, ucrgb)


def main():


    nc = vtk.vtkNamedColors()
    resolution = 3

    plane11 = vtk.vtkPlaneSource()
    plane11.SetXResolution(resolution)
    plane11.SetYResolution(resolution)


    tableSize = max(resolution * resolution + 1, 10)


    plane11.Update()
    lut1 = MakeLUT(tableSize)

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
    ren11.SetBackground(nc.GetColor3d('MidnightBlue'))


    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(800, 800)
    renWin.AddRenderer(ren11)

    ren11.AddActor(actor11)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    renWin.Render()

    return iren


if __name__ == '__main__':
    
    
    iren = main()
    iren.Start()
    

