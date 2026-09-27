
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
rail=extrude(RectangleRounded(w,length,rounding),amount=height)
side=-1
run=length-stop+1
cy=stop/2+0.5
cx=side*(w/2-lip-channel_d/2)
rail=rail-Pos(cx,cy,channel_z)*Box(channel_d,run,channel_h)
rail=rail-Pos(side*(w/2-lip/2+0.1),cy,channel_z)*Box(lip+0.3,run,mouth_h)
rail=rail-Pos(side*(w/2-channel_d/2),length/2-entry/2+0.1,channel_z)*Box(channel_d+0.2,entry+0.2,channel_h)
rail=rail-Pos(side*(w/2-lip-channel_d-latch_depth/2+0.1),latch_y,channel_z)*Box(latch_depth+0.2,latch_len,channel_h/2)
rail.color=Color(0.20,0.30,0.38)
publish("left_rail",rail,"左侧槽形滑轨",material="petg")
fit("left_rail","rear_shell",kind="fused",reason="Custom rail root is fused into the wing edge for a single printed shell.")
assert len(rail.solids())==1
