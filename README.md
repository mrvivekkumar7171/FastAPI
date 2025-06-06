# 🧩 What is an API?
An API (Application Programming Interface) is a set of rules and protocols that allow two software components—like frontend and backend—to communicate with each other.s
Real-Life Analogy:
Think of an API as a waiter in a restaurant:
The customer (frontend) places an order.
The waiter (API) communicates this to the kitchen (backend).
The kitchen prepares the dish (response) and the waiter delivers it back to the customer.

![API](images/image.png)
![API Example in Restaurant](images/image-1.png)

## ⚡ Why FastAPI and Not Other Frameworks?
Most companies prefer FastAPI for deploying ML models due to its:
Speed (based on asynchronous programming)
Easy integration with Python-based ML workflows
Automatic generation of interactive API documentation (via Swagger UI)
Built-in validation and error handling using Pydentic
Fast development and testing processs
All these benefits make FastAPI ideal for modern, scalable ML applications.

## ❓ Why Do We Need APIs?
Let’s take the example of IRCTC (Indian Railway Catering and Tourism Corporation):
Initially, when everything was built as a monolithic application (single application i.e. frontend and backend code in single directory thus enabling direct communication without API), both frontend and backend code existed within a single structure. In such a setup:
- Frontend directly called backend functions to fetch data from the database.
- Communication between frontend and backend was internal and didn’t require APIs.
- However, this tight coupling meant that a failure in one component could affect the entire system.

## 🤖 So, why move to APIs?
Imagine third-party services like MakeMyTrip, Yatra, or Ixigo want real-time train data from IRCTC for trains between two locations and agreed to pay for it. With a monolithic setup:
- You can't give direct access to your internal backend.
- You can’t expose your database either.
Solution: Add an API layer on top of your backend.
- This API can be accessed by any external system using defined endpoints.
- The frontend and other clients (like mobile apps, partner websites, etc.) can now fetch data through these APIs using HTTP/HTTPS protocols. All the frontend uses same backend and database instead of multiple Monolithic Architectures
- You can enforce security, rate limits, access control, and other constraints on these APIs.
- The response from the API come in a specific format called json (universal data format) enabling all the backend written in different languages to communicate easily like makemytrip, yatra and ixigo etc. may be using python, java and php backend respectively.
- Here, Backend and frontend are not coupled like in Monolithic Architecture.

## 🌐 Why APIs Are Needed for ML Models + Why FastAPI?
APIs are essential for making machine learning models accessible and usable across various platforms. This write-up covers the importance of APIs, why FastAPI is often chosen for ML deployment, and a simple analogy to help understand APIs in real-world scenarios.
To make a machine learning model accessible to the rest of the world, an API (Application Programming Interface) is required. Machine learning models often rely on structured data or predictions, and users (clients or customers) want to access these services through a backend system.
APIs act as bridges that allow your ML model (hosted on a server) to be used on various platforms, such as websites, mobile apps, or even other services.
For example, OpenAI's ChatGPT model is accessible through an API—developers can integrate it into their own websites or applications seamlessly.

![API on multiple platform](images/image-2.png)

## What is fastAPI?
FastAPI is a modern, high-performance web framework for building APIs with Python. It is made using two most popular libraries Starlette (manages how your API receives requests and sends back responses) and Pydentic(data validation library to check if the data incoming into your API is correct and in the right format).

## Objectives of FastAPI?
- Fast to run and handle concurrent users
- Fast to code the API

## Why FastAPI is so fast?
- When we deploy ML model on AWS, It has two components.
Web Server: Listen http requests that are coming to the port of AWS machine on which the API is running.
Example of http request received by the Web Server.
```bash
    POST /predict HTTP/1.1
    Host: api.example.com
    Content-Type: application/json
    Content-Length: 45
    {
    "feature1": 5.2,
    "feature2": 3.1
    }
```
- API Code: It contains number of future values model will get, how to load the model, call the function to generate the prediction.
Example of Output of the model
```bash
"prediction:8.3"
```

- SGI(Server Gateway Interface): convert http request into python understandable format.
Example of output of http request to be passed to the API Code.
```bash
Request.method --> "POST"
Request.url --> "/predict"
Request.json()->{"feature1": 5.2, "feature2": 3.1}
```
- Example of Response after converting into http understandable format by the SGI.
```bash
HTTP/1.1 200 OK
Content-Type: application/json
{
"prediction": 8.3
}
```
![FastAPI](images/image-3.png)

## Flask VS FastAPI:
In Flask, we use WSGI(Web Server Gateway Interface) by the name of Gunicorn as SGI which is Synchronous Endpoint. Its synchronous nature (one request at a time) and blocking architecture can lead to slower request processing and scalability challenges. It uses Werkzeug.
```bash
@app.route("/predict", methods=["POST"])
def predict():
    json_data = request.get_json()
    data = InputData(**json_data)
    result = predict_sync(data)
    return jsonify(result)
```
In FastAPI, we use ASGI(Asynchronous Server Gateway Interface) by the name of uvicorn as SGI which is Asynchronous Endpoint. It can process multiple request concurrently and provide high performance. It uses Starlette.
Here, if predict_async(data) will take longer time and new request came then function predict will process the next one without waiting for the output of the first one.
```bash
@app.post("/predict")
async def predict(data: InputData):
    result = await predict_async(data)
    return result
```

## Why FastAPI is fast to code?
1. Automatic Input Validation using Pydentic
2. Auto-Generated Interactive Documentation
3. Seamless Integration with Modern Ecosystem (ML/DL libraries, OAuth, JWT, SQL Alchemy, Docker, Kubernetes etc.)

