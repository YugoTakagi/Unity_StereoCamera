using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class SaveImageR : MonoBehaviour
{
    public Camera camera;

    private Texture2D image;
    private Rect      rect;
    // public Camera camera = gameObject.GetComponent<Camera>();
    

    // Start is called before the first frame update
    void Start()
    {
        // camera.pixelRect = new Rect(0, 0, 640, 480);

        // camera.fieldOfView = 67.9156f; // horizontal Field of view varies is 90.0.
        Vector2 sensorSize = camera.sensorSize;
        camera.focalLength = sensorSize[0] / 2.0f;
        float f = camera.focalLength;
        
        // float height = 2f * camera.orthographicSize;
        // float width = height * camera.aspect;
        float fx = camera.pixelHeight / sensorSize[0];
        float fy = camera.pixelWidth / sensorSize[1];
        print("height: " + camera.pixelHeight + "[pixcel]");
        print("width: " + camera.pixelWidth + "[pixcel]");
        print("f: " + f + "[mm] -> fx: " + fx + "[pixel], fy: " + fx + "[pixel]");
        print("sensor size: " + sensorSize + "[mm]");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            CaptureImage("testR.png");
        }
    }

    private void CaptureImage(string filePath)
    {
        // 画像サイズを設定．
        image = new Texture2D(640, 480, TextureFormat.RGB24, false);
        rect  = new Rect(0, 0, 640, 480);

        var prev = camera.targetTexture;

        // カメラから出力するサイズをheight: 640[pixel]，width: 480[pixel]に設定．
        var rt = new RenderTexture(640, 480, 24);
        camera.targetTexture = rt;
        camera.Render();
        camera.targetTexture = prev;
        RenderTexture.active = rt;

        image.ReadPixels(rect, 0, 0);
        image.Apply();
        var bytes_image = image.EncodeToPNG();
        Destroy(image);
        File.WriteAllBytes(filePath, bytes_image);
    }
}
