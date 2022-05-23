using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Globalization;
using UnityEngine;
using System;

struct vehicle_chars
{
    public Vector3 receivedPos; //position
    public Vector3 Size;  //size
    public string object_catogory; //object type
    public Vector3 rotation; //rotation
}

public class Server : MonoBehaviour
{
    Thread mThread;
    public string connectionIP = "127.0.0.1";
    public int connectionPort = 54955;
    public GameObject spawnee;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;

    //these are the values
    vehicle_chars[] vehicle_array = new vehicle_chars[100];
    int vehicle_arra_size = 0;
    bool clear = false;
    bool running;
    bool data_available = false;

    private void Start()
    {
        //creating a new thread for sockets
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
    }
    void spwan(vehicle_chars annotaion)
    {
        
        GameObject b = Instantiate(spawnee) as GameObject;
        b.transform.position = annotaion.receivedPos;
        b.transform.Rotate(annotaion.rotation);
        b.transform.localScale = annotaion.Size;
    }
    
   void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            CheckFrameEnd();
            if (!running)
            {
                break;
            }
            ReceiveData();
        }
        listener.Stop();
    }
    void Update()
        {
            //print(vehicle_array);
            if (data_available)
            {
            for(int i=1;i<vehicle_arra_size;i++)
            {
                //print(vehicle_array[i].Size);
                print(vehicle_array[i].rotation);
                //print(vehicle_array[i].object_catogory);
                //print(vehicle_array[i].receivedPos);
            }
            //clear env
            if (clear)
                {
                    //clear function here
                     var clones = GameObject.FindGameObjectsWithTag ("clone");
                    foreach (var clone in clones){
                        Destroy(clone);}
                    
                    print("cleared");
                    clear = false;
                }
                if(!running)
                {
                    //exit program or do whatever you like
                    print("finished");
                }

            // you can do your things here
            for (int i = 1; i < vehicle_arra_size; i++)
            {
                spwan(vehicle_array[i]);
            }
      
                //print(object_catogory);
            data_available = false;
            }
        }

    private void CheckFrameEnd()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        //---receiving translation Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string CheckStr = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string
        if(CheckStr == "FRAME")
        {
            clear = true;
        }
        if(CheckStr == "DONE")
        {
            running = false;
        }
    }

    void ReceiveData()
     {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];

        //---receiving translation Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string DataReceived = Encoding.UTF8.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (DataReceived != null)
        {
            string[] annos = DataReceived.Split('$');
            int i;
            for(i=1;i<annos.Length;i++)
            {
                string[] items = annos[i].Split('/');
                vehicle_array[i].Size = StringToVector3(items[0]);
                vehicle_array[i].rotation = StringToVector3(items[1]);
                vehicle_array[i].object_catogory = items[2];
                vehicle_array[i].receivedPos = StringToVector3(items[3]);
            }
            //---Using received data---
            //receivedPos = StringToVector3(TransDataReceived); //<-- assigning receivedPos value from Python
            //print(receivedPos);
            data_available = true;
            vehicle_arra_size = i;
        }
    }

    public static Vector3 StringToVector3(string sVector, bool IsSize=false)
    {
        // Remove the parentheses
        if (sVector.StartsWith("(") && sVector.EndsWith(")"))
        {
            sVector = sVector.Substring(1, sVector.Length - 2);
        }

        // split the items
        string[] sArray = sVector.Split(',');

        Vector3 result;
        if (IsSize)
        {
            result = new Vector3(
            float.Parse("0"),
            float.Parse(sArray[2])+180,
            float.Parse("0"));
        }
        else
        {
            result = new Vector3(
            float.Parse(sArray[0]),
            float.Parse(sArray[2]),
            float.Parse(sArray[1]));
        }

        // store as a Vector3
        

        return result;
    }

    public static Quaternion StringToQuadotrion(string sVector)
    {
        // Remove the parentheses
        if (sVector.StartsWith("(") && sVector.EndsWith(")"))
        {
            sVector = sVector.Substring(1, sVector.Length - 2);
        }

        // split the items
        string[] sArray = sVector.Split(',');

        // store as a Vector3
        Quaternion result = new Quaternion(
            float.Parse(sArray[0], CultureInfo.InvariantCulture.NumberFormat),
            float.Parse(sArray[1], CultureInfo.InvariantCulture.NumberFormat),
            float.Parse(sArray[2], CultureInfo.InvariantCulture.NumberFormat),
            float.Parse(sArray[3], CultureInfo.InvariantCulture.NumberFormat));

        return result;
    }
}
