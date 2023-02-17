import ezdxf
import math
from ezdxf.addons.drawing import matplotlib

class Drawing:
    def __init__(self,):
        self.dwg = ezdxf.new('R2000')
        self.dwg.layers.add(name="MyLines", color=7, linetype="DASHED")

    def add_profile_one(self, d1, d1_length, shank_d, oal,point):
        msp = self.dwg.modelspace()
        chamfer = 1
        tip = -round(((math.tan(math.radians((180 - point) / 2))) * (d1 / 2)), 3)

        p1 = (tip, 0)
        p2 = (0, d1/2)
        p3 = (d1_length,d1/2)
        p4 = (d1_length, shank_d / 2)
        p5 = (oal-chamfer, shank_d / 2 )
        p6 = (oal, shank_d / 2 - chamfer)
        p7 = (oal, 0)

        points = [ p1, p2, p3, p4, p5, p6, p7] 

        msp.add_lwpolyline(points)
        msp.add_line((points[0][0] - 1 ,0) , (oal+2,0), dxfattribs={'layer':'MyLines'})
        msp.add_lwpolyline(points).scale(1, -1, 1)

        dim = msp.add_aligned_dim(p1=(points[1]), p2=(oal,d1 / 2), distance=30, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2}) #oal
        dim1 = msp.add_aligned_dim(p1=(points[1]), p2=(points[2]), distance=15, override={'dimtad': 2,'dimasz': 2,'dimtxt': 2})           #d1 length
        dim2 = msp.add_aligned_dim(p1=(points[1]), p2=(( points[1][0], -points[1][1])), distance=-10, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2, 'dimjust':1}) # d1 
        dim3 = msp.add_aligned_dim(p1=(points[-3]), p2=(( points[-3][0], -points[-3][1])), distance=10, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2, 'dimjust':1})# shank diameter

        dimensions = [dim, dim1, dim2]
        for item in dimensions:
            item.render()

        return points

    def add_profile_two(self, d1, d1_length, d2, d2_length, step_angle, shank_d, oal,point): 
        msp = self.dwg.modelspace()
        chamfer = 1
        tip = -round(((math.tan(math.radians((180 - point) / 2))) * (d1 / 2)), 3)
        # d2_length = round((math.tan(round(math.radians(90 - (step_angle / 2)), 5)) * ((d2 - d1) / 2)), 5)
        step_1_l = round((math.tan(round(math.radians((180 - step_angle)/2), 5))*((d2-d1)/2)), 5)

        p1 = (tip, 0)  # Point angle start
        p2 = (0, d1 / 2)  # corner        
        p3 = (d1_length, d1/2 )
        p4 = (d1_length+step_1_l , d2/2, )
        p5 = (d2_length, d2/2, )
        p6 = (d2_length, shank_d / 2 )
        p7 = (oal-chamfer, shank_d / 2 )
        p8 = (oal, shank_d / 2 - chamfer)
        p9 = (oal,0 )

        points = [ p1, p2, p3, p4, p5, p6, p7, p8, p9]

        msp.add_lwpolyline(points)
        msp.add_line((points[0][0] - 1 ,0) , (oal+2,0), dxfattribs={'layer':'MyLines'})
        msp.add_lwpolyline(points).scale(1, -1, 1)

        return points

    def add_profile_three(self, d1, d1_length, d2, d2_length, d3, d3_length, shank_d, oal, point): 
        msp = self.dwg.modelspace()
        chamfer = 1
        tip = -round(((math.tan(math.radians((180 - point) / 2))) * (d1 / 2)), 3)

        p1 = (tip, 0)  # Point angle start
        p2 = (0, d1 / 2)  # corner        
        p3 = (d1_length, d1 / 2)
        p4 = (d1_length, d2 / 2)
        p5 = (d2_length, d2 / 2)
        p6 = (d2_length, d3 / 2)
        p7 = (d3_length, d3 / 2)
        p8 = (d3_length, shank_d / 2)
        p9 = (oal - chamfer, shank_d / 2)
        p10 = (oal, shank_d / 2 - chamfer)
        p11 = (oal, 0)
        points = (p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11)
        msp.add_lwpolyline(points)
        msp.add_line((points[0][0] - 1 ,0) , (oal+2,0), dxfattribs={'layer':'MyLines'})
        msp.add_lwpolyline(points).scale(1, -1, 1)   

         
        return points

    def add_endface(self,d1):
        msp = self.dwg.modelspace()
        tip = self.dwg.blocks.new(name = 'TIP')

        tip.add_circle((0,0), d1/2)
        msp.add_blockref('TIP', (-70,0))

    def add_frame(self):
        msp = self.dwg.modelspace()
        frame = self.dwg.blocks.new(name = 'FRAME')

        try: 
            frame_a4 = ezdxf.readfile('a4.DXF')
        except: 
            frame_a4 = ezdxf.readfile('src/a4.DXF')

        frame_ent = frame_a4.entities
        
        for i in frame_ent: 
            #print(i)
            frame.add_foreign_entity(i)

        msp.add_blockref('FRAME', (0,0))


    def save(self, name):
        self.dwg.saveas(f'{name}.dxf')
        matplotlib.qsave(self.dwg.modelspace(), f'drawing.pdf',dpi=100, bg='#FFFFFF')

# if __name__ == "__main__":
#     dwg = Drawing()
#     dwg.add_line((0, 0), (10, 10))
#     dwg.add_circle((5, 5), 3)
#     dwg.save()