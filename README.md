# Virtual IR Lab Annotation System

**1. Overview**
- We host an engine on Cloud( i.e. AWS, Azure). The engine receives a query and produces a ranked list which can be annotated by annotators. Researchers or educators can upload their own IR algorithms and datasets into the Cloud so that the engine can run different IR algorithms and apply algorithms on different datasets and annotators can perform mannual annotation and relevance judgement.

**2. System Architecture**
![Screen Shot 2017-02-28 at 10.18.39 PM](http://i.imgur.com/zIczFb8.png)
**3. Technologies**
- Primary programming languages: Python
- Web framework: Flask
- Database

**4. Functionalities & APIs**
- Upload datasets & query set
- Override ranking & retrieving functions
- Annotation
- A/B test (Leaderboard)

**5. Future Plan**
- Build up web framework to handle local request.
- Implement API for uploading data sets and query
- Implement modules for overriding ranking & retrieving functions.
- Implement annotation module.
- Implement A/B test module.
- Testing functionalities.
- Deploy the system on cloud.
