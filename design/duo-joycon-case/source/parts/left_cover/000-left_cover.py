
w=param("left_cover_width",22.2)
length=param("left_cover_length",96.0)
height=param("left_cover_height",10.2)
roof=param("left_cover_roof_thickness",1.6)
radius=param("left_cover_corner_radius",1.0)
inner_length=param("left_cover_inner_length",83.0)
transition=param("left_cover_transition_span",16.0)
seam=param("left_cover_seam_inset",0.2)

def wing_profile(w, length, inner_length, transition, r):
    a=-w/2
    b=w/2
    t=min(a+transition,b-r)
    yt=length/2
    yi=inner_length/2
    k=0.5522847498
    with BuildSketch() as sketch:
        with BuildLine():
            Line((a,-yi),(a,yi))
            Bezier((a,yi),((a+t)/2,yi),((a+t)/2,yt),(t,yt))
            Line((t,yt),(b-r,yt))
            Bezier((b-r,yt),(b-r+k*r,yt),(b,yt-r+k*r),(b,yt-r))
            Line((b,yt-r),(b,-yt+r))
            Bezier((b,-yt+r),(b,-yt+r-k*r),(b-r+k*r,-yt),(b-r,-yt))
            Line((b-r,-yt),(t,-yt))
            Bezier((t,-yt),((a+t)/2,-yt),((a+t)/2,-yi),(a,-yi))
        make_face()
    return sketch.sketch

outline=wing_profile(w-2*seam,length-2*seam,inner_length-2*seam,transition,max(radius-seam,seam))
outline=Rot(0,0,180)*outline
# Only the top plate is detachable. All lower sidewalls now belong to rear_shell.
lid=Pos(0,0,height-roof)*extrude(outline,amount=roof)


slot_l=param("left_cover_slot_length",14.0)
slot_w=param("left_cover_slot_width",2.8)
slot_pitch=param("left_cover_slot_pitch",7.0)
slot_y=param("left_cover_slot_y",0.0)
for sign in [-1,1]:
    lid-=Pos(sign*slot_pitch/2,slot_y,height-roof-1)*extrude(SlotOverall(slot_l,slot_w,rotation=90),amount=roof+2)

lid.color=Color(0.18,0.21,0.25)
publish("left_cover",lid,"左侧曲线出声上盖",material="petg")
assert len(lid.solids())==1
