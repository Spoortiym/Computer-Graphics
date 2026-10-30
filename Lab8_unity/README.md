# Lab8 — 2D Geometric Transformations with Vertex and Fragment Shaders

## Objective
Apply translation, rotation, scaling, reflection and shearing to a 2D object using homogeneous-coordinate matrices in a Unity shader.

## Open in Unity Hub
1. Extract the downloaded ZIP.
2. In Unity Hub, choose **Add** → **Add project from disk**.
3. Select the `Lab8` folder.
4. Open the project, then open the scene or create a new scene.
5. Create an empty GameObject named `Lab8Demo`.
6. Add the `Lab8TransformationDemo` component to it. The script creates the quad automatically.
7. Press **Play**. Select the GameObject and change **Mode** and parameters in the Inspector while playing.

## Included files
- `Assets/Scripts/Lab8TransformationDemo.cs` — builds the quad and sets the transformation matrix.
- `Assets/Shaders/Lab8Homogeneous2D.shader` — vertex and fragment shader.
- `ProjectSettings/ProjectVersion.txt` — Unity editor version marker.

## Transformation matrices
Translation: [[1,0,tx],[0,1,ty],[0,0,1]]
Rotation: [[cosθ,-sinθ,0],[sinθ,cosθ,0],[0,0,1]]
Scaling: [[sx,0,0],[0,sy,0],[0,0,1]]
Reflection: [[±1,0,0],[0,±1,0],[0,0,1]]
Shearing: [[1,shx,0],[shy,1,0],[0,0,1]]

Note: this is a Unity implementation of the lab's vertex/fragment-shader and transformation-matrix concepts, rather than native OpenGL/GLSL.