## Example of Basic FastAPI:
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}
```
- To run the FastAPI you need to install the required libraries:
```bash
pip install fastapi uvicorn pydentic
```
- To run the app, use the command in the terminal instead of running the python file:
```bash
uvicorn main:app --reload
```
- **Reload** will automatically reload the server when you make changes to the code.
- http://127.0.0.1:8000/docs to see the **API documentation** where 8000 is the **port number** and **127.0.0.1** is the IP address.

## ML model with FastAPI
- An website that helps patient to maintain patient records to treat the patient better as physical documents can be lost, miss-place etc. It allows you to add new customer profile(create), view(one individual and all patient), update and delete the existing customers. **Here, we are storing the customer profile in a json but ideally one should store in a database.**
- **endpoints** in the example:
    - /create
    - /view
    - /view/patient_id
    - /update/patient_id
    - /delete/polient_id
- **Http Methods**: In website the software is installed in **server** and accessed by the **client** on other machine using http protocol.
There are two types of websites(softwares):
1. **Static**: very less interaction between user and client like calender, Blog, Government Website and clock.
2. **Dynamic**: too much interaction between user and client like MSExcel, YouTube etc.
- Four operations(**CRUD**) performed in Dynamic Software are:

**Create**: **POST**
```bash
@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])
    # save into the json file
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'patient created successfully'})
```
**Retrieve**: **GET**
```bash
@app.get("/view")
def view():
    data = load_data()
    return data
```
**Update**: **PUTs**
```bash
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')
    # add this dict to data
    data[patient_id] = existing_patient_info
    # save data
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient updated'})
```
**Delete**: **DELETE**
```bash
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # load data
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient deleted'})
```
![Patients](images/image-4.png)

## Path Parameters: 
They are dynamic segments of a URL path used to identify a specific resource. The Path() furiction in FastAPI is used to provide metadata, validation rules, and documentation hints for path parameters in your API endpoints.
Example:
    Title
    Description
    Example
    ge(greater than equal to), gt, le, It
    Min_length
    Max_length
    regex
    ... (means required)

**HTTP status codes** are 3-digit numbers returned by a web server (like FastAPI) to indicate the result of a client's request (like from a browser or API consumer).

![alt text](image.png)

They help the client (browser, frontend, mobile app, etc.) understand:
    - whether the request was successful,
    - whether something went wrong,
    - and what kind of issue occurred (if any).

| Code Range | Meaning        | Description                                              |
|------------|----------------|----------------------------------------------------------|
| `2xx`      | Success        | The request was successfully received and processed      |
| `3xx`      | Redirection    | Further action needs to be taken (e.g., redirect)        |
| `4xx`      | Client Error   | Something is wrong with the request from the client      |
| `5xx`      | Server Error   | Something went wrong on the server side                  |

| Status Code | Meaning                   | When It Occurs                                      |
|-------------|---------------------------|-----------------------------------------------------|
| `200 OK`    | Standard success          | A GET or POST succeeded                             |
| `201 Created` | Resource created        | After a POST that creates something                 |
| `204 No Content` | Success, no data     | After a DELETE request                              |
| `400 Bad Request` | Malformed request   | Missing field, wrong data type                      |
| `401 Unauthorized` | Auth required      | No or invalid authentication; login required        |
| `403 Forbidden` | Permission denied     | Logged in but not allowed                           |
| `404 Not Found` | Resource missing      | Patient ID not in database                          |
| `500 Internal Server Error` | Server failure | Something broke on the server                  |
| `502 Bad Gateway` | Gateway failure     | Gateway (e.g., Nginx) failed to reach backend       |
| `503 Service Unavailable` | Server down | Server is down or overloaded                        |

**HTTPException** is a special built-in exception in FastAPI used to return custom HTTP error responses when something goes wrong in your API.
Instead of returning a normal JSON or crashing the server, you can gracefully raise an error with:
- a proper HTTP status code (like 404, 400, 403, etc.)
- a custom error message
- (optional) extra headers

Example of HTTPException, HTTP status codes and Path Parameters.
```bash
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    # load all the patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')
```

**Query Parameter** are optional key-value pairs appended to the end of a URL, used to pass additional data to the server in an HTTP request. They are typically employed for operations like filtering, sorting, searching, and pagination, without altering the endpoint path itself.
```bash
/patients?city=Delhi&sort_by=age
```
- The ? marks the start of query parameters.
- Each parameter is a key-value pair: `key=value`
- Multiple parameters are separated by `&`
In this case:
    - `city=Delhi` is a query parameter for filtering
    - `sort_by=age` is a query parameter for sorting

**Query()** is a utility function provided by FastAPI to declare, validate, and document query parameters in your API endpoints.

It allows you to:
    - Set default values
    - Enforce validation rules
    - Add metadata like description, title, examples

| Parameter/Option      | Description                                |
|-----------------------|--------------------------------------------|
| `default`             | Set default value (e.g., `Query(e)`)       |
| `title`               | Displayed in API documentation             |
| `description`         | Detailed explanation in Swagger UI         |
| `example` / `examples`| Provide sample input(s)                    |
| `min_length`, `max_length` | Validate string length                |
| `ge`, `gt`, `le`, `lt`| Validate numeric bounds                    |
| `regex`               | Pattern match for string validation        |

```bash
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), 
                    order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data
```

A **request body** is the portion of an HTTP request that contains data sent by the client to the server. It is typically used in HTTP methods such as POST, or PUT to transmit structured data (e.g., JSON, XML, form-data) for the purpose of creating or updating resources on the server. The server parses the request body to extract the necessary information and perform the intended
operation.

## deployment of API on AWS
