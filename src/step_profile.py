import math


class Step_profile:
    
    def one_step(self, d1, d1_length, shank_d, oal,point): 
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

        return points

    def two_steps(self, d1, d1_length, d2, d2_length, shank_d, oal,point): 
        chamfer = 1
        tip = -round(((math.tan(math.radians((180 - point) / 2))) * (d1 / 2)), 3)
        # d2_length = round((math.tan(round(math.radians(90 - (step_angle / 2)), 5)) * ((d2 - d1) / 2)), 5)
        step_1_l = round((math.tan(round(math.radians(90-(90/2)), 5))*((d2-d1)/2)), 5)

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
       
        return points
    
    def three_steps(self, d1, d1_length, d2, d2_length, d3, d3_length, shank_d, oal, point): 

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
        
        return points