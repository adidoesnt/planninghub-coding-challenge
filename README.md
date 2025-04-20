# PlanningHub Coding Challenge

## Overview

This is a simple REST API that allows a client to determine whether planning permission is required or not required for a fence, gate, or wall in various scenarios.

## Approach

Here is a summary of the approach I took to solve the problem:

1. I created a CSV config file that stores the condition types, conditions for each condition type, and the combination of conditions that make up each site category.
2. I created a schema generator that reads the config file and generates a JSON schema based on the config file.
3. I created a classifier that uses the schema to validate the input data, flatten it into a binary vector, and match it against binary vectors for each category from the config file.
    - For universal categories, if the input data matches any of the conditions for the category, then the category is a match.
    - For other categories, if the input data matches all of the conditions for the category, then the category is a match.
    - If there are any universal categories matched, then planning permission is required, and we do not need to check the other categories.
    - If there are no universal categories matched, then we check the other categories.
    - If there is one match in other categories, we check if it requires planning permission and return that.
    - If there are multiple matches in other categories, we check if any one of them requires planning permission. If so, then planning permission is required.
    - If there are no matches, then we raise an error.
4. I created a simple REST API using FastAPI to allow a client to forward input data to the classifier and receive a response.

## Setup

### No Docker

1. Clone the repository

```bash
git clone https://github.com/adidoesnt/planninghub-coding-challenge.git
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file to `.env` and change the variables if needed

```bash
cp .env.example .env
```

4. Run the schema generator

```bash
python -m src.planninghub_coding_challenge.components.utils.schema_generator
```

5. Run the server

```bash
python src/planninghub-coding-challenge/main.py
```

### Docker

1. Clone the repository

```bash
git clone https://github.com/adidoesnt/planninghub-coding-challenge.git
```

2. Copy the `.env.example` file to `.env` and change the variables if needed

```bash
cp .env.example .env
```

3. Use Docker Compose to build and run the container

```bash
docker-compose up --build
```

## API Documentation

### Base URL

By default, the server runs at `http://localhost:8080`

### Endpoints

#### 1. Health Check

Check if the server is running properly.

```
GET /
```

##### Response

```json
{
  "message": "Server is healthy"
}
```

#### 2. Classify Planning Permission

Check if planning permission is required based on the provided criteria.

```
POST /classify
```

##### Request Body Schema

The request body should be a JSON object with the following structure:

```json
{
  "location": {
    "adjacent": boolean,
    "gate_fence_wall": boolean
  },
  "height": {
    "up_to_1m": boolean,
    "above_1m": boolean,
    "up_to_2m": boolean,
    "above_2m": boolean
  },
  "planning_constraints": {
    "listed_building": boolean,
    "article_2_3_land": boolean,
    "article_2_4_land": boolean,
    "article_4_directive": boolean,
    "aonb": boolean,
    "works_affecting_tpo": boolean
  },
  "other": {
    "permitted_development_removed": boolean,
    "new_build_property": boolean
  }
}
```

> **Note**: The request body schema is dynamically generated from `config/planning-permission-rules-config.csv` (or whatever you choose to name your config CSV file).

##### Example Request

```bash
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d ./config/sample-input.json
```

##### Example Response

```json
{
  "message": "OK",
  "input_data": {
    "location": { "adjacent": true, "gate_fence_wall": false },
    "height": {
      "up_to_1m": true,
      "above_1m": false,
      "up_to_2m": false,
      "above_2m": false
    },
    "planning_constraints": {
      "listed_building": false,
      "article_2_3_land": false,
      "article_2_4_land": false,
      "article_4_directive": false,
      "aonb": false,
      "works_affecting_tpo": false
    },
    "other": {
      "permitted_development_removed": false,
      "new_build_property": false
    }
  },
  "result": {
    "planning_permission_required": true
  }
}
```

##### Error Response

If the input data is invalid:

```json
{
  "message": "Error",
  "error": "Invalid input data: [error details]"
}
```
