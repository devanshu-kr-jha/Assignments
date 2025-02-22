
# **User Management API**  

A **Flask-based REST API** for managing user data with CRUD operations, search, sorting, pagination, and statistics. Includes OpenAPI documentation and Docker support.

---

## **API Reference**  

### **1️⃣ Get All Users**  

```http
GET /api/v1/users
```

#### **Query Parameters**  
| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `page`    | `int`    | Page number for pagination |
| `limit`   | `int`    | Number of items per page (default: 5) |
| `search`  | `string` | Case-insensitive search on First Name or Last Name |
| `sort`    | `string` | Field to sort in ascending order; prefix with `-` (e.g., `-age`) for descending |

#### **Example Request**
```http
GET /api/v1/users?page=1&limit=10&search=James&sort=-age
```

---

### **2️⃣ Get a Single User**  

```http
GET /api/v1/users/{id}
```

#### **Path Parameters**  
| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `id`      | `int`    | Retrieve details of a user by ID |

---

### **3️⃣ Create a User**  

```http
POST /api/v1/users
```

#### **Request Body (JSON)**  
| Field | Type  | Description  |
| :---- | :---- | :----------- |
| `first_name` | `string` | User's first name |
| `last_name` | `string` | User's last name |
| `company_name` | `string` | Company the user works for |
| `age` | `int` | User's age |
| `city` | `string` | User's city |
| `state` | `string` | User's state |
| `zip` | `int` | Zip code |
| `email` | `string` | User's email |
| `web` | `string` | User's website |

#### **Example Request**
```json
{
  "first_name": "Amit",
  "last_name": "Sharma",
  "company_name": "TCS",
  "age": 30,
  "city": "Mumbai",
  "state": "Maharashtra",
  "zip": 400001,
  "email": "amit.sharma@example.com",
  "web": "https://tcs.com"
}
```

---

### **4️⃣ Update a User (Full Update)**  

```http
PUT /api/v1/users/{id}
```

#### **Path Parameters**  
| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `id`      | `int`    | ID of the user to update |

#### **Request Body (JSON)**  
(Same as Create User)

---

### **5️⃣ Partially Update a User**  

```http
PATCH /api/v1/users/{id}
```

#### **Path Parameters**  
| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `id`      | `int`    | ID of the user to update |

#### **Request Body (JSON)**  
| Field | Type  | Description  |
| :---- | :---- | :----------- |
| `first_name` | `string` | (Optional) User's first name |
| `age` | `int` | (Optional) User's age |

---

### **6️⃣ Delete a User**  

```http
DELETE /api/v1/users/{id}
```

#### **Path Parameters**  
| Parameter | Type     | Description  |
| :-------- | :------- | :----------- |
| `id`      | `int`    | ID of the user to delete |

---

### **7️⃣ Get User Statistics**  

```http
GET /api/v1/users/summary
```

#### **Response Example**
```json
{
  "data": {
    "avg_age": 56.01,
    "count_by_city": {
      "Mumbai": 10,
      "Delhi": 15
    },
    "max_age": 99,
    "min_age": 18
  }
}
```
---

## **Run with Docker**  
This will start both the **Flask API** and **PostgreSQL database**.

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/devanshu-kr-jha/Assignments

cd Assignments/flask_task
```

### **2️⃣ Run docker-compose.yml**  
```sh
docker-compose up --build -d
```
## **API Documentation (Swagger UI)**  
Once running, access **Swagger UI** at:  
**`http://localhost:5000/api/docs`**

---
