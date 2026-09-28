
w=param("left_cover_width",19.2)
length=param("left_cover_length",84.0)
height=param("left_cover_height",10.2)
roof=param("left_cover_roof_thickness",1.6)
wall=param("left_cover_wall_thickness",2.0)
radius=param("left_cover_corner_radius",4.0)
foot_depth=param("left_cover_foot_depth",6.0)
foot_inset=param("left_cover_foot_inset",9.0)
tape_depth=param("left_cover_tape_depth",0.3)
tape_w=param("left_cover_tape_width",12.0)
tape_l=param("left_cover_tape_length",4.0)
# Roof and U-shaped skirt. Phone-facing edge stays open to the original port / linkage.
outline=RectangleRounded(w,length,radius)
lid=extrude(outline,amount=height)
lid-=extrude(RectangleRounded(w-2*wall,length-2*wall,radius-wall),amount=height-roof)
lid-=Pos(1*w/2,0,(height-roof)/2)*Box(3*wall,length-2*radius,height-roof)
# Two full-height end supports carry finger loads. Recesses locate removable tape.
for sign in [-1,1]:
    fy=sign*(length/2-foot_inset)
    lid+=Pos(0,fy,(height-roof)/2)*Box(w,foot_depth,height-roof)
    lid-=Pos(0,fy,tape_depth/2)*Box(tape_w,tape_l,tape_depth)

slot_l=param("left_cover_slot_length",14.0)
slot_w=param("left_cover_slot_width",2.8)
slot_pitch=param("left_cover_slot_pitch",7.0)
slot_y=param("left_cover_slot_y",0.0)
for sign in [-1,1]:
    lid-=Pos(sign*slot_pitch/2,slot_y,height-roof)*extrude(SlotOverall(slot_l,slot_w,rotation=90),amount=roof+1)

lid.color=Color(0.18,0.21,0.25)
publish("left_cover",lid,"左侧双槽出声盖板",material="petg")
assert len(lid.solids())==1
