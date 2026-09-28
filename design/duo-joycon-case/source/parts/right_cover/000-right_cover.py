
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


hole_w=param("right_cover_key_hole_width",8.8)
hole_l=param("right_cover_key_hole_length",10.8)
hole_r=param("right_cover_key_hole_radius",2.4)
key_x=param("right_cover_key_x",4.5)
key_y=param("right_cover_key_y",3.45)
key_pitch=param("right_cover_key_pitch",24.0)
for sign in [-1,1]:
    lid-=Pos(key_x,key_y+sign*key_pitch/2,height-roof)*extrude(RectangleRounded(hole_w,hole_l,hole_r),amount=roof+1)

lid.color=Color(0.18,0.21,0.25)
publish("right_cover",lid,"右侧曲线音量上盖",material="petg")
assert len(lid.solids())==1
