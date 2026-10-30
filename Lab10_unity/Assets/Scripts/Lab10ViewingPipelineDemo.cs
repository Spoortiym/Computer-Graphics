using UnityEngine;

// Experiment 10: Demonstrates the 3D viewing pipeline in Unity:
// model/world placement, camera view, perspective/orthographic projection,
// and viewport mapping to a portion of the screen.
public class Lab10ViewingPipelineDemo : MonoBehaviour
{
    public enum ProjectionMode { Perspective, Orthographic }
    public ProjectionMode projection = ProjectionMode.Perspective;

    [Header("Camera / projection")]
    [Range(20f, 100f)] public float fieldOfView = 60f;
    [Range(2f, 15f)] public float orthographicSize = 4f;
    [Header("Viewport mapping (normalized 0..1)")]
    [Range(0f, 0.8f)] public float viewportX = 0f;
    [Range(0f, 0.8f)] public float viewportY = 0f;
    [Range(0.2f, 1f)] public float viewportWidth = 1f;
    [Range(0.2f, 1f)] public float viewportHeight = 1f;
    public bool rotateObject = true;

    private Camera demoCamera;
    private Transform demoObject;

    void Start()
    {
        // Create a visible 3D object if one is not already assigned.
        GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        cube.name = "ViewingPipeline_Cube";
        cube.transform.position = Vector3.zero;
        cube.transform.localScale = new Vector3(1.5f, 1.5f, 1.5f);
        Renderer renderer = cube.GetComponent<Renderer>();
        renderer.material.color = new Color(0.2f, 0.75f, 1f);
        demoObject = cube.transform;

        GameObject cameraObject = new GameObject("ViewingPipeline_Camera");
        demoCamera = cameraObject.AddComponent<Camera>();
        cameraObject.transform.position = new Vector3(3f, 2.5f, -6f);
        cameraObject.transform.LookAt(Vector3.zero);
        demoCamera.clearFlags = CameraClearFlags.SolidColor;
        demoCamera.backgroundColor = new Color(0.08f, 0.1f, 0.15f);
        demoCamera.nearClipPlane = 0.1f;
        demoCamera.farClipPlane = 100f;
        ApplyCameraSettings();
    }

    void Update()
    {
        if (demoCamera != null) ApplyCameraSettings();
        if (rotateObject && demoObject != null)
            demoObject.Rotate(20f * Time.deltaTime, 30f * Time.deltaTime, 10f * Time.deltaTime);
    }

    void OnValidate()
    {
        if (Application.isPlaying && demoCamera != null) ApplyCameraSettings();
    }

    void ApplyCameraSettings()
    {
        demoCamera.orthographic = projection == ProjectionMode.Orthographic;
        if (demoCamera.orthographic) demoCamera.orthographicSize = orthographicSize;
        else demoCamera.fieldOfView = fieldOfView;

        // Unity viewport rect uses normalized coordinates (x, y, width, height).
        float w = Mathf.Clamp(viewportWidth, 0.2f, 1f - viewportX);
        float h = Mathf.Clamp(viewportHeight, 0.2f, 1f - viewportY);
        demoCamera.rect = new Rect(viewportX, viewportY, w, h);
    }

    void OnGUI()
    {
        GUI.color = Color.white;
        GUI.Label(new Rect(12, 12, 520, 26), "LAB 10: 3D VIEWING PIPELINE");
        GUI.Label(new Rect(12, 36, 650, 24), "Projection: " + projection + " | Viewport: normalized screen rectangle");
        GUI.Label(new Rect(12, 60, 700, 24), "Select this GameObject in the Inspector during Play to change projection and viewport.");
    }

    void OnDestroy()
    {
        if (demoCamera != null) Destroy(demoCamera.gameObject);
        if (demoObject != null) Destroy(demoObject.gameObject);
    }
}
