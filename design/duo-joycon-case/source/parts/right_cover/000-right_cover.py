# cell: right_cover
# cell: right_cover
# cell: right_cover

w=param("right_cover_width",22.2)
length=param("right_cover_length",96.0)
height=param("right_cover_height",10.2)
roof=param("right_cover_roof_thickness",1.6)
radius=param("right_cover_corner_radius",1.0)
inner_length=param("right_cover_inner_length",83.0)
transition=param("right_cover_transition_span",16.0)
seam=param("right_cover_seam_inset",0.2)

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

# Only the top plate is detachable. All lower sidewalls now belong to rear_shell.
lid=Pos(0,0,height-roof)*extrude(outline,amount=roof)


# Existing hole width controls the circular opening diameter.
hole_w=param("right_cover_key_hole_width",8.8)
key_x=param("right_cover_key_x",4.5)
key_y=param("right_cover_key_y",3.45)
key_pitch=param("right_cover_key_pitch",24.0)
for sign in [-1,1]:
    lid-=Pos(key_x,key_y+sign*key_pitch/2,height-roof)*extrude(Circle(hole_w/2),amount=roof+1)

peg_w=param("right_cover_peg_width",4.0)
peg_l=param("right_cover_peg_length",8.0)
peg_pitch=param("right_cover_peg_spacing",72.0)
peg_x=param("right_cover_peg_x",0.0)
lead=param("right_cover_peg_leadin",0.4)
split=param("right_cover_peg_split",1.6)
root=param("right_cover_peg_root",0.8)
barb=param("right_cover_peg_retention",0.4)
barb_h=param("right_cover_peg_retention_height",1.2)
release_h=param("right_cover_peg_release_height",0.4)
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
publish("right_cover",lid,"右侧曲线音量上盖",material="petg")
assert len(lid.solids())==1
