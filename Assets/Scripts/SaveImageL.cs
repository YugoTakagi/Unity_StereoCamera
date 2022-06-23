using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SaveImageL : MonoBehaviour
{
    public Camera camera;
    // public Camera camera = gameObject.GetComponent<Camera>();
    

    // Start is called before the first frame update
    void Start()
    {
        camera.pixelRect = new Rect(0, 0, 640, 480);
        // float height = 2f * camera.orthographicSize;
        // float width = height * camera.aspect;
        print("height: " + camera.pixelHeight + "[pixcel]");
        print("width: " + camera.pixelWidth + "[pixcel]");
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
