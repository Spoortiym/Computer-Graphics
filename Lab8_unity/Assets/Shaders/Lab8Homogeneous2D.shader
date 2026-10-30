Shader "Custom/Lab8Homogeneous2D"
{
    Properties
    {
        _Tint ("Tint", Color) = (0.2, 0.75, 1, 1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue"="Geometry" }
        Pass
        {
            Cull Off
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            fixed4 _Tint;
            float4x4 _TransformMatrix;

            struct appdata { float4 vertex : POSITION; };
            struct v2f { float4 position : SV_POSITION; };

            v2f vert(appdata v)
            {
                v2f o;
                // Apply a homogeneous 4x4 matrix to the 2D vertex (z=0, w=1).
                float4 transformed = mul(_TransformMatrix, float4(v.vertex.xy, 0.0, 1.0));
                o.position = UnityObjectToClipPos(transformed);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target { return _Tint; }
            ENDHLSL
        }
    }
}
