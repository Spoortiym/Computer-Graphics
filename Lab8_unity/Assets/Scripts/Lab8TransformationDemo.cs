using UnityEngine;

// Experiment 8: 2D geometric transformations using homogeneous coordinates.
// Attach this script to an empty GameObject. It creates a quad and applies
// translation, rotation, scaling, reflection, or shearing through a matrix.
[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class Lab8TransformationDemo : MonoBehaviour
{
    public enum TransformMode { Translation, Rotation, Scaling, Reflection, Shearing }
    public TransformMode mode = TransformMode.Rotation;

    [Header("Transformation parameters")]
    public Vector2 translation = new Vector2(0.35f, 0.15f);
    [Range(-180f, 180f)] public float rotationDegrees = 30f;
    public Vector2 scale = new Vector2(1.3f, 0.8f);
    public bool reflectX = true;
    public bool reflectY = false;
    [Range(-2f, 2f)] public float shearX = 0.5f;
    [Range(-2f, 2f)] public float shearY = 0f;

    private Material materialInstance;
    private static readonly int TransformMatrixId = Shader.PropertyToID("_TransformMatrix");
    private static readonly int TintId = Shader.PropertyToID("_Tint");

    void Start()
    {
        Mesh mesh = new Mesh { name = "2D Transformation Quad" };
        mesh.vertices = new Vector3[] {
            new Vector3(-0.5f, -0.5f, 0), new Vector3(0.5f, -0.5f, 0),
            new Vector3(0.5f, 0.5f, 0), new Vector3(-0.5f, 0.5f, 0)
        };
        mesh.triangles = new int[] { 0, 2, 1, 0, 3, 2 };
        mesh.uv = new Vector2[] { Vector2.zero, Vector2.right, Vector2.one, Vector2.up };
        mesh.RecalculateNormals();
        GetComponent<MeshFilter>().sharedMesh = mesh;

        Shader shader = Shader.Find("Custom/Lab8Homogeneous2D");
        if (shader == null) {
            Debug.LogError("Shader Custom/Lab8Homogeneous2D not found. Check Assets/Shaders/Lab8Homogeneous2D.shader.");
            enabled = false; return;
        }
        materialInstance = new Material(shader);
        materialInstance.SetColor(TintId, new Color(0.2f, 0.75f, 1f, 1f));
        GetComponent<MeshRenderer>().material = materialInstance;
        ApplyTransformation();
    }

    void OnValidate()
    {
        if (Application.isPlaying && materialInstance != null) ApplyTransformation();
    }

    void Update()
    {
        if (materialInstance != null) ApplyTransformation();
    }

    void ApplyTransformation()
    {
        Matrix4x4 m = Matrix4x4.identity;
        switch (mode)
        {
            case TransformMode.Translation:
                m = Matrix4x4.Translate(new Vector3(translation.x, translation.y, 0));
                break;
            case TransformMode.Rotation:
                m = Matrix4x4.Rotate(Quaternion.Euler(0, 0, rotationDegrees));
                break;
            case TransformMode.Scaling:
                m = Matrix4x4.Scale(new Vector3(scale.x, scale.y, 1));
                break;
            case TransformMode.Reflection:
                m = Matrix4x4.Scale(new Vector3(reflectX ? -1 : 1, reflectY ? -1 : 1, 1));
                break;
            case TransformMode.Shearing:
                m.m01 = shearX; // x' = x + shearX*y
                m.m10 = shearY; // y' = shearY*x + y
                break;
        }
        materialInstance.SetMatrix(TransformMatrixId, m);
    }

    void OnDestroy()
    {
        if (materialInstance != null) Destroy(materialInstance);
    }
}
