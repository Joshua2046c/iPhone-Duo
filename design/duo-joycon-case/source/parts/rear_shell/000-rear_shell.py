
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
camw = param("rear_shell_camera_width", 24.0)
camh = param("rear_shell_camera_length", 62.0)
camx = param("rear_shell_camera_x", 38.0)
camy = param("rear_shell_camera_y", 0.0)
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
# Rounded rear tray, open at the hinge and never wrapped over the inner display.
s = extrude(RectangleRounded(ox,oy,corner), amount=base+rise)
s = Pos(0,0,-base)*s
cavity = Pos(0,0,0)*extrude(RectangleRounded(ix,iy,max(corner-wall,0.5)),amount=rise+1)
s = s-cavity
hinge_y = PHONE_HALF_Y/2-setback
s = s-Pos(0,hinge_y+oy/2,0)*Box(ox+2,oy,30)
# Solid blank/control wings carry the rails without bridging the folding half.
lwing=Pos(-ox/2-left/2+0.2,0,-base)*extrude(RectangleRounded(left+0.4,wing_depth,3),amount=base)
rwing=Pos(ox/2+right/2-0.2,0,-base)*extrude(RectangleRounded(right+0.4,wing_depth,3),amount=base)
s=s+lwing+rwing
camera = Pos(camx,camy,-base-1)*extrude(RectangleRounded(camw,camh,camw/2-0.1),amount=base+rise+2)
s=s-camera
s=s-Pos(-ox/2,porty,rise/2)*Box(wall*3,portw,rise+0.2)
for yy in [-key_pitch/2,key_pitch/2]:
    s=s-Pos(ox/2-wall/2,yy,rise/2)*Box(wall*3,keyslot,rise+0.2)
    for sign in [-1,1]:
        s=s+Pos(key_x,yy+sign*stop_span/2,stop_z/2)*Box(stop_w,stop_depth,stop_z)
s.color=Color(0.16,0.19,0.23)
publish("rear_shell",s,"半包后盖承力壳",material="petg")
assert len(s.solids()) == 1
