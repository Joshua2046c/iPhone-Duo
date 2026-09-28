# cell: rear_shell
# cell: rear_shell

# Phone envelope from the user's size sheet, rotated into the reference pose.
PHONE_X = 117.8
PHONE_HALF_Y = 84.1  # folded width is only a provisional half-body envelope
gap = param("rear_shell_side_clearance", 0.5)
base = param("rear_shell_base_thickness", 2.4)
wall = param("rear_shell_wall_thickness", 2.4)
rise = param("rear_shell_wall_height", 3.4)
left = param("rear_shell_left_blank", 20.0)
right = param("rear_shell_right_control", 20.0)
setback = param("rear_shell_hinge_setback", 4.0)
corner = param("rear_shell_corner_radius", 6.0)
camw = param("rear_shell_camera_width", 22.0)
camh = param("rear_shell_camera_length", 56.0)
camx = param("rear_shell_camera_x", 41.5)
camy = param("rear_shell_camera_y", -8.5)
portw = param("rear_shell_port_relief_length", 24.0)
porty = param("rear_shell_port_relief_y", 0.0)
key_pitch = param("rear_shell_button_pitch", 24.0)
key_x = param("rear_shell_button_stop_x", 76.0)
stop_z = param("rear_shell_button_stop_height", 7.6)
stop_w = param("rear_shell_button_stop_width", 2.0)
stop_span = param("rear_shell_button_stop_spacing", 9.0)
stop_depth = param("rear_shell_button_stop_depth", 1.0)
keyslot = param("rear_shell_output_slot_width", 7.0)
wing_depth = param("rear_shell_wing_length", 96.0)
ix = PHONE_X + 2*gap
iy = PHONE_HALF_Y + 2*gap
ox = ix+2*wall
oy = iy+2*wall

transition = param("rear_shell_transition_span",16.0)
foundation = param("rear_shell_rail_foundation_width",4.8)
outer_r = param("rear_shell_outline_radius",1.0)
hinge_y = PHONE_HALF_Y/2-setback
front_y = -oy/2
xl = -ox/2-left-foundation
xr = ox/2+right+foundation
center_y = (hinge_y+front_y)/2
yt = center_y+wing_depth/2
yb = center_y-wing_depth/2
join = ix/2
tl = max(xl+outer_r, -join-transition)
tr = min(xr-outer_r, join+transition)
front_join = join  # mirrored upper/lower transitions about center_y
k = 0.5522847498  # cubic circle approximation coefficient, not a dimension
# A single closed outline and a single extrusion form the entire load-bearing floor.
with BuildSketch() as floor_profile:
    with BuildLine():
        Line((-join,hinge_y),(join,hinge_y))
        Bezier((join,hinge_y),(join+(tr-join)*0.5,hinge_y),(tr-(tr-join)*0.5,yt),(tr,yt))
        Line((tr,yt),(xr-outer_r,yt))
        Bezier((xr-outer_r,yt),(xr-outer_r+k*outer_r,yt),(xr,yt-outer_r+k*outer_r),(xr,yt-outer_r))
        Line((xr,yt-outer_r),(xr,yb+outer_r))
        Bezier((xr,yb+outer_r),(xr,yb+outer_r-k*outer_r),(xr-outer_r+k*outer_r,yb),(xr-outer_r,yb))
        Line((xr-outer_r,yb),(tr,yb))
        Bezier((tr,yb),((tr+front_join)/2,yb),((tr+front_join)/2,front_y),(front_join,front_y))
        Line((front_join,front_y),(-front_join,front_y))
        Bezier((-front_join,front_y),((tl-front_join)/2,front_y),((tl-front_join)/2,yb),(tl,yb))
        Line((tl,yb),(xl+outer_r,yb))
        Bezier((xl+outer_r,yb),(xl+outer_r-k*outer_r,yb),(xl,yb+outer_r-k*outer_r),(xl,yb+outer_r))
        Line((xl,yb+outer_r),(xl,yt-outer_r))
        Bezier((xl,yt-outer_r),(xl,yt-outer_r+k*outer_r),(xl+outer_r-k*outer_r,yt),(xl+outer_r,yt))
        Line((xl+outer_r,yt),(tl,yt))
        Bezier((tl,yt),((tl-join)/2,yt),((tl-join)/2,hinge_y),(-join,hinge_y))
    make_face()
s = Pos(0,0,-base)*extrude(floor_profile.sketch,amount=base)
# Three-sided low phone wall rises from the common floor; no wall spans the hinge.
rim=extrude(RectangleRounded(ox,oy,corner),amount=rise)
rim=rim-extrude(RectangleRounded(ix,iy,max(corner-wall,0.5)),amount=rise+1)
rim=rim-Pos(0,hinge_y+oy/2,rise/2)*Box(ox+2,oy,rise+2)
s=s+rim

# Closed side cavities are part of the base, not skirts on the detachable lids.
housing_h=param("rear_shell_wing_wall_height",8.6)
rail_allowance=param("rear_shell_wing_rail_allowance",0.2)
support_inset=param("rear_shell_cover_support_inset",12.0)
support_depth=param("rear_shell_cover_support_depth",6.0)
tape_w=param("rear_shell_cover_tape_width",12.0)
tape_l=param("rear_shell_cover_tape_length",4.0)
tape_d=param("rear_shell_cover_tape_depth",0.3)
port_h=param("rear_shell_port_tunnel_height",4.2)
port_z=param("rear_shell_port_tunnel_z",2.3)
key_h=param("rear_shell_output_tunnel_height",3.6)
key_z=param("rear_shell_output_tunnel_z",3.1)

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

for sign, extension in [(-1,left),(1,right)]:
    wing_w=extension+wall-rail_allowance
    wc=sign*(join+wing_w/2)
    outline=wing_profile(wing_w,wing_depth,hinge_y-front_y,transition,outer_r)
    if sign<0:
        outline=Rot(0,0,180)*outline
    outer=Pos(wc,center_y,0)*extrude(outline,amount=housing_h)
    inner=wing_profile(wing_w-2*wall,wing_depth-2*wall,hinge_y-front_y-2*wall,transition,outer_r)
    if sign<0:
        inner=Rot(0,0,180)*inner
    chamber=outer-Pos(wc,center_y,0)*extrude(inner,amount=housing_h+1)
    for end in [-1,1]:
        sy=center_y+end*(wing_depth/2-support_inset)
        chamber+=outer & (Pos(wc,sy,housing_h/2)*Box(wing_w,support_depth,housing_h))
        chamber-=Pos(wc,sy,housing_h-tape_d/2)*Box(tape_w,tape_l,tape_d)
    s+=chamber

# Photo 2 supplies corner location/orientation only; cutout dimensions are tunable defaults.
camera = Pos(camx,camy,-base-1)*extrude(RectangleRounded(camw,camh,camw/2-0.1),amount=base+rise+2)
s=s-camera
s=s-Pos(-join,porty,port_z)*Box(wall*3,portw,port_h)
for yy in [-key_pitch/2,key_pitch/2]:
    s=s-Pos(join+wall/2,yy,key_z)*Box(wall*3,keyslot,key_h)
    for sign in [-1,1]:
        s=s+Pos(key_x,yy+sign*stop_span/2,stop_z/2)*Box(stop_w,stop_depth,stop_z)
s.color=Color(0.16,0.19,0.23)
publish("rear_shell",s,"半包后盖承力壳",material="petg")
assert len(s.solids()) == 1
