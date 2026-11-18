

\# Database Entity Relationship Diagram



```mermaid

erDiagram

&#x20;   USERS ||--o{ BOOKINGS : creates

&#x20;   PASSENGERS ||--o{ BOOKINGS : travels\_on

&#x20;   FLIGHTS ||--o{ BOOKINGS : reserved\_for

&#x20;   BOOKINGS ||--o{ PAYMENTS : has



&#x20;   USERS {

&#x20;       int user\_id PK

&#x20;   }



&#x20;   PASSENGERS {

&#x20;       int passenger\_id PK

&#x20;   }



&#x20;   FLIGHTS {

&#x20;       int flight\_id PK

&#x20;   }



&#x20;   BOOKINGS {

&#x20;       int booking\_id PK

&#x20;       int user\_id FK

&#x20;       int passenger\_id FK

&#x20;       int flight\_id FK

&#x20;   }



&#x20;   PAYMENTS {

&#x20;       int payment\_id PK

&#x20;       int booking\_id FK

&#x20;   }



&#x20;   AIRPORTS {

&#x20;       int airport\_id PK

&#x20;   }

```



\## Database Description



The application uses MySQL to manage users, passengers, airports, flights, bookings, and payments.



\- \*\*Users:\*\* Stores registered user accounts.

\- \*\*Passengers:\*\* Stores passenger information.

\- \*\*Airports:\*\* Stores airport reference information.

\- \*\*Flights:\*\* Stores flight details, prices, and seat availability.

\- \*\*Bookings:\*\* Connects users, passengers, and flights.

\- \*\*Payments:\*\* Stores simulated payment records associated with bookings.



The booking records associate a reservation with its authenticated user, passenger, and selected flight.



