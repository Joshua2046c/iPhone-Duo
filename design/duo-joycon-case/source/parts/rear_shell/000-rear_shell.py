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
back_bevel=param("rear_shell_back_chamfer",0.6)
edge_bevel=param("rear_shell_outer_chamfer",0.3)
front_bevel=param("rear_shell_front_chamfer",0.4)
s = Pos(0,0,-base)*extrude(floor_profile.sketch,amount=base)
# Only the outside wire of the rear face is beveled, before any interior or rail exists.
s=chamfer(s.faces().sort_by(Axis.Z)[0].outer_wire().edges(),length=back_bevel)
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
socket_w=param("rear_shell_cover_socket_width",4.4)
socket_d=param("rear_shell_cover_socket_depth",8.4)
socket_relief=param("rear_shell_socket_retention_relief",0.4)
capture_h=param("rear_shell_socket_capture_height",2.2)
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
    # Chamfer the outside end shoulders only, never the phone-facing or rail-side long edge.
    shoulders=[e for e in outer.edges() if all(abs(v.Z-housing_h)<1e-5 for v in e.vertices()) and abs(e.center().Y-center_y)>(hinge_y-front_y)/2-1e-5]
    assert len(shoulders)>0
    outer=chamfer(shoulders,length=edge_bevel)
    # End voids and tape recesses are replaced by solid square-socket lands.
    pocket_l=wing_depth-2*support_inset-support_depth
    inner=RectangleRounded(wing_w-2*wall,pocket_l,outer_r)
    chamber=outer-Pos(wc,center_y,0)*extrude(inner,amount=housing_h+1)
    for end in [-1,1]:
        sy=center_y+end*(wing_depth/2-support_inset)
        chamber-=Pos(wc,sy,housing_h-socket_d/2)*Box(socket_w,socket_w,socket_d)
        chamber-=Pos(wc,sy,housing_h-socket_d+capture_h/2)*Box(socket_w+2*socket_relief,socket_w,capture_h)
    s+=chamber

# Fill the exterior triangular junctions without entering the phone keep-out.
phone_keepout=extrude(RectangleRounded(ix,iy,max(corner-wall,0.5)),amount=rise+1)
for sign in [-1,1]:
    corner_zone=Pos(sign*(ox/2-corner/2),front_y+corner/2,rise/2)*Box(corner,corner,rise)
    bridge=(extrude(floor_profile.sketch,amount=rise) & corner_zone)-phone_keepout
    s+=bridge

# Photo 2 supplies corner location/orientation only; cutout dimensions are tunable defaults.
camera = Pos(camx,camy,-base-1)*extrude(RectangleRounded(camw,camh,camw/2-0.1),amount=base+rise+2)
s=s-camera
s=s-Pos(-join,porty,port_z)*Box(wall*3,portw,port_h)
for yy in [-key_pitch/2,key_pitch/2]:
    s=s-Pos(join+wall/2,yy,key_z)*Box(wall*3,keyslot,key_h)
    for sign in [-1,1]:
        s=s+Pos(key_x,yy+sign*stop_span/2,stop_z/2)*Box(stop_w,stop_depth,stop_z)

