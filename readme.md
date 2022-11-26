# Kanban App

## Introduction

This is a Kanban app built with Vue.js and Flask. It is a simple app that allows you to create, edit, and delete tasks. It also allows you to move tasks between columns. The app is built with a RESTful API and uses Vue.js for the frontend.

## Installation

To install the app, clone the repository and run the following commands:

```bash
cd kaban/project
npm install
npm run serve
```

Then, open a new terminal and run:

```bash
cd backend
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

The app should now be running at http://localhost:8080.

## Api Reference

### Register (POST)

```http
POST /register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name`    | `string` | **Required**. Your name    |
| `email`   | `string` | **Required**. Your email   |
| `password`    | `string` | **Required**. Your password|
| `u_name`   | `string` | **Required**. Your username|
| `name`    | `string` | **Required**. Your name    |

### Login (POST)

```http
POST /login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email`   | `string` | **Required**. Your email   |
| `password`    | `string` | **Required**. Your password|

### Get List (GET)

```http
GET /lists
```

### Create List (POST)

```http
POST /lists
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name`   | `string` | **Required**. List name   |

### Update List (PUT)

```http
PUT /lists
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `list_id`      | `string` | **Required**. List id      |
| `list_name`   | `string` | **Required**. List title   |

### Delete List (DELETE)

```http
DELETE /lists
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id`      | `string` | **Required**. List id      |

### Get Cards (GET)

```http
GET /cards/:list_id
```

### Create Card (POST)

```http
POST /cards/:list_id
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `card_title`   | `string` | **Required**. Card title   |
| `card_description`      | `string` | **Required**. Card description      |
| `card_content`   | `string` | **Required**. Card content   |
| `card_status`   | `string` | **Required**. Card status   |
| `card_deadline`   | `string` | **Required**. Card deadline   |
| `card_completion_date`   | `string` | Card completion date   |

### Update Card (PUT)

```http
PUT /cards/:list_id
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `card_id`      | `string` | **Required**. Card id      |
| `card_title`   | `string` | **Required**. Card title   |
| `card_description`      | `string` | **Required**. Card description      |
| `card_content`   | `string` | **Required**. Card content   |
| `card_status`   | `string` | **Required**. Card status   |
| `card_deadline`   | `string` | **Required**. Card deadline   |
| `card_completion_date`   | `string` | Card completion date   |

### Delete Card (DELETE)

```http
DELETE /cards/:list_id
```

### Download Card (GET)

```http
GET /download/:list_id/:card_id
```

### Download List (GET)

```http
GET /download/:list_id
```