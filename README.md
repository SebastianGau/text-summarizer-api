# Informatics, Computing, Digital - Seminar for Patent Attorneys

This repository contains code and tutorial examples to demonstrate patent attorneys which technologies are the back bone of digitalization today. In this seminar, we will develop a REST application programmer interface (API) that is capable of summarizing text, e.g. patent text, to a specified length.

## The Basics - What is a REST API and why developers use REST APIs

**ToDo by Robert - currently proposal from Sebastian**

A REST API can be used to exchange data between two computer systems:

![Rest-API.png](docs/Rest-API.png)

- **Stateless client/server protocol**: Each HTTP contains all the necessary information to run it, which means that neither the client nor the server need to remember any previous state to satisfy it. Be that as it may, some HTTP applications incorporate a cache memory. This configures what is known as the stateless client-cache-server protocol: it is possible to define some of the responses to specific HTTP requests as cachable, so the client can run the same response for identical requests in the future. However, the fact that the option exists doesn't mean it is the most recommended.
- **Well-defined Operation Set**:There are four very important data transactions in any REST system and HTTP specification: POST (create), GET (read and consult), PUT (edit) and DELETE.
- **URI-oriented**: Objects in REST are always manipulated from the URI. It is the URI and no other element that is the sole identifier of each resource in this REST system. The URI allows us to access the information in order to change or delete it, or for example to share its exact location with third parties.
- **Uniform interface**: to transfer data, the REST system applies specific actions (POST, GET, PUT and DELETE) on the resources, provided they are identified with a URI. This makes it easier to obtain a uniform interface that systematizes the process with the information.
Layer system: hierarchical architecture between the components. Each layer has a functionality within the REST system.
- **Use of hypermedia**: hypermedia is a term coined by Ted Nelson in 1965 and is an extension of the concept of hypertext. This concept, taken to web page development, is what allows the user to browse the set of objects through HTML links. In the case of a REST API, the concept of hypermedia explains the capacity of an app development interface to provide the client and the user with the adequate links to run specific actions on the data.

Advantages:

- **Separation between the client and the server**: the REST protocol totally separates the user interface from the server and the data storage. This has some advantages when making developments. For example, it improves the portability of the interface to other types of platforms, it increases the scalability of the projects, and allows the different components of the developments to be evolved independently.
- **Visibility, reliability and scalability**: The separation between client and server has one evident advantage, and that is that each development team can scale the product without too much problem. They can migrate to other servers or make all kinds of changes in the database, provided the data from each request is sent correctly. The separation makes it easier to have the front and the back on different servers, and this makes the apps more flexible to work with.
- **The REST API is always independent of the type of platform or languages**: The REST API always adapts to the type of syntax or platforms being used, which gives considerable freedom when changing or testing new environments within the development. With a REST API you can have PHP, Java, Python or Node.js servers. The only thing is that it is indispensable that the responses to the requests should always take place in the language used for the information exchange, normally XML or JSON.

## Deploying the API

We will deploy the API using **Docker**. Google describes Docker as follows:


>Docker is an open source containerization platform. It enables developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.

In other words, Docker is a virtualization technology that allows us to execute computer programs, in this case our API, with all dependencies shipped within a single container (and file). The only runtime dependency of a container is an OCI compliant container runtime, which relies on standard features existent in the Linux kernel. The following picture demonstrates the relation between a virtual machine and a container image:

![alt text](docs/docker-vm-container.png)


### Building the Container Image

Prior to being able to execute the container image containg our code we have to put our code into a container. How this is done is defined by our dockerfile:

```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000

# Copy contents from your local to your docker container
COPY ./app /app

# execution is handled by the base image
# CMD ["python","main.py"]
```

Based on the dockerfile we can execute the following bash commands:

```bash
# at first, we log in to docker hub
docker login -u sebastiangau -p xxx
# with this command, we build the image locally on our development machine and give it a name
# this is done by our dockerfile (we tell docker to look for the dockerfile with the dot '.' here)
docker build . -t text-summarizer-api
# we now 'tag' the container image so that docker knows where to upload our baked image - in this case into my personal repository in docker hub
docker tag text-summarizer-api sebastiangau/text-summarizer-api:v1
# we push (=upload) the image from our local development computer to docker hub, a centralized storage service for containers. this takes some time
docker push sebastiangau/text-summarizer-api:v1
```

