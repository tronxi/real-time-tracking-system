import trimesh
import pyglet
from pyglet.gl import *
import numpy as np
import json
from ctypes import POINTER, c_float

with open('attitude.jsonl') as f:
    attitudes = [json.loads(l)['payload'] for l in f]

def get_rotation_matrix(roll, pitch, yaw):
    r, p, y = np.radians([roll, pitch, yaw])
    Rx = np.array([[1, 0, 0], [0, np.cos(r), -np.sin(r)], [0, np.sin(r), np.cos(r)]])
    Ry = np.array([[np.cos(p), 0, np.sin(p)], [0, 1, 0], [-np.sin(p), 0, np.cos(p)]])
    Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

scene = trimesh.load('cube.glb')
mesh = scene.dump(concatenate=True)
vertices = mesh.vertices - mesh.center_mass
faces = mesh.faces
normals = mesh.vertex_normals
colors = mesh.visual.vertex_colors[:, :3] / 255.0 if hasattr(mesh.visual, 'vertex_colors') else None

window = pyglet.window.Window(width=800, height=600, caption='3D Attitude Viewer')
frame = 0

@window.event
def on_draw():
    global frame
    window.clear()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_pos = (GLfloat * 4)(5, 5, 10, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    # Cámara
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, window.width / window.height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    att = attitudes[frame % len(attitudes)]
    R = get_rotation_matrix(att['roll'], att['pitch'], att['yaw'])
    M = np.eye(4)
    M[:3, :3] = R
    M = M.T.astype(np.float32).flatten()
    glMultMatrixf(M.ctypes.data_as(POINTER(c_float)))

    glBegin(GL_TRIANGLES)
    for face in faces:
        for idx in face:
            if normals is not None:
                glNormal3f(*normals[idx])
            if colors is not None:
                glColor3f(*colors[idx])
            else:
                glColor3f(0.6, 0.7, 0.9)
            glVertex3f(*vertices[idx])
    glEnd()

@window.event
def on_key_press(symbol, modifiers):
    global frame
    if symbol == pyglet.window.key.SPACE:
        frame += 1

pyglet.app.run()
