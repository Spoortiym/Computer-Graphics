# Lab10 — 3D Viewing Pipeline, Projection and Viewport Mapping

## Objective
Demonstrate the 3D viewing pipeline by displaying a 3D object through a camera, comparing perspective and orthographic projection, and changing viewport mapping.

## Open in Unity Hub
1. Extract the downloaded ZIP.
2. In Unity Hub, choose **Add** → **Add project from disk**.
3. Select the `Lab10` folder and open it.
4. Create an empty GameObject named `Lab10Demo`.
5. Attach `Lab10ViewingPipelineDemo.cs` from `Assets/Scripts`.
6. Press **Play**. Select `Lab10Demo` and change Projection, Field Of View / Orthographic Size, and viewport settings in the Inspector.

The script creates a cube and camera at runtime. The cube rotates to make the 3D view easier to observe.

## Pipeline covered
1. **Model/world coordinates:** cube position and rotation.
2. **View transformation:** camera position and `LookAt` orientation.
3. **Projection:** perspective (`fieldOfView`) or orthographic (`orthographicSize`).
4. **Clipping:** near and far clipping planes.
5. **Viewport mapping:** `Camera.rect` uses normalized `(x, y, width, height)` values to map the camera output to a screen region.

## Included files
- `Assets/Scripts/Lab10ViewingPipelineDemo.cs` — creates the 3D object and camera, and exposes projection/viewport settings.
- `ProjectSettings/ProjectVersion.txt` — Unity editor version marker.

Note: this is a Unity implementation of the viewing-pipeline concepts, not a native OpenGL application.
