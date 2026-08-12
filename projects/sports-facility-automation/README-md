# 💬 Automated Conversational Assistant

## 📌 Overview
This project showcases the architecture and development of an automated conversational bot designed to manage sports facility reservations via WhatsApp. By leveraging **n8n workflows** and the **Facebook Graph API**, the system eliminates manual booking friction and provides users with real-time availability and confirmation.

## 🛠️ Technical Highlights
- **Webhook & API Integration:** Engineered robust webhooks in n8n to listen for incoming messages, securely processing inbound HTTP requests and complex JSON payloads from the Facebook Graph API.

- **Intent Classification:** Implemented conditional logic and parsing strategies to accurately classify user intents (e.g., booking, canceling, querying schedules) directly from raw message text.

- **Resilient Workflows:** Designed error-handling nodes within n8n to catch API timeouts and trigger fallback responses, ensuring high availability and a seamless user experience.

## 🚀 Technologies Used
- **Automation Platform:** n8n

- **APIs:** Facebook Graph API, RESTful APIs

- **Data Processing:** JSON parsing, Webhooks

## ⚙️ System Architecture Flow

```mermaid
graph TD
    A[User WhatsApp Message] -->|Webhook Trigger| B[n8n Workflow Listener]
    B --> C{Intent Classification}
    C -->|Query Availability| D[Database/CRM]
    C -->|Booking Request| E[Process Reservation]
    C -->|Unrecognized/Support| F[Human Hand-off]
    D --> G[Generate JSON Payload]
    E --> G
    G --> H[Facebook Graph API]
    H --> I[Automated WhatsApp Reply]