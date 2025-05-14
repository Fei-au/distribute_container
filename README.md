# Container connection, distribute to multiple vms

## Deploy to aws
1. Backend
   mangus
3. Async task
4. Database
5. Message Queue
6. Proxy
7. CDN
8. Static resources
9. Log
10. Image and container
11. Subnet management
12. User management
13. VM play
    1. EC2, Debian VM
        - deployed container services including django, subscriber, nginx within docker compose
14. Kubernates


## Already deployed on gcp (gcp branch):
1. Backend: gcloud run service
   **gcloud run service** only suitable with http request, the container listen to some port and deal with http request. **Automatic scale**
2. Async task:
     1. using **push** method to do task, which is normal post call to the backend, so using **gcloud run service**, **Automatic scale**
     2. **compute engine** run **pull** method, need scale manully.
3. Database:
   **Redis** as database, using **gcloud MemoryStore**, this one is expensive, change to **redis cloud**, which has free tier
4. Message Queue:
   **Pub/sub**, this is a pub/sub mode, a pub can have many subs. But what we really need is a **task queue**, while pub/sub can do this job as well
   There is free **RabbitMQ cloud service** like cloudamqp, should try those
5. Proxy:
   1. **Load balancing**, as reverse proxy, can **scale automatically**, reverse http api request to backend service (gcloud run service container)
6. CDN
   **CDN** under **load balancing**. When receive request, check if CDN cache hit, then use the cache, if not, pass request to **cloud run**
   The **Networks** in gcloud can also create free ssl key for domains
8. Static resources
   Store **web static file** like html, js, css. And images, files that the server needs
9. Log
   Using **gcloud logging**, which directly capture console message in services.
10. Image and container
   Using **Artificial Registry** for better integration with **cloud run**. Build image locally, tag specific tag, and push to **gcloud repo**
11. **VPC netrworks**
     1. Keep **static ip** for load balacing, so domain's a tag can point to ip address
     2. Create a subnet for services to include load balancer. Cloud run service can set up a bridge to connect with the subnet 
     3. If using cloud database like mysql, we can make it only open access within subnet for security.
     4. If using compute engine, the subnet connection also works very good
11. User management and service management
     1. If having compute engines to manage, we need **IAM & Admin** to create users, and give them specific access to services. So they can only access these services, for better security.
     2. When **create compute engine**, we can make the compute engine to access specific services.
     3. When a service that run on compute engine, needs to access specific cloud service, an access token is needed so the service have access to cloud services.
        Access token is belong to an IAM user, only the user has specific authorities, services started by the user will have same authorities.
     4. cloud run does not need this user management.
12. compute engine
      self managed vm. pull code, run all above serivces on the vm
      1. vm has an cloud user, so it has specific accesses.
      2. vm group is an auto scaled solution, scaled more vms when certain vm cannot do tasks properly or shrink when fewer tasks are there.
         It needs a startup script to run the service from scrach, like from a very clean vm. So the script mainly do env config, libraries download, code pull, service setup.
         And those services running in vm group should be stateless, so if an vm is closed, the data is still safe
13. kubernates 
   
     
