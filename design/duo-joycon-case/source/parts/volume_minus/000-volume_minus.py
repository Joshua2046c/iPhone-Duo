
foot_w=param("volume_minus_anchor_width",4.0)
foot_span=param("volume_minus_anchor_span",14.0)
foot_t=param("volume_minus_anchor_thickness",1.2)
beam_l=param("volume_minus_flexure_length",8.0)
beam_w=param("volume_minus_flexure_width",2.0)
beam_t=param("volume_minus_flexure_thickness",0.8)
beam_z=param("volume_minus_flexure_height",6.4)
span=param("volume_minus_flexure_spacing",10.0)
arm_l=param("volume_minus_input_arm_length",8.0)
arm_t=param("volume_minus_arm_thickness",2.0)
nose_x=param("volume_minus_contact_x",-4.0)
nose_z=param("volume_minus_contact_height",3.1)
nose_w=param("volume_minus_contact_width",3.0)
nose_t=param("volume_minus_contact_thickness",1.6)
cap_w=param("volume_minus_cap_width",8.0)
cap_l=param("volume_minus_cap_length",10.0)
cap_t=param("volume_minus_cap_thickness",2.0)
embed=param("volume_minus_anchor_embed",0.2)
# Anchor integrates with shell; flexible leaves and nose remain free of the shell.
k=Pos(0,0,foot_t/2-embed)*Box(foot_w,foot_span,foot_t)
for side in [-1,1]:
    k=k+Pos(0,side*span/2,beam_z/2)*Box(beam_w,beam_w,beam_z)
    k=k+Pos(beam_l/2,side*span/2,beam_z+beam_t/2)*Box(beam_l,beam_w,beam_t)
k=k+Pos(beam_l,0,beam_z+arm_t/2)*Box(arm_t,span+beam_w,arm_t)
k=k+Pos(beam_l+arm_l/2,0,beam_z+arm_t/2)*Box(arm_l,2*nose_w,arm_t)
# Downward leg below flexure converts front downstroke to inward nose travel.
leg_h=beam_z+arm_t-nose_z
k=k+Pos(beam_l,0,nose_z+leg_h/2)*Box(arm_t,nose_w,leg_h)
k=k+Pos((nose_x+beam_l)/2,0,nose_z)*Box(beam_l-nose_x,nose_w,nose_t)
cap_x=beam_l+arm_l/2
cap_bottom=beam_z+arm_t
cap=Pos(cap_x,0,cap_bottom)*extrude(RectangleRounded(cap_w,cap_l,min(cap_w,cap_l)/4),amount=cap_t)
k=k+cap
# Raised tactile mark derived from cap size.
k=k+Pos(cap_x,0,cap_bottom+cap_t+beam_t/4)*Box(cap_w*0.6,beam_t,beam_t/2)

k.color=Color(0.12,0.63,0.72)
publish("volume_minus",k,"音量减柔性转向键",material="petg")
fit("volume_minus","rear_shell",kind="fused",reason="The fixed foot joins both the base (0.2 mm) and the tray sidewall (0.8 mm); only this anchor is fused, leaving both flexure leaves and the output arm free.")
assert len(k.solids())==1
