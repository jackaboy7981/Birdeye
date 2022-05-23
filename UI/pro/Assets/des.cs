
using UnityEngine;

public class des : MonoBehaviour
{
    public float lifeTime = 5f;

    // Update is called once per frame
    void Update()
    {
      if(lifeTime>0)
      {
        lifeTime -= Time.deltaTime;
        if(lifeTime <= 0)
        {
          Destruction();  
        }
      }
    }
   void Destruction()
   {
     Destroy(this.gameObject);
   }
}