**IMPORTANT: If you want to try this out you need to create your own docker hub account!** 
Now our container image is ready to be executed in the cloud.


### Deploying the Container Image

We will deploy the API into (Azure) cloud using Azure Kubernetes Service. Wikipedia describes kubernetes as follows:

*Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management. It was originally designed by Google and is now maintained by the Cloud Native Computing Foundation. It aims to provide a "platform for automating deployment, scaling, and operations of container workloads". It works with a variety of container runtimes such as Docker, Containerd, and CRI-O. Kubernetes originally interfaced exclusively with the Docker runtime[8] through a "Dockershim"; however, the shim has since been deprecated in favor of directly interfacing with the container through containerd, or replacing Docker with a runtime that is compliant with the Container Runtime Interface (CRI) introduced by Kubernetes in 2016. Many cloud services offer a Kubernetes-based platform or infrastructure as a service (PaaS or IaaS) on which Kubernetes can be deployed as a platform-providing service. Many vendors also provide their own branded Kubernetes distributions.*

The following picture shows the basic kubernetes architecture:
![](docs/kubernetes.png)

We will now fire commands to the kubernetes API server using their kubernetes command line client, called *kubectl*: 

```bash
kubectl create namespace text-summarizer-api-namespace
kubectl apply -f .\deploy-api-on-kubernetes.yaml -n text-summarizer-api-namespace
```

We afterwards find out which external IP was assigned by Azure to expose our API:

```bash
kubectl describe service text-summarizer-api-service -n text-summarizer-api-namespace
```

We can see the external IP in the command output:

```bash
Name:                     text-summarizer-api-service
Namespace:                text-summarizer-api-namespace
Labels:                   <none>
Annotations:              <none>
Selector:                 app=text-summarizer-api
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.0.145.229
IPs:                      10.0.145.229
LoadBalancer Ingress:     20.50.224.251
Port:                     <unset>  5000/TCP
TargetPort:               5000/TCP
NodePort:                 <unset>  30286/TCP
Endpoints:                <none>
Session Affinity:         None
External Traffic Policy:  Cluster
Events:
  Type    Reason                Age   From                Message
  ----    ------                ----  ----                -------
  Normal  EnsuringLoadBalancer  57s   service-controller  Ensuring load balancer
  Normal  EnsuredLoadBalancer   41s   service-controller  Ensured load balancer
```

