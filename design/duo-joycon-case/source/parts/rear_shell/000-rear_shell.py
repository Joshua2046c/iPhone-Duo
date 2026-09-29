# cell: rear_shell
# cell: rear_shell
# cell: rear_shell
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
back_bevel=param("rear_shell_back_chamfer",0.6)
edge_bevel=param("rear_shell_outer_chamfer",0.3)
front_bevel=param("rear_shell_front_chamfer",0.4)
s = Pos(0,0,-base)*extrude(floor_profile.sketch,amount=base)
# Only the outside wire of the rear face is beveled, before any interior or rail exists.
s=chamfer(s.faces().sort_by(Axis.Z)[0].outer_wire().edges(),length=back_bevel)
# Rear-photo outline: the two outer corners are round; hinge-side corners stay square.
# Source: user image 20260929T115547271Z-1; radii remain photo-based defaults.
def phone_outline(width,depth,r):
    a=-width/2
    b=width/2
    f=-depth/2
    h=depth/2
    with BuildSketch() as profile:
        with BuildLine():
            Polyline((a,h),(b,h),(b,f+r))
            CenterArc((b-r,f+r),r,0,-90)
            Line((b-r,f),(a+r,f))
            CenterArc((a+r,f+r),r,-90,-90)
            Line((a,f+r),(a,h))
        make_face()
    return profile.sketch
# Three-sided low phone wall rises from the common floor; no wall spans the hinge.
rim=extrude(phone_outline(ox,oy,corner),amount=rise)
rim=rim-extrude(phone_outline(ix,iy,max(corner-wall,0.5)),amount=rise+1)
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
    outline=Pos(outer_r,0)*wing_profile(wing_w+2*outer_r,wing_depth,hinge_y-front_y,transition,outer_r)
    # The blank extends into the rail replacement band so the end has no plan-view notch.
    if sign<0:
        outline=Rot(0,0,180)*outline
    outer=Pos(wc,center_y,0)*extrude(outline,amount=housing_h)
    # Chamfer the outside end shoulders only, never the phone-facing or rail-side long edge.
    shoulders=[e for e in outer.edges() if all(abs(v.Z-housing_h)<1e-5 for v in e.vertices()) and abs(e.center().Y-center_y)>(hinge_y-front_y)/2-1e-5]
    assert len(shoulders)>0
    if edge_bevel>0:
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
phone_keepout=extrude(phone_outline(ix,iy,max(corner-wall,0.5)),amount=rise+1)
for sign in [-1,1]:
    corner_zone=Pos(sign*(ox/2-corner/2),front_y+corner/2,rise/2)*Box(corner,corner,rise)
    bridge=(extrude(floor_profile.sketch,amount=rise) & corner_zone)-phone_keepout
    s+=bridge

# Camera module position scaled from rear photo; 0.5-1 mm nominal clearance is provisional.
camera = Pos(camx,camy,-base-1)*extrude(SlotOverall(camh,camw,rotation=90),amount=base+rise+2)
s=s-camera
s=s-Pos(-join,porty,port_z)*Box(wall*3,portw,port_h)
# Photo-visible top buttons; independent of the user's front-cap pitch.
output_plus_y=param("rear_shell_output_plus_y",-2.0)
output_minus_y=param("rear_shell_output_minus_y",-15.5)
for yy in [output_plus_y,output_minus_y]:
    s=s-Pos(join+wall/2,yy,key_z)*Box(wall*3,keyslot,key_h)
for yy in [-key_pitch/2,key_pitch/2]:
    for sign in [-1,1]:
        s=s+Pos(key_x,yy+sign*stop_span/2,stop_z/2)*Box(stop_w,stop_depth,stop_z)


# STL reference 1c8aebf06ef5afe978ff12c1fb71b8741c7f7302be65ff041370069c9f929254.
# Local u points inward, v follows sliding direction, z starts on rail bottom.
# Entry boundary sampled from the uploaded mesh, millimetres assumed. Not a standard.
RAIL_ENTRY_SAMPLES = [[0,45.8174],[0.005,45.950453],[0.02,46.098106],[0.05,46.259242],[0.1,46.440397],[0.2,46.688844],[0.35,46.947008],[0.5,47.140131],[0.7,47.336907],[1,47.548992],[1.25,47.673701],[1.5,47.80278],[1.75,47.964278],[2,48.165033],[2.25,48.415849],[2.5,48.742328],[2.7,49.094049],[2.8,49.325257],[2.85,49.465936],[2.9,49.634881],[2.95,49.856649],[2.98,50.0585],[2.995,50.228623],[3,50.4]]
RAIL_ENTRY_RADIAL_SPAN = 3.0
RAIL_ENTRY_Y_START = 45.8174
RAIL_ENTRY_Y_END = 50.4

