![image-entete](img/entete.webp)
# HBnB Technical Documentation
- [HBnB Technical Documentation](#hbnb-technical-documentation)
  - [Introduction](#introduction)
  - [General Architecture](#general-architecture)
    - [Layered Architecture Overview](#layered-architecture-overview)
    - [Key Components](#key-components)
  - [Domain Models](#domain-models)
    - [Class Structure](#class-structure)
      - [Core Entities](#core-entities)
  - [API Interaction Flows](#api-interaction-flows)
    - [User Registration](#user-registration)
    - [Place Creation](#place-creation)
    - [Review Submission](#review-submission)
    - [Fetching Places List](#fetching-places-list)
  - [Technical Considerations](#technical-considerations)
    - [Security](#security)
    - [Error Handling](#error-handling)
    - [Performance](#performance)
  - [Implementation Notes](#implementation-notes)
    - [Authentication Flow](#authentication-flow)
    - [Data Validation Strategy](#data-validation-strategy)
    - [API Design Principles](#api-design-principles)
  - [Conclusion](#conclusion)
  - [Authors](#authors)

## Introduction

This technical document details the architecture and design of the HBnB (Holberton Bed and Breakfast) project, a lodging reservation platform. 

This documentation serves as a comprehensive guide for system implementation and provides a detailed reference of its architecture.

The HBnB project is designed using a modern layered architecture, implementing robust design patterns to ensure maintainability, scalability, and separation of concerns.

## General Architecture
![package-diagram](<img/High-Level Package Diagram.png>)
### Layered Architecture Overview

The application is structured in three main layers:

1. **Presentation Layer**: Handles client interactions through a REST API
2. **Business Logic Layer**: Contains business logic and domain models
3. **Persistence Layer**: Manages data storage and retrieval

The architecture employs the Facade pattern at multiple levels to decouple different layers:
- APIFacade: Interface between presentation layer and business logic
- BusinessFacade: Business operations orchestration
- StorageFacade: Persistence layer abstraction

### Key Components

**Presentation Layer**
- RESTServices: API endpoints for users, places, reviews, and amenities
- APIFacade: Unified interface for request handling

**Business Logic Layer**
- DomainModels: Business entity definitions (User, Place, Review, Amenity)
- BusinessFacade: Business rules orchestration and validation

**Persistence Layer**
- DataAccess: Database operations, cache management, and validation
- StorageFacade: Standardized CRUD interface

## Domain Models

### Class Structure
![class-diagram](<img/Class Diagram for Business Logic Layer.png>)


The system is built around a `BaseModel` base class that provides common functionality:
- Unique identifier management (UUID)
- Timestamps (created_at, updated_at)
- Utility methods (save, to_dict, str)

#### Core Entities

**User**
- Attributes: email, password, first_name, last_name
- Relationships: places (owner), reviews (author)
- Key Methods: create_place(), update_profile(), authenticate()

**Place**
- Attributes: name, description, price_per_night, location (latitude/longitude)
- Relationships: owner (User), reviews, amenities
- Key Methods: add_amenity(), calculate_total_price(), update_availability()

**Review**
- Attributes: text, rating
- Relationships: reviewer (User), place
- Key Methods: update_review(), validate_rating()

**Amenity**
- Attributes: name, description
- Relationships: places
- Key Methods: update_amenity(), get_places()

## API Interaction Flows

### User Registration
![user-registration](<img/Sequence Diagram - User Registration Flow.png>)
The registration process comprises:
1. Input data validation
2. Email uniqueness verification
3. Password hashing
4. User account creation
5. Registration confirmation

### Place Creation
![place creation](<img/Sequence Diagram - Place Creation Flow.png>)
The creation process involves several validation steps:
1. Receiving POST request with data and token
2. Authentication verification via AuthMiddleware
3. Input data validation
4. Instance creation in database
5. Creation confirmation (201 Created)

### Review Submission
![review-submission](<img/Sequence Diagram - Review Submission Flow.png>)
The review creation process includes:
1. Authentication token validation
2. Place existence verification
3. Review data validation
4. Review creation and storage
5. Appropriate status return
      
### Fetching Places List
![fetching-places](<img/Sequence Diagram - Fetching Places List Flow.png>)
The place retrieval process follows a sequence of operations:
1. Client sends GET request with filter parameters
2. API delegates to PlaceService
3. Query construction via QueryBuilder
4. Query execution and data retrieval
5. Response formatting and serialization
6. Return to client with 200 OK status

## Technical Considerations

### Security
- Token-based authentication
- Systematic input validation
- Password hashing
- Authorization checks

### Error Handling

| HTTP Code | Description |
|-----------|-------------|
| 200       | OK - The request has succeeded. |
| 201       | Created - The request has been fulfilled and resulted in a new resource being created. |
| 400       | Bad Request - The server could not understand the request due to invalid syntax. |
| 401       | Unauthorized - The client must authenticate itself to get the requested response. |
| 404       | Not Found - The server can not find the requested resource. |
| 409       | Conflict - The request could not be completed due to a conflict with the current state of the target resource. |
| 500       | Internal Server Error - The server has encountered a situation it doesn't know how to handle. |

- Explicit error messages
- Multi-level validation

### Performance
- Caching via DataAccess
- Optimized queries via QueryBuilder
- Efficient data serialization

## Implementation Notes

### Authentication Flow
- Middleware-based token verification
- Secure password handling
- Session management
- Access control implementation

### Data Validation Strategy
- Input sanitization
- Business rule validation
- Data integrity checks
- Error handling protocols

### API Design Principles
- RESTful endpoint structure
- Consistent response formats
- Proper status code usage
- Rate limiting considerations

## Conclusion

This technical documentation provides a comprehensive view of the HBnB system's architecture and operation. 

It serves as a reference for project implementation and maintenance, ensuring a common understanding among development team members.

The documented design patterns and architectural decisions support:
- Scalability for future growth
- Maintainability through clear separation of concerns
- Security through systematic validation and authentication
- Performance through optimized data handling

## Authors

<li> Adrien MENDES RAMOS - <a href="https://github.com/Saynez667">@Saynez667</a></li>
<li> Benjamin RISTORD - <a href="https://github.com/jbn179">@jbn179</a></li>
<li> Mina SINANI - <a href="https://github.com/MINS2405">@MINS2405</a></li>