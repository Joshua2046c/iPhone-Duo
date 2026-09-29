"""Read-only measurement of the user's STL; no CAD source or geometry is written.
Run from the project root with numpy, trimesh, and matplotlib installed.
STL has no units: millimetres are an explicit interpretation, not file metadata.
"""
from pathlib import Path
import hashlib, json, struct
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SOURCE = Path('product/references/uploads/20260929T041741902Z-1-joycon-phone-grip.stl')
OUT = Path('product/references/joycon-rail-reference')
raw = SOURCE.read_bytes()
mesh = trimesh.load(SOURCE, force='mesh')
components = sorted(mesh.split(only_watertight=False), key=lambda c: len(c.faces), reverse=True)
body = components[0]
tri, normals = body.triangles, body.face_normals
patches = {}
for side in ['left', 'right']:
    mask = np.all(tri[:, :, 0] < 38.01, axis=1) if side == 'left' else np.all(tri[:, :, 0] > 175.99, axis=1)
    records = []
    for axis in range(3):
        ids = np.where(mask & (np.abs(normals[:, axis]) > .99999))[0]
        groups = {}
        for j in ids:
            groups.setdefault(round(float(tri[j, :, axis].mean()), 3), []).append(j)
        for coordinate, ids in sorted(groups.items()):
            area = float(body.area_faces[ids].sum())
            if area <= .1:
                continue
            points = tri[ids].reshape(-1, 3)
            records.append(dict(axis='xyz'[axis], coordinate=coordinate, area=area,
                                bounds=[points.min(0).tolist(), points.max(0).tolist()]))
    patches[side] = records

result = {
    'source_file': str(SOURCE), 'source_sha256': hashlib.sha256(raw).hexdigest(),
    'format': 'binary STL', 'unit': {'value': 'mm', 'source': 'default', 'note': 'STL does not encode units; no rescaling applied.'},
    'triangle_count': int(struct.unpack('<I', raw[80:84])[0]),
    'watertight': bool(mesh.is_watertight),
    'components': [dict(faces=len(c.faces), bounds=c.bounds.tolist()) for c in components],
    'reference_scope': 'Only the two exterior Joy-Con channels. Phone frame, central plates and rail spacing are excluded from adoption.',
    'axes': {'u': 'inward from rail exterior plane: left X-35; right 179-X', 'v': 'source Y; entry at high Y, closed stop at Y=79.7', 'z': 'source Z, bottom=0'},
    'planar_patch_evidence': patches,
    'reference_dimensions': {
        'rail_outer_z_range': [0, 14], 'channel_z_range': [2, 12],
        'mouth_z_range': [3.2, 10.8], 'channel_height': 10,
        'mouth_height': 7.6, 'groove_back_depth_from_exterior': 2.9,
        'lip_thickness_inward': .7, 'undercut_depth_behind_lip': 2.2,
        'lip_projection_each_z': 1.2, 'top_bottom_material_thickness': 2,
        'body_y_range': [69.6, 170.4], 'body_y_span': 100.8,
        'closed_stop_y': 79.7, 'stop_offset_from_outer_end': 10.1,
        'paired_lip_notches_y': [156.1, 161.1], 'notch_length': 5,
        'notch_center_y': 158.6, 'notch_center_from_stop': 78.9,
        'notch_depth_in_z_each': 1.2, 'notch_depth_inward': .7,
        'groove_back_end_y_measured': 169.6319,
        'groove_back_length_measured': 89.9319,
        'nominal_longitudinal_center_y': 120,
        'closed_stop_relative_center': -40.3,
        'notch_center_relative_center': 38.6
    },
    'regular_channel_void_cross_section_u_z': [[0,3.2],[.7,3.2],[.7,2],[2.9,2],[2.9,12],[.7,12],[.7,10.8],[0,10.8]],
    'accuracy_note': 'Planar dimensions rounded to 0.1 mm from STL planes; curved endpoint rounded to 0.0001 coordinate unit, which is mesh precision, not fit accuracy. Underlying analytic fillet radii and manufacturing tolerances are unavailable.',
    'notch_function': 'Likely a latch/relief feature from geometry; not proven by supplied mesh.',
    'fit_verified': False,
    'applied_to_current_cad': False
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT/'measurements.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
fig, axs = plt.subplots(2, 2, figsize=(13, 7), gridspec_kw={'height_ratios':[2,1]})
for ax, y in zip(axs[0], [120, 158.6]):
    segs = trimesh.intersections.mesh_plane(body, [0,1,0], [0,y,0])
    for seg in segs:
        if np.any(seg[:,0] < 41):
            ax.plot(seg[:,0]-35, seg[:,2], color='#156b91', lw=1.4)
    ax.set(xlim=(-.5,5), ylim=(-.5,14.5), xlabel='u: inward from outer face (assumed mm)', ylabel='Z (assumed mm)', title=f'Left rail cross-section, source Y={y}')
    ax.set_aspect('equal'); ax.grid(alpha=.25)
for ax, x in zip(axs[1], [35.35,36.5]):
    segs = trimesh.intersections.mesh_plane(body,[1,0,0],[x,0,0])
    for seg in segs:
        ax.plot(seg[:,1]-120, seg[:,2], color='#156b91', lw=1.2)
    ax.set(xlim=(-52,52), ylim=(-1,15), xlabel='Y relative to 120 (assumed mm)', ylabel='Z', title=f'Longitudinal section, depth u={x-35:.2f}')
    ax.set_aspect('equal'); ax.grid(alpha=.25)
fig.suptitle('User-supplied STL: rail evidence only; no fit certification')
fig.tight_layout(); fig.savefig(OUT/'rail-sections.png',dpi=180)
print('Measured', result['triangle_count'], 'triangles; source SHA256', result['source_sha256'])
