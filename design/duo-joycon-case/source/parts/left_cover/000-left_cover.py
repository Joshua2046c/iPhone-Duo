# cell: left_cover
# cell: left_cover
# cell: left_cover
# cell: left_cover

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

outline=Pos(radius,0)*wing_profile(w+2*radius,length,inner_length,transition,radius)
# End curves follow the lower shell exactly; clearance is kept on the two long sides.
outline=outline & Rectangle(w-2*seam,length)
outline=Rot(0,0,180)*outline
# Only the top plate is detachable. All lower sidewalls now belong to rear_shell.
lid=Pos(0,0,height-roof)*extrude(outline,amount=roof)
# Fixed envelope data from the supplied STL rail: 14 mm high, R4 longitudinal ends.
RAIL_PROFILE_HEIGHT=14.0
RAIL_END_RADIUS=4.0
end_envelope=extrude(Plane.YZ*Pos(0,height-RAIL_PROFILE_HEIGHT/2)*RectangleRounded(length,RAIL_PROFILE_HEIGHT,RAIL_END_RADIUS),amount=w,both=True)
lid=lid & end_envelope


slot_l=param("left_cover_slot_length",14.0)
slot_w=param("left_cover_slot_width",2.8)
# Two slots are stacked on the same vertical centreline (Y direction).
slot_pitch=param("left_cover_slot_pitch",24.0)
slot_y=param("left_cover_slot_y",0.0)
for sign in [-1,1]:
    lid-=Pos(0,slot_y+sign*slot_pitch/2,height-roof-1)*extrude(SlotOverall(slot_l,slot_w,rotation=90),amount=roof+2)

peg_w=param("left_cover_peg_width",4.0)
peg_l=param("left_cover_peg_length",8.0)
peg_pitch=param("left_cover_peg_spacing",72.0)
peg_x=param("left_cover_peg_x",0.0)
lead=param("left_cover_peg_leadin",0.4)
split=param("left_cover_peg_split",1.6)
root=param("left_cover_peg_root",0.8)
barb=param("left_cover_peg_retention",0.4)
barb_h=param("left_cover_peg_retention_height",1.2)
release_h=param("left_cover_peg_release_height",0.4)
for end in [-1,1]:
    yy=end*peg_pitch/2
    bottom=height-roof-peg_l
    peg=Pos(peg_x,yy,bottom+peg_l/2)*Box(peg_w,peg_w,peg_l)
    peg=chamfer(peg.faces().sort_by(Axis.Z)[0].edges(),length=lead)
    ramp=loft([Pos(peg_x,yy,bottom+lead)*Rectangle(peg_w,peg_w),
               Pos(peg_x,yy,bottom+lead+barb_h)*Rectangle(peg_w+2*barb,peg_w),
               Pos(peg_x,yy,bottom+lead+barb_h+release_h)*Rectangle(peg_w,peg_w)],ruled=True)
    peg+=ramp
    peg-=Pos(peg_x,yy,bottom+(peg_l-root)/2-0.05)*Box(split,peg_w+2*barb+1,peg_l-root+0.1)
    lid+=peg
# Pegs and relieved square sockets are separated in their seated position.
# Their spring arms deflect during insertion; the retained shoulders need no static overlap declaration.
lid.color=Color(0.18,0.21,0.25)
publish("left_cover",lid,"左侧曲线出声上盖",material="petg")
assert len(lid.solids())==1
