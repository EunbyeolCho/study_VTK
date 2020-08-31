"""
https://vtk.org/Wiki/VTK/Examples/Python/Interaction/MouseEvents
Practice vtk mouseevents
"""


from __future__ import print_function
import vtk


#Initialize Renderer
ren = vtk.vtkRenderer()
ren.GradientBackgroundOn()
ren.SetBackground(135/255, 206/255, 235/255)
ren.SetBackground2(44/255, 125/255, 158/255)
renWin = vtk.vtkRenderWindow()
# renWin.SetFullScreen(True)
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

def MakeActor(sphereSource):
    
    #Visualize
    mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(polydata)
    mapper.SetInputConnection(sphereSource.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, polydata, parent=None):
        self.AddObserver("LeftButtonPressEvent", self.LeftButtonPressEvent)
        self.AddObserver("MouseMoveEvent", self.MouseMove)
        self.AddObserver("LeftButtonReleaseEvent", self.LeftButtonReleaseEvent)

        self.source = polydata
        self.planeActor = MakeActor(source)
        
        self.pickedPosition = -1

    def LeftButtonPressEvent(self,obj,event):

        print("Middle Button pressed")
        self.OnLeftButtonDown()

        ###
        pos = obj.GetInteractor().GetEventPosition()

        picker = vtk.vtkCellPicker()
        picker.PickFromListOn()
        #Add an actor to the pick list.
        picker.AddPickList(self.planeActor)
        picker.Pick(pos[0], pos[1], 0, ren)

        position = picker.GetPickPosition()

        if picker.GetActor() == self.planeActor:
            self.pickedPosition = position

        return

    def LeftButtonReleaseEvent(self,obj,event):

        print("Middle Button released")
        self.pickedPosition = -1
        self.OnLeftButtonUp()
        return


    def MouseMove(self,obj,event):
        print("Mouse Move")

        if self.pickedPosition == -1:
            self.OnMouseMove()
            return

        pos = obj.GetInteractor().GetEventPosition()

        picker = vtk.vtkCellPicker()
        picker.PickFromListOn()
        picker.AddPickList(self.planeActor)
        picker.Pick(pos[0], pos[1], 0, ren)

        position = picker.GetPickPosition()



source = vtk.vtkSphereSource()
source.SetCenter(0, 0, 0)
source.SetRadius(1)
source.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)

renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(source))
interactor.SetRenderWindow(renwin)

interactor.Initialize()
interactor.Start()