# Integrated left_rail: original channel, entry and latch relief dimensions are preserved.
def make_left_rail():
    w=param("left_rail_width",5.0)
    length=param("left_rail_length",96.0)
    height=param("left_rail_height",10.0)
    rounding=param("left_rail_corner_radius",1.0)
    channel_d=param("left_rail_channel_depth",2.8)
    channel_h=param("left_rail_channel_height",4.6)
    mouth_h=param("left_rail_mouth_height",2.4)
    lip=param("left_rail_lip_thickness",0.7)
    channel_z=param("left_rail_channel_center_z",6.0)
    stop=param("left_rail_bottom_stop",3.0)
    latch_y=param("left_rail_latch_y",-39.0)
    latch_len=param("left_rail_latch_length",3.0)
    latch_depth=param("left_rail_latch_depth",0.6)
    entry=param("left_rail_entry_length",5.0)
    # Custom groove inspired by user's red-box views. These are NOT Nintendo-certified dimensions.
    foundation=param("left_rail_foundation_height",2.4)
    # Rail dimensions retain their original parameter names as features of the unified shell.
    rail=Pos(0,0,foundation)*extrude(RectangleRounded(w,length,rounding),amount=height-foundation)
    side=-1
    # Solid web joins the inner rail corners to the wing wall before cutting the track.
    rail=rail+Pos(-side*w/2,0,(foundation+height)/2)*Box(2*rounding,length,height-foundation)
    run=length-stop+1
    cy=stop/2+0.5
    cx=side*(w/2-lip-channel_d/2)
    rail=rail-Pos(cx,cy,channel_z)*Box(channel_d,run,channel_h)
    rail=rail-Pos(side*(w/2-lip/2+0.1),cy,channel_z)*Box(lip+0.3,run,mouth_h)
    rail=rail-Pos(side*(w/2-channel_d/2),length/2-entry/2+0.1,channel_z)*Box(channel_d+0.2,entry+0.2,channel_h)
    rail=rail-Pos(side*(w/2-lip-channel_d-latch_depth/2+0.1),latch_y,channel_z)*Box(latch_depth+0.2,latch_len,channel_h/2)
    return Pos(xl+w/2,center_y,-foundation)*rail
s=s+make_left_rail()

# Integrated right_rail: original channel, entry and latch relief dimensions are preserved.
def make_right_rail():
    w=param("right_rail_width",5.0)
    length=param("right_rail_length",96.0)
    height=param("right_rail_height",10.0)
    rounding=param("right_rail_corner_radius",1.0)
    channel_d=param("right_rail_channel_depth",2.8)
    channel_h=param("right_rail_channel_height",4.6)
    mouth_h=param("right_rail_mouth_height",2.4)
    lip=param("right_rail_lip_thickness",0.7)
    channel_z=param("right_rail_channel_center_z",6.0)
    stop=param("right_rail_bottom_stop",3.0)
    latch_y=param("right_rail_latch_y",-39.0)
    latch_len=param("right_rail_latch_length",3.0)
    latch_depth=param("right_rail_latch_depth",0.6)
    entry=param("right_rail_entry_length",5.0)
    # Custom groove inspired by user's red-box views. These are NOT Nintendo-certified dimensions.
    foundation=param("right_rail_foundation_height",2.4)
    # Rail dimensions retain their original parameter names as features of the unified shell.
    rail=Pos(0,0,foundation)*extrude(RectangleRounded(w,length,rounding),amount=height-foundation)
    side=1
    # Solid web joins the inner rail corners to the wing wall before cutting the track.
    rail=rail+Pos(-side*w/2,0,(foundation+height)/2)*Box(2*rounding,length,height-foundation)
    run=length-stop+1
    cy=stop/2+0.5
    cx=side*(w/2-lip-channel_d/2)
    rail=rail-Pos(cx,cy,channel_z)*Box(channel_d,run,channel_h)
    rail=rail-Pos(side*(w/2-lip/2+0.1),cy,channel_z)*Box(lip+0.3,run,mouth_h)
    rail=rail-Pos(side*(w/2-channel_d/2),length/2-entry/2+0.1,channel_z)*Box(channel_d+0.2,entry+0.2,channel_h)
    rail=rail-Pos(side*(w/2-lip-channel_d-latch_depth/2+0.1),latch_y,channel_z)*Box(latch_depth+0.2,latch_len,channel_h/2)
    return Pos(xr-w/2,center_y,-foundation)*rail
s=s+make_right_rail()

s=s.clean()
# The front exterior rim edge is outside the phone contact faces; rails are excluded by Z/Y.
front_edges=[e for e in s.edges() if all(abs(v.Z-rise)<1e-5 and abs(v.Y-front_y)<1e-5 for v in e.vertices()) and e.length>wall]
assert len(front_edges)>0
s=chamfer(front_edges,length=front_bevel)
assert len(s.solids()) == 1, "Rails and lower housing must be one connected solid"
s.color=Color(0.16,0.19,0.23)
publish("rear_shell",s,"滑轨一体下壳",material="petg")
