#Author-rmmshv
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def makeLines(sketch, core, lines, origin, constraints, points, dimensions, arcs):

    x = 1.5
    y = 1.5
    
    p_center = points.add(core(0, 0, 0))
    p_center.isFixed = True
    # Construction lines

    
    for i in range(2, 6):
        l_diag1 = lines.addByTwoPoints(core(-x * i, y * i, 0), core(x * i, -y * i, 0))
        l_diag2 = lines.addByTwoPoints(core(-x * i, -y * i,0), core(x * i, y *i , 0))
        l_diag1.isConstruction = True
        l_diag2.isConstruction = True
        l_left = lines.addByTwoPoints(l_diag1.startSketchPoint, l_diag2.startSketchPoint)
        l_right = lines.addByTwoPoints(l_diag2.endSketchPoint, l_diag1.endSketchPoint)    
        l_top = lines.addByTwoPoints(l_diag1.startSketchPoint, l_diag2.endSketchPoint)
        l_bot = lines.addByTwoPoints(l_diag2.startSketchPoint, l_diag1.endSketchPoint)
  
        # Constrain the lines
        constraints.addCoincident(p_center,l_diag1);
        constraints.addCoincident(p_center, l_diag2)
        constraints.addPerpendicular(l_diag1, l_diag2)
        constraints.addPerpendicular(l_left, l_bot)
        constraints.addPerpendicular(l_top, l_right)
        constraints.addHorizontal(l_bot)
        constraints.addHorizontal(l_top)
    
        # Add the fillet mignon
        arc_top_l = arcs.addFillet(l_left, l_left.startSketchPoint.geometry, l_top, l_top.startSketchPoint.geometry, 1)
        arc_top_r = arcs.addFillet(l_top, l_top.endSketchPoint.geometry, l_right, l_right.startSketchPoint.geometry, 1)
        arc_bot_l = arcs.addFillet(l_left, l_left.endSketchPoint.geometry, l_bot, l_bot.startSketchPoint.geometry, 1)
        arc_bot_r = arcs.addFillet(l_bot, l_bot.endSketchPoint.geometry, l_right, l_right.endSketchPoint.geometry, 1)
        dimensions.addDistanceDimension(l_bot.startSketchPoint, l_bot.endSketchPoint, 0, core(-4 * i, 4 * i, 0))
        dimensions.addDistanceDimension(l_left.startSketchPoint, l_left.endSketchPoint, 0, core(-4 * i, 3 * i, 0))
        dimensions.addRadialDimension(arc_top_l,adsk.core.Point3D.create(-3 * i, 3 *i, 0))
        dimensions.addRadialDimension(arc_top_r,adsk.core.Point3D.create(3 * i, 2.5 *i, 0))
        dimensions.addRadialDimension(arc_bot_l,adsk.core.Point3D.create(-3 * i, -2 *i, 0))
        #dimensions.addRadialDimension(arc_bot_r,adsk.core.Point3D.create(5 * i, 5 *i, 0)) # it'll overconstraint it

def makePoints(sketch, core, constraints, origin):
    
    points = sketch.sketchPoints    
    p_center = points.add(core(0, 0, 0))
    
    # Constraint the point
    constraints.addCoincident(origin, p_center)
    
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
      
        design = app.activeProduct;
        root = adsk.fusion.Component.cast(design.rootComponent);
        
        sketches = root.sketches;
        xyPlane = root.xYConstructionPlane;
        s = sketches.add(xyPlane);
        origin = s.originPoint;
                
        coreP3D = adsk.core.Point3D.create;
        dimensions = s.sketchDimensions;
        arcs = s.sketchCurves.sketchArcs;
        lines = s.sketchCurves.sketchLines;
        points = s.sketchPoints;
        constraints = s.geometricConstraints;
        
        makeLines(s, coreP3D, lines, origin, constraints, points, dimensions, arcs)
        makePoints(s, coreP3D, constraints, origin)
              
        
    except:
        if ui:
            ui.messageBox('Failed. Try again. You got this.\n{}'.format(traceback.format_exc()))