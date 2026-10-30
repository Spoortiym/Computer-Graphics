using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
public static class LabSceneAutoSetup_lab9
{
    private const string SceneFolder = "Assets/Scenes";
    private const string ScenePath = "Assets/Scenes/Lab9_Interactive3DScene.unity";
    private const string MaterialFolder = "Assets/GeneratedMaterials";

    static LabSceneAutoSetup_lab9()
    {
        EditorApplication.delayCall += BuildSceneIfNeeded;
    }

    private static void BuildSceneIfNeeded()
    {
        if (Application.isPlaying) return;
        if (AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath) != null) return;

        EnsureFolder(SceneFolder);
        EnsureFolder(MaterialFolder);
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

        Material groundMat = CreateMaterial("GroundMaterial", new Color(0.035f, 0.055f, 0.12f));
        Material playerMat = CreateMaterial("PlayerMaterial", new Color(0.08f, 0.72f, 1f), 0.35f);
        Material obstacleMat = CreateMaterial("ObstacleMaterial", new Color(0.16f, 0.19f, 0.32f));
        Material accentMat = CreateMaterial("AccentMaterial", new Color(1f, 0.12f, 0.48f), 0.55f);
        Material collectibleMat = CreateMaterial("CollectibleMaterial", new Color(0.12f, 1f, 0.78f), 0.8f);
        Material trimMat = CreateMaterial("NeonTrimMaterial", new Color(0.08f, 0.62f, 1f), 0.7f);

        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.name = "Ground";
        ground.transform.localScale = new Vector3(4f, 1f, 4f);
        SetMaterial(ground, groundMat);

        CreateArenaTrim(trimMat);

        GameObject player = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        player.name = "Player";
        player.transform.position = new Vector3(0f, 1f, -10f);
        Object.DestroyImmediate(player.GetComponent<CapsuleCollider>());
        CharacterController controller = player.AddComponent<CharacterController>();
        controller.height = 2f;
        controller.radius = 0.5f;
        controller.center = Vector3.zero;
        player.AddComponent<PlayerController_lab9>();
        SetMaterial(player, playerMat);

        CreateObstacle("Obstacle_A", new Vector3(-5f, 1f, -2f), new Vector3(3f, 2f, 3f), obstacleMat);
        CreateObstacle("Obstacle_B", new Vector3(4f, 1.5f, 1f), new Vector3(2.5f, 3f, 2.5f), obstacleMat);
        CreateObstacle("Obstacle_C", new Vector3(-2f, 0.75f, 7f), new Vector3(5f, 1.5f, 2f), obstacleMat);
        CreateObstacle("Obstacle_D", new Vector3(8f, 1f, 8f), new Vector3(3f, 2f, 3f), obstacleMat);
        CreateObstacle("Obstacle_E", new Vector3(-9f, 1.25f, 10f), new Vector3(2f, 2.5f, 5f), obstacleMat);

        CreateRotatingCube("RotatingCube_A", new Vector3(7f, 2f, -5f), new Vector3(2f, 2f, 2f), accentMat);
        CreateRotatingCube("RotatingCube_B", new Vector3(-8f, 1.8f, 2f), new Vector3(1.8f, 1.8f, 1.8f), accentMat);

        Vector3[] collectiblePositions =
        {
            new Vector3(-7f, 1.2f, -7f),
            new Vector3(6f, 1.2f, -1f),
            new Vector3(0f, 1.2f, 5f),
            new Vector3(9f, 1.2f, 11f),
            new Vector3(-10f, 1.2f, 13f)
        };
        foreach (Vector3 position in collectiblePositions) CreateCollectible(position, collectibleMat);

        GameObject lightObject = new GameObject("Directional Light");
        Light light = lightObject.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 0.8f;
        light.color = new Color(0.55f, 0.68f, 1f);
        lightObject.transform.rotation = Quaternion.Euler(48f, -32f, 0f);