Therefore, we can navigate to the following url in our browser [http://20.50.224.251/docs](http://20.50.224.251/docs) where will see the documentation of our API according to our  so-called OpenAPI standard.

**Hint:** To actually use our API in production we would have to ensure many things that we left away here for simplicity:
 - **Encryption and DNS**: Left to the URL, you can see your browser telling you that the website you are calling is 'insecure'. For productive use we need to generate a SSL certificate and bind it in our kubernetes ingress, e.g. by using [Let's Encrypt on Azure Kubernetes Service](https://docs.microsoft.com/de-de/azure/aks/ingress-tls). Additionally, we need a public DNS domain name to ensure our API is reachable by a human-readable name, e.g. under [https://myapi.mydomain.com](https://myapi.mydomain.com) instead of [http://20.50.224.251/docs](http://20.50.224.251/docs).
 - **Authentication and Authorization**: You normally do not want any user in the public internet to be able call your API - only authenticated users should be able to do this based on providing secrets. You can to this by coupling your API with [Azure Active Directory](https://azure.microsoft.com/de-de/services/active-directory/) or an external service like [keycloak](https://www.keycloak.org/).
 - **Securing the API from malicious Attackers**: Any website or API exposed to the public internet needs to be secured from malicious attackers. We need to take multiple measures ensuring that attackers can under no circumstances misuse our API. There are specialised software stacks ensuring that our API is safe from malicious attackers, e.g. to limit invocation frequency from a certain API consumer. They are e.g. available as cloud services, e.g. the [Azure WAF](https://azure.microsoft.com/de-de/services/web-application-firewall/).


## Putting it into Practice


### Example Texts

We will invoke the API using the following test text containing 7 sentences, you can copy the text to test it yourself.

```text
Johannes Gutenberg (1398 – 1468) was a German goldsmith and publisher who introduced printing to Europe. His introduction of mechanical movable type printing to Europe started the Printing Revolution and is widely regarded as the most important event of the modern period. It played a key role in the scientific revolution and laid the basis for the modern knowledge-based economy and the spread of learning to the masses.Gutenberg many contributions to printing are: the invention of a process for mass-producing movable type, the use of oil-based ink for printing books, adjustable molds, and the use of a wooden printing press. His truly epochal invention was the combination of these elements into a practical system that allowed the mass production of printed books and was economically viable for printers and readers alike. In Renaissance Europe, the arrival of mechanical movable type printing introduced the era of mass communication which permanently altered the structure of society. The relatively unrestricted circulation of information—including revolutionary ideas—transcended borders, and captured the masses in the Reformation. The sharp increase in literacy broke the monopoly of the literate elite on education and learning and bolstered the emerging middle class.
```

We can also invoke the API using the following URL [https://www.gutenberg.org/cache/epub/5200/pg5200.txt](https://www.gutenberg.org/cache/epub/5200/pg5200.txt) containing 'Metamorphosis' by Frank Kafka. The API will then pull the text from this URL, summarize it and return the summarized results to us.


### Invocation via WebUI

The [OpenAPI specification](https://swagger.io/specification/) contains guidelines how REST APIs can be documented in a standard format. In our python code, we use a package that automatically creates the API documentation page based on an automatic analysis of our code. **Question:** Can you find out where in the code this package is referenced?

![Alt Text](docs/invocation-webui.gif)

### Invocation of the API via PowerShell on your machine

You can invoke the API using the following powershell command. To open PowerShell, press the windows key and r at the same time, type in 'powershell' and press enter.

```powershell
$body = @{text='Johannes Gutenberg (1398 – 1468) was a German goldsmith and publisher who introduced printing to Europe. His introduction of mechanical movable type printing to Europe started the Printing Revolution and is widely regarded as the most important event of the modern period. It played a key role in the scientific revolution and laid the basis for the modern knowledge-based economy and the spread of learning to the masses.Gutenberg many contributions to printing are: the invention of a process for mass-producing movable type, the use of oil-based ink for printing books, adjustable molds, and the use of a wooden printing press. His truly epochal invention was the combination of these elements into a practical system that allowed the mass production of printed books and was economically viable for printers and readers alike. In Renaissance Europe, the arrival of mechanical movable type printing introduced the era of mass communication which permanently altered the structure of society. The relatively unrestricted circulation of information—including revolutionary ideas—transcended borders, and captured the masses in the Reformation. The sharp increase in literacy broke the monopoly of the literate elite on education and learning and bolstered the emerging middle class.';language='english';sentencecount=3}
$response = Invoke-WebRequest -Uri http://20.50.224.251/summarize -Method 'Post' -Body ($body|ConvertTo-Json) -ContentType "application/json"
$response.Content
```



## Challenges - Invocation for an external URL

The API can also be used to download text from an external URL and summarize it.

*Challenge 1: Invoke the API using the OpenAPI documentation to summarize Kafkas 'Metamorphosis' (you can find the URL link above)!*

<details>
  <summary>Solution to Challenge 1</summary>
  Use the WebUI as shown in the embedded gif, but put in the following request body:
  ```json
  {
  "text": "",
  "url": "https://www.gutenberg.org/cache/epub/5200/pg5200.txt",
  "language": "english",
  "sentencecount": 10
  }
  ```
</details>

*Challenge 2: Invoke the API using PowerShell to summarize Kafkas 'Metamorphosis'!*

<details>
  <summary>Solution to Challenge 2</summary>
  ```powershell
  $body = @{url='https://www.gutenberg.org/cache/epub/5200/pg5200.txt';language='english';sentencecount=3}
  $response = Invoke-WebRequest -Uri http://20.50.224.251/summarize -Method 'Post' -Body ($body|ConvertTo-Json) -ContentType "application/json"
  $response.Content
  ```
</details>






