import os
import sys
import numpy as np
import open3d as o3d

# ————— Pfad‐Hack, damit a42_proto und Blickfeld-Protos gefunden werden —————
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
# —————————————————————————————————————————————————————————

from a42_proto.frame_pb2 import Frame as AggFrame
from blickfeld.data.frame_pb2 import Frame as ProtoFrame

# Einfacher Pfad zur Frame-Datei (ändere hier nach Bedarf)
FRAME_FILE = r"C:\Users\abaum\Downloads\frame_0002.pb"


def load_agg_frame(path: str) -> AggFrame:
    agg = AggFrame()
    with open(path, "rb") as f:
        agg.ParseFromString(f.read())
    return agg


def unpack_packed(pf: ProtoFrame) -> np.ndarray:
    """Entpackt pf.packed.cartesian (Big-Endian Float32) zu einem Nx3-Array."""
    cnt = pf.packed.length
    pts = np.frombuffer(pf.packed.cartesian, dtype=">f4")
    return pts.reshape(cnt, 3)


def matrix_from_list(mat_list):
    """Wandelt eine 16-Element-Liste (row-major) in eine 4×4 numpy-Matrix."""
    M = np.array(mat_list, dtype=np.float64)
    return M.reshape(4, 4)


def visualize_global_pointcloud(all_pts: np.ndarray):
    """Visualisiert alle Punkte in globalen Koordinaten."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(all_pts)
    o3d.visualization.draw_geometries([pcd])


def main():
    # 1) Frame laden
    frame_path = FRAME_FILE
    if not os.path.isfile(frame_path):
        print(f"Datei nicht gefunden: {frame_path}")
        sys.exit(1)

    print(f"Lade Frame: {frame_path}")
    agg = load_agg_frame(frame_path)

    # 2) Punkte aus allen Lasern transformieren
    all_pts = []
    for i, laser in enumerate(agg.lasers):
        pf = ProtoFrame()
        pf.CopyFrom(laser.data)
        pts = unpack_packed(pf)  # Nx3 in Sensor-Koordsystem

        if laser.HasField("calibration") and laser.calibration.extrinsic.matrix:
            M = matrix_from_list(laser.calibration.extrinsic.matrix)
        else:
            print(f"▶ Laser #{i}: keine Extrinsic, nehme Identity.")
            M = np.eye(4, dtype=np.float64)

        homo = np.hstack([pts, np.ones((pts.shape[0], 1), dtype=np.float64)])  # Nx4
        global_pts = (M @ homo.T).T[:, :3]
        print(f"▶ Laser #{i} verwandelt {pts.shape[0]} Punkte ins globale Koordinatensystem")
        all_pts.append(global_pts)

    if not all_pts:
        print("❌ Keine Laser-Daten gefunden.")
        return

    all_pts = np.vstack(all_pts)
    print(f"Gesamtpunktwolke: {all_pts.shape[0]} Punkte")

    # 3) Visualisieren
    visualize_global_pointcloud(all_pts)


if __name__ == "__main__":
    main()
