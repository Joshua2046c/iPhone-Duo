
w=param("right_cover_width",19.2)
length=param("right_cover_length",84.0)
height=param("right_cover_height",10.2)
roof=param("right_cover_roof_thickness",1.6)
wall=param("right_cover_wall_thickness",2.0)
radius=param("right_cover_corner_radius",4.0)
foot_depth=param("right_cover_foot_depth",6.0)
foot_inset=param("right_cover_foot_inset",9.0)
tape_depth=param("right_cover_tape_depth",0.3)
tape_w=param("right_cover_tape_width",12.0)
tape_l=param("right_cover_tape_length",4.0)
# Roof and U-shaped skirt. Phone-facing edge stays open to the original port / linkage.
outline=RectangleRounded(w,length,radius)
lid=extrude(outline,amount=height)
lid-=extrude(RectangleRounded(w-2*wall,length-2*wall,radius-wall),amount=height-roof)
lid-=Pos(-1*w/2,0,(height-roof)/2)*Box(3*wall,length-2*radius,height-roof)
# Two full-height end supports carry finger loads. Recesses locate removable tape.
for sign in [-1,1]:
    fy=sign*(length/2-foot_inset)
    lid+=Pos(0,fy,(height-roof)/2)*Box(w,foot_depth,height-roof)
    lid-=Pos(0,fy,tape_depth/2)*Box(tape_w,tape_l,tape_depth)

hole_w=param("right_cover_key_hole_width",8.8)
hole_l=param("right_cover_key_hole_length",10.8)
hole_r=param("right_cover_key_hole_radius",2.4)
key_x=param("right_cover_key_x",3.3)
key_y=param("right_cover_key_y",3.45)
key_pitch=param("right_cover_key_pitch",24.0)
for sign in [-1,1]:
    lid-=Pos(key_x,key_y+sign*key_pitch/2,height-roof)*extrude(RectangleRounded(hole_w,hole_l,hole_r),amount=roof+1)

lid.color=Color(0.18,0.21,0.25)
publish("right_cover",lid,"右侧音量机构盖板",material="petg")
assert len(lid.solids())==1
