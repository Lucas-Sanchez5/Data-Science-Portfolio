# 🌐 Full-Stack Web Development & Auth Architecture

## 📌 Overview
This repository section highlights the architectural decisions and backend security implementations of a full-stack web application. The project strictly adheres to the **MVC (Model-View-Controller)** pattern and utilizes a dynamic **React** frontend connected to a secure backend via RESTful APIs.

## 🔐 Security & Authentication (JWT)
One of the core focuses of this build is a robust, stateless authentication flow. 
- **Token Generation:** Upon successful login, the server issues a JSON Web Token (JWT) signed with a secure, environment-protected secret.
- **Protected Routes:** All sensitive API endpoints are shielded by a custom authentication middleware that verifies the token's signature and expiration before granting access.

## ⚡ Key Features & Business Logic
- **Domain Logic & Data Integrity:** Implemented server-side validations to enforce enrollment capacity limits and prevent duplicate entries before writing to the database.
- **Auditability via Soft Delete:** Applied non-destructive deletion patterns (`is_deleted` flags) across core entities to preserve historical data traceability.
- **Automated Document Generation:** Integrated headless browser rendering to automatically generate official course certificates in PDF format based on real-time database queries.

## 🤖 AI-Assisted Prototyping
To accelerate the development cycle, **AI agents and advanced Prompt Engineering** were leveraged. This approach significantly sped up the creation of React component boilerplates, CSS state management, and initial database schemas, allowing for a faster transition from concept to functional prototype.

## 📂 Featured Code Snippets
Check out the `src/` directory for core backend implementations:
* [`jwt_middleware.js`](./src/jwt_middleware.js) - Middleware function used to protect secure backend routes.
* [`pdf_generator_service.js`](./src/pdf_generator_service.js) - Asynchronous PDF rendering service using Puppeteer and Handlebars.
* [`enrollment_service.js`](./src/enrollment_service.js) - Domain logic handling capacity validation, duplicate checks, and soft deletes.

## 🚀 Technologies Used
* **Frontend:** React, JavaScript, HTML5/CSS3
* **Backend:** Node.js, Express
* **Database & ORM:** PostgreSQL / SQL (Relational Design, Soft Delete)
* **Document Engine:** Puppeteer, Handlebars
* **Architecture & Security:** MVC, REST API, JSON Web Tokens (JWT)