        RenderSettings.ambientLight = new Color(0.16f, 0.19f, 0.34f);
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.035f, 0.055f, 0.12f);
        RenderSettings.fogDensity = 0.012f;

        GameObject cameraObject = new GameObject("Main Camera");
        cameraObject.tag = "MainCamera";
        Camera camera = cameraObject.AddComponent<Camera>();
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(0.025f, 0.035f, 0.09f);
        camera.fieldOfView = 60f;
        cameraObject.transform.position = player.transform.position + new Vector3(0f, 6f, -8f);
        CameraFollow_lab9 follow = cameraObject.AddComponent<CameraFollow_lab9>();
        follow.target = player.transform;

        GameObject hudObject = new GameObject("GameHUD");
        GameHUD_lab9 hud = hudObject.AddComponent<GameHUD_lab9>();
        hud.totalCollectibles = collectiblePositions.Length;

        GameObject titleObject = new GameObject("SceneTitle");
        TextMesh title = titleObject.AddComponent<TextMesh>();
        title.text = "NEON RELAY";
        title.characterSize = 0.8f;
        title.fontSize = 48;
        title.anchor = TextAnchor.MiddleCenter;
        title.alignment = TextAlignment.Center;
        title.color = Color.white;
        titleObject.transform.position = new Vector3(0f, 4.5f, 14f);
        titleObject.transform.rotation = Quaternion.Euler(0f, 180f, 0f);

        EditorSceneManager.SaveScene(scene, ScenePath);
        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath, true) };
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        Selection.activeGameObject = player;
    }

    private static void CreateObstacle(string name, Vector3 position, Vector3 scale, Material material)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obj.name = name;
        obj.transform.position = position;
        obj.transform.localScale = scale;
        SetMaterial(obj, material);
    }

    private static void CreateRotatingCube(string name, Vector3 position, Vector3 scale, Material material)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obj.name = name;
        obj.transform.position = position;
        obj.transform.localScale = scale;
        obj.AddComponent<RotatingObject_lab9>();
        SetMaterial(obj, material);
    }

    private static void CreateCollectible(Vector3 position, Material material)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        obj.name = "Collectible";
        obj.transform.position = position;
        obj.transform.localScale = Vector3.one * 0.7f;
        SphereCollider collider = obj.GetComponent<SphereCollider>();
        collider.isTrigger = true;
        Rigidbody body = obj.AddComponent<Rigidbody>();
        body.isKinematic = true;
        body.useGravity = false;
        obj.AddComponent<Collectible_lab9>();
        SetMaterial(obj, material);
    }

    private static void CreateArenaTrim(Material material)
    {
        CreateObstacle("NeonTrim_North", new Vector3(0f, 0.12f, 19f), new Vector3(38f, 0.16f, 0.12f), material);
        CreateObstacle("NeonTrim_South", new Vector3(0f, 0.12f, -19f), new Vector3(38f, 0.16f, 0.12f), material);
        CreateObstacle("NeonTrim_East", new Vector3(19f, 0.12f, 0f), new Vector3(0.12f, 0.16f, 38f), material);
        CreateObstacle("NeonTrim_West", new Vector3(-19f, 0.12f, 0f), new Vector3(0.12f, 0.16f, 38f), material);
    }

    private static Material CreateMaterial(string name, Color color, float emission = 0f)
    {
        string path = MaterialFolder + "/" + name + ".mat";
        Material existing = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (existing != null) return existing;
        Shader shader = Shader.Find("Standard");
        if (shader == null) shader = Shader.Find("Universal Render Pipeline/Lit");
        if (shader == null) shader = Shader.Find("Unlit/Color");
        Material material = new Material(shader);
        material.color = color;
        if (emission > 0f && material.HasProperty("_EmissionColor"))
        {
            material.EnableKeyword("_EMISSION");
            material.SetColor("_EmissionColor", color * emission);
        }
        AssetDatabase.CreateAsset(material, path);
        return material;
    }

    private static void SetMaterial(GameObject obj, Material material)
    {
        Renderer renderer = obj.GetComponent<Renderer>();
        if (renderer != null) renderer.sharedMaterial = material;
    }

    private static void EnsureFolder(string path)
    {
        if (AssetDatabase.IsValidFolder(path)) return;
        Directory.CreateDirectory(path);
        AssetDatabase.Refresh();
    }
}
