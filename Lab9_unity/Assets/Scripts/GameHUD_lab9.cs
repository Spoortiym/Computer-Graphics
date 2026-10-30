using UnityEngine;

public class GameHUD_lab9 : MonoBehaviour
{
    public int totalCollectibles = 5;
    private int score;
    private GUIStyle titleStyle;
    private GUIStyle textStyle;
    private GUIStyle completeStyle;

    public void AddScore(int amount) => score += amount;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape)) Application.Quit();
    }

    void OnGUI()
    {
        EnsureStyles();
        GUI.Box(new Rect(20f, 20f, 370f, 164f), GUIContent.none);
        GUI.Label(new Rect(38f, 30f, 340f, 32f), "NEON RELAY", titleStyle);
        GUI.Label(new Rect(38f, 66f, 340f, 24f), "WASD / Arrows  Move     Space  Jump", textStyle);
        GUI.Label(new Rect(38f, 92f, 340f, 24f), "R  Restart     Esc  Quit Build", textStyle);
        GUI.Label(new Rect(38f, 124f, 340f, 28f), $"ENERGY CELLS     {score} / {totalCollectibles}", textStyle);

        if (score >= totalCollectibles)
            GUI.Label(new Rect(Screen.width * 0.5f - 220f, 40f, 440f, 60f), "RELAY COMPLETE!", completeStyle);
    }

    void EnsureStyles()
    {
        if (titleStyle != null) return;
        titleStyle = new GUIStyle(GUI.skin.label)
        {
            fontSize = 22,
            fontStyle = FontStyle.Bold,
            normal = { textColor = Color.white }
        };
        textStyle = new GUIStyle(GUI.skin.label)
        {
            fontSize = 13,
            normal = { textColor = new Color(0.9f, 0.94f, 1f) }
        };
        completeStyle = new GUIStyle(GUI.skin.label)
        {
            fontSize = 26,
            fontStyle = FontStyle.Bold,
            alignment = TextAnchor.MiddleCenter,
            normal = { textColor = new Color(1f, 0.85f, 0.25f) }
        };
    }
}
