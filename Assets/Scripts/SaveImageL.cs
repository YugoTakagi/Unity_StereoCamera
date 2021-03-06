using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;

public class SaveImageL : MonoBehaviour
{
    public Camera camera;

    private Texture2D image;
    private Rect      rect;
    // public Camera camera = gameObject.GetComponent<Camera>();
    

    // Start is called before the first frame update
    void Start()
    {
        Vector2 sensorSize = camera.sensorSize;

        camera.focalLength = sensorSize[0] / 2.0f;

        float f = camera.focalLength;
        print("height: " + camera.pixelHeight + "[pixcel]");
        print("width: "  + camera.pixelWidth  + "[pixcel]");
        print("sensor size: " + sensorSize + "[mm]");
        print("f: " + f + "[mm]");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            CaptureImage("testL.png");

            Vector2 sensorSize = camera.sensorSize;
            float f = camera.focalLength;
            print("height: " + camera.pixelHeight + "[pixcel]");
            print("width: "  + camera.pixelWidth  + "[pixcel]");
            print("sensor size: " + sensorSize + "[mm]");
            print("f: " + f + "[mm]");
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