def reference_rail(w,length,height,rounding,channel_d,channel_h,mouth_h,lip,channel_z,stop,latch_y,latch_len,latch_depth,entry,foundation):
    # Only the mounting web is adapted to the existing wing. The functional void stays 1:1.
    assert w>lip+channel_d and height>channel_h and length>stop
    entry_points=[(u, length/2-entry+(v-RAIL_ENTRY_Y_START)*entry/(RAIL_ENTRY_Y_END-RAIL_ENTRY_Y_START)) for u,v in RAIL_ENTRY_SAMPLES]
    with BuildSketch() as entry_plan:
        with BuildLine():
            Polyline((0,-length/2),entry_points[0])
            Spline(*entry_points)
            Polyline(entry_points[-1],(w,length/2),(w,-length/2),(0,-length/2))
        make_face()
    rail=extrude(entry_plan.sketch,amount=height)
    # Source longitudinal end surfaces: 4 mm round-nosed envelope in YZ.
    envelope=extrude(Plane.YZ*Pos(0,height/2)*RectangleRounded(length,height,rounding),amount=w)
    rail=rail & envelope
    # Join to the original wing only below its lid seat, keeping a 0.2 mm lid side gap.
    web=Pos(w+wall/4-rail_allowance,0,foundation+housing_h/2)*Box(wall/2,wing_depth-2*outer_r,housing_h)
    rail+=web
    v0=-length/2+stop
    run=length-stop+2
    cy=v0+run/2
    void=Pos(lip+channel_d/2,cy,channel_z)*Box(channel_d,run,channel_h)
    void+=Pos((lip-1)/2,cy,channel_z)*Box(lip+1,run,mouth_h)
    # Source has paired lip notches near the entrance, not a blind groove-back pocket.
    void+=Pos((latch_depth-1)/2,latch_y,channel_z)*Box(latch_depth+1,latch_len,channel_h)
    return rail-void,void

def make_left_rail():
    w=param("left_rail_width",5)
    length=param("left_rail_length",100.8)
    height=param("left_rail_height",14)
    rounding=param("left_rail_corner_radius",4)
    channel_d=param("left_rail_channel_depth",2.2)
    channel_h=param("left_rail_channel_height",10)
    mouth_h=param("left_rail_mouth_height",7.6)
    lip=param("left_rail_lip_thickness",0.7)
    channel_z=param("left_rail_channel_center_z",7)
    stop=param("left_rail_bottom_stop",10.1)
    latch_y=param("left_rail_latch_y",38.6)
    latch_len=param("left_rail_latch_length",5)
    latch_depth=param("left_rail_latch_depth",0.7)
    entry=param("left_rail_entry_length",4.5826)
    foundation=param("left_rail_foundation_height",2.4)
    rail,void=reference_rail(w,length,height,rounding,channel_d,channel_h,mouth_h,lip,channel_z,stop,latch_y,latch_len,latch_depth,entry,foundation)
    band=Pos(w/2,0,height/2)*Box(w,2*max(length,wing_depth),height+2*base)
    silhouette=extrude(Plane.YZ*Pos(0,height/2)*RectangleRounded(length,height,rounding),amount=(xr-xl)/2)
    return Pos(xl,center_y,-foundation)*rail,Pos(xl,center_y,-foundation)*void,Pos(xl,center_y,-foundation)*band,Pos(xl,center_y,-foundation)*silhouette
left_rail_body,left_rail_void,left_rail_band,left_silhouette=make_left_rail()
# Cut the functional channel through the existing foundation as well.
s=(s-left_rail_band+left_rail_body)-left_rail_void

def make_right_rail():
    w=param("right_rail_width",5)
    length=param("right_rail_length",100.8)
    height=param("right_rail_height",14)
    rounding=param("right_rail_corner_radius",4)
    channel_d=param("right_rail_channel_depth",2.2)
    channel_h=param("right_rail_channel_height",10)
    mouth_h=param("right_rail_mouth_height",7.6)
    lip=param("right_rail_lip_thickness",0.7)
    channel_z=param("right_rail_channel_center_z",7)
    stop=param("right_rail_bottom_stop",10.1)
    latch_y=param("right_rail_latch_y",38.6)
    latch_len=param("right_rail_latch_length",5)
    latch_depth=param("right_rail_latch_depth",0.7)
    entry=param("right_rail_entry_length",4.5826)
    foundation=param("right_rail_foundation_height",2.4)
    rail,void=reference_rail(w,length,height,rounding,channel_d,channel_h,mouth_h,lip,channel_z,stop,latch_y,latch_len,latch_depth,entry,foundation)
    band=Pos(w/2,0,height/2)*Box(w,2*max(length,wing_depth),height+2*base)
    rail=mirror(rail,about=Plane.YZ)
    void=mirror(void,about=Plane.YZ)
    band=mirror(band,about=Plane.YZ)
    silhouette=extrude(Plane.YZ*Pos(0,height/2)*RectangleRounded(length,height,rounding),amount=(xr-xl)/2)
    silhouette=mirror(silhouette,about=Plane.YZ)
    return Pos(xr,center_y,-foundation)*rail,Pos(xr,center_y,-foundation)*void,Pos(xr,center_y,-foundation)*band,Pos(xr,center_y,-foundation)*silhouette
right_rail_body,right_rail_void,right_rail_band,right_silhouette=make_right_rail()
# Cut the functional channel through the existing foundation as well.
s=(s-right_rail_band+right_rail_body)-right_rail_void

# One shared rail-derived end envelope removes projecting floor and wing corners.
s=s & left_silhouette.fuse(right_silhouette)
s=s.clean()
# The front exterior rim edge is outside the phone contact faces; rails are excluded by Z/Y.
front_edges=[e for e in s.edges() if all(abs(v.Z-rise)<1e-5 and abs(v.Y-front_y)<1e-5 for v in e.vertices()) and e.length>wall]
assert len(front_edges)>0
s=chamfer(front_edges,length=front_bevel)
assert (s & left_rail_void).volume < 1e-6, "Left channel blocked by lower shell"
assert (s & right_rail_void).volume < 1e-6, "Right channel blocked by lower shell"
assert len(s.solids()) == 1, "Rails and lower housing must be one connected solid"
s.color=Color(0.16,0.19,0.23)
publish("rear_shell",s,"滑轨一体下壳",material="petg")
