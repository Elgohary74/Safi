

**Introduction to Software Engineering**

# **Safi | صافي**

CSAI 203 \- Fall 2025

# **Specification Requirements Document**

Team Number: 36

Team Members

[Elgohary Mohamed 202300526](mailto:s-elgohary.khedr@zewailcity.edu.eg)

[Osama Ashraf 202301054](mailto:s-osama.abdelwahhab@zewailcity.edu.eg)

[Mohamed Radwan 202300723](mailto:s-mohamed.el-dakrony@zewailcity.edu.eg)

[Omar Mohamed 202301042](mailto:s-omar.shehata@zewailcity.edu.eg)

Representative Contact info:

**Elgohary Mohamed**			 [s-elgohary.khedr@zewailcity.edu.eg](mailto:s-elgohary.khedr@zewailcity.edu.eg)

#

[**1\. Introduction	3**](#1.-introduction)

[1.1 Purpose	3](#1.1-purpose)

[1.2 Scope	3](#1.2-scope)

[1.3 Definitions, Acronyms, and Abbreviations	3](#1.3-definitions,-acronyms,-and-abbreviations)

[1.4 References	3](#1.4-references)

[1.5 Overview	3](#1.5-overview)

[**2\. Overall Description	4**](#2.-overall-description)

[2.2 Product Functions	4](#2.2-product-functions)

[2.3 User Classes and Characteristics	4](#2.3-user-classes-and-characteristics)

[2.4 Operating Environment	4](#2.4-operating-environment)

[2.5 Design and Implementation Constraints	4](#2.5-design-and-implementation-constraints)

[2.6 User Documentation	5](#2.6-user-documentation)

[2.7 Assumptions and Dependencies	5](#2.7-assumptions-and-dependencies)

[2.7.1 Assumptions	5](#2.7.1-assumptions)

[2.7.2 Dependencies	5](#2.7.2-dependencies)

[**3\. Specific Requirements	5**](#3.-specific-requirements)

[3.1 Functional Requirements	5](#3.1-functional-requirements)

[3.2 Use Case Model	6](#3.2-use-case-model)

[3.2.1 Use Case Diagrams	6](#3.2.1-use-case-diagrams)

[3.2.2 Use Cases Description	7](#3.2.2-use-cases-description)

[3.2.2.1 Financial Management	7](#3.2.2.1-financial-management)

[3.3 Domain Model	13](#3.3-domain-model)

[3.3.1 Conceptual Class Diagram	13](#3.3.1-conceptual-class-diagram)

[3.3.2 Class Descriptions	13](#3.3.2-class-descriptions)

[3.4 Non-Functional Requirements	14](#3.4-non-functional-requirements)

[3.5 External Interface Requirements	15](#3.5-external-interface-requirements)

[3.5.1 User Interface	15](#3.5.1-user-interface)

[3.5.4 Communication Interface	15](#3.5.4-communication-interface)

[4.1 Appendix A: Data Dictionary	15](#4.1-appendix-a:-data-dictionary)

[4.2 Appendix B: Glossary	15](#4.2-appendix-b:-glossary)

#

# **1\. Introduction** {#1.-introduction}

## **1.1 Purpose**  {#1.1-purpose}

This document defines the software requirements for the Safi web application. Safi enables groups of people to manage shared expenses and compute the simplest set of transactions needed for members to settle their balances. The SRS describes the full functionality planned for the application's initial release.

## **1.2 Scope** {#1.2-scope}

Safi is a web application that helps small groups manage shared expenses and automatically compute the simplest settlement transactions so each member pays an equal share. The system focuses solely on calculating and organizing expenses.

## **1.3 Definitions, Acronyms, and Abbreviations** {#1.3-definitions,-acronyms,-and-abbreviations}

| User  | Any person who registers and uses the Safi application |
| :---- | :---- |
| **Group** | A collection of users sharing expenses (roommates, friends) |
| **Expense** | A cost incurred by a user on behalf of the group  |
| **Settlement** | The Process of simplifying and balancing debts among users  |

## **1.4 References**  {#1.4-references}

* Flask Documentation: [https://flask.palletsprojects.com/en/stable/](https://flask.palletsprojects.com/en/stable/)
* Mongo Documentation: [https://www.mongodb.com/docs/](https://www.mongodb.com/docs/)
* Github Documentation: [https://docs.github.com/en](https://docs.github.com/en)

## **1.5 Overview**  {#1.5-overview}

The remainder of this SRS describes the system’s overall design, functionalities, constraints, and requirements in detail, following IEEE guidelines.

# **2\. Overall Description** {#2.-overall-description}

Safi is a web application designed to manage shared expenses. The application operates with two main external interfaces:

* **Users**: who access the system through a web browser.
* **A database server**: To store the data of the application.

## **2.2 Product Functions** {#2.2-product-functions}

* **User Account Management:** Managing registration(log in, sign up).
* **Dashboard:** For group management, including group creation and membership.
* **Multi-Group Support:** Users can join multiple groups simultaneously.
* **Expense Management:** Record expenses in detail between users.
* **Debt Simplification:** Automatic minimization of transactions within a group.
* **Financial Summaries:** Summarize the financial state for each user.
* **Settlement & Confirmation:** Record user settlements via two-way confirmation.
* **Notifications:** In-app alerts for pending actions, such as settlement requests.

## **2.3 User Classes and Characteristics**  {#2.3-user-classes-and-characteristics}

**User:** Anyone who needs to manage shared expenses (students, roommates,...)

## **2.4 Operating Environment** {#2.4-operating-environment}

**Server:** Linux-based server (Ubuntu LTS) that can run Flask and MongoDB

**Client:** Any device (desktop, laptop, tablet, smartphone) with a current web browser (Chrome recommended). Compatible with Windows, macOS/iOS, and Android.

## **2.5 Design and Implementation Constraints** {#2.5-design-and-implementation-constraints}

* **Design Standards Constraint:** The architecture must follow the **MVC (Model–View–Controller) structure.**
* **Security Constraint:** User passwords shall be stored using a strong one-way hashing algorithm (e.g., SHA-256).

## **2.6 User Documentation** {#2.6-user-documentation}

An integrated "Frequently Asked Questions" (FAQ) section shall be provided for simple answers to common user questions regarding the app

## **2.7 Assumptions and Dependencies** {#2.7-assumptions-and-dependencies}

The design and operation of the **Safi** web application rely on the following assumptions and dependencies:

### ***2.7.1 Assumptions*** {#2.7.1-assumptions}

**Internet Access and Browser:** All users must have a stable internet connection and a modern browser to access the application.

### ***2.7.2 Dependencies*** {#2.7.2-dependencies}

1. **Flask Framework:** The backend of the Safi system depends on the Flask framework for routing, request handling, and api development.
2. **Database System:** The application depends on a database management system(MongoDB) to store and retrieve user and system data reliably.
3. **Version Control:** the app uses Github as version controlling tool

# **3\. Specific Requirements**   {#3.-specific-requirements}

## **3.1 Functional Requirements** {#3.1-functional-requirements}

* **Registration and Login:** Users can create an account using a valid email. After that, the system must verify emails and prevent duplicates.
* **User Dashboard:** Each user has a dashboard summarizing all their groups, including names and recent transactions.
* **Group Creation / Joining:** Any user can create new groups and invite their friends to join. Also, users can request to join, and the group admin should handle join requests.
* **Group Member Management:** The admin of the group can remove members using their usernames or invite new users to the group by their emails.
* **Recording of Expense Entries:** Users can record expenses with the payer, amount, involved participants, and description. The system must update group balances accurately and simplify the total debt network.
* **Automated Debt Simplification:** Adding any new transactions or logging any settlements between users will trigger an automatic simplification of the whole debt network.
* **User Summary for Each Group:** Each user can view their net summary within each group; this summary is the final positive or negative value.
* **Settlement between Users:** Users can log settlements between each other and record the amount and date.
* **Two-Way Confirmation for Settlements:** Any settlement between any two users must require confirmation from both of them.
* **Notification System:** Users will receive notifications for any pending transactions.

## **3.2 Use Case Model** {#3.2-use-case-model}

### ***3.2.1 Use Case Diagrams***  {#3.2.1-use-case-diagrams}

***3.2.1.1 Financial Management***

***3.2.1.2 User Management***

***3.2.1.3 Teams Management***

### ***3.2.2*** **Use Cases Description**   {#3.2.2-use-cases-description}

### ***3.2.2.1 Financial Management***  {#3.2.2.1-financial-management}

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | FM-1 |
| Use Case Name | Record an Expense |
| Primary Actor | User |
| Stakeholders and Interests | Users want to log expenses accurately and quickly.  |
| Preconditions | The user is logged in and part of at least one group. |
| Postconditions | Expense is added, and balances are updated for all group members. |
| Main Success Scenario (Basic Flow) | 1\. The user selects a group. 2\. Enters expense amount, payer, and participants. 3\. Confirms and saves. 4\. The system recalculates balances. |
| Extensions (Alternative Flows) | Invalid input → show validation error |
| Includes / Extends (Relationships) | Includes “Simplify Money Network.” |
| Special Requirements | Real-time update of balances |
| Assumptions | Active group session |
| Frequency of Use | High — used whenever new expenses occur. |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | FM-2 |
| Use Case Name | Simplify Money Network |
| Primary Actor | System |
| Stakeholders and Interests | Users want minimal transactions for debt settlement. The system ensures fairness and transparency. |
| Preconditions | The group has at least one expense logged |
| Postconditions | The system generates optimized settlement transactions. |
| Main Success Scenario (Basic Flow) | 1\. The user requests “Simplify debts.” 2\. The system analyzes net balances. 3\. Generates a minimal set of transactions. 4\. Displays results to the user. |
| Extensions (Alternative Flows) | No expenses → notify user “No debts to simplify.” |
| Includes / Extends (Relationships) | Includes “Record an Expense.” |
| Special Requirements | Algorithm efficiency. |
| Assumptions | User balances are stored accurately. |
| Frequency of Use | Moderate — once per settlement cycle. |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | FM-3 |
| Use Case Name | Settle Up Debt |
| Primary Actor | User |
| Stakeholders and Interests | Users want to confirm and record payments securely. |
| Preconditions | Simplified transactions have been generated. |
| Postconditions | Settlement confirmed and recorded in the database. |
| Main Success Scenario (Basic Flow) | 1\. The user selects a person to pay. 2\. Enters amount. 3\. System updates records. |
| Extensions (Alternative Flows) |  |
| Includes / Extends (Relationships) | Extends “Simplify Money Network.” |
| Special Requirements | Two-way verification. |
| Assumptions | Both users exist.  |
| Frequency of Use | Moderate.  |

***3.2.2.2 User Management***

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | UM-1 |
| Use Case Name | Log In & Verify Email. |
| Primary Actor | User |
| Stakeholders and Interests | Users want secure and easy access. The system must ensure that verified users only. |
| Preconditions | User account exists. |
| Postconditions | User successfully authenticated. |
| Main Success Scenario (Basic Flow) | 1\. The user enters an email and a password. 2\. System verifies credentials. 3\. Send a verification link if not verified. 4\. Grants access. |
| Extensions (Alternative Flows) | Invalid credentials → show error(invalid Email or password). |
| Includes / Extends (Relationships) | Includes “Verify Email.” |
| Special Requirements | Secure password handling. |
| Assumptions | Email service is operational. |
| Frequency of Use | High — each login session. |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | UM-2 |
| Use Case Name | Check Group Summary. |
| Primary Actor | User |
| Stakeholders and Interests | Users need a clear overview of group balances and transactions. |
| Preconditions | The user is part of at least one group. |
| Postconditions | The system displays the expense summary. |
| Main Success Scenario (Basic Flow) | 1\. The user selects a group. 2\. The system retrieves group data. 3\. Displays expenses, balances, and transactions. |
| Extensions (Alternative Flows) | Data not found → show “No records available.” |
| Includes / Extends (Relationships) |  |
| Special Requirements |  |
| Assumptions | Database connection is stable. |
| Frequency of Use | High.  |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | UM-3 |
| Use Case Name | Accept / Reject Group Invite |
| Primary Actor | User  |
| Stakeholders and Interests | Users want control over joining groups; group admins need confirmation. |
| Preconditions | The user has received an invite. |
| Postconditions | User joins or declines the group. |
| Main Success Scenario (Basic Flow) | 1\. User receives group invite. 2\. Accepts or rejects. 3\. System updates group membership. |
| Extensions (Alternative Flows) | Invite expired → notify user. |
| Includes / Extends (Relationships) | Extends “Create / Join Group.” |
| Special Requirements | Secure link validation. |
| Assumptions | The invited user has an account.  |
| Frequency of Use | Moderate. |

***3.2.2.3 Teams Management***

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | TM-1 |
| Use Case Name | Create / Join Group |
| Primary Actor | User |
| Stakeholders and Interests | Users want to manage groups efficiently; the system ensures unique IDs and secure joins. |
| Preconditions | The user is logged in. |
| Postconditions | New group created or user added to an existing one. |
| Main Success Scenario (Basic Flow) | 1\. The user selects “Create Group” or “Join Group.” 2\. System validates name or invite code. 3\. Updates membership list. |
| Extensions (Alternative Flows) |  |
| Includes / Extends (Relationships) | Includes “Verify Authority.” |
| Special Requirements | Unique group ID. |
| Assumptions | Database connection.  |
| Frequency of Use | Moderate.  |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | TM-2 |
| Use Case Name | Invite / Remove Users |
| Primary Actor | Group Admin |
| Stakeholders and Interests | Admins manage membership; users want notifications and control |
| Preconditions | The group exists, and the user is an admin. |
| Postconditions | User list updated. |
| Main Success Scenario (Basic Flow) | 1\. Admin opens group settings. 2\. Adds or removes a user. 3\. System updates group data. |
| Extensions (Alternative Flows) | User already exists → error |
| Includes / Extends (Relationships) | Extends “Create / Join Group. |
| Special Requirements | Secure authorization check. |
| Assumptions |  |
| Frequency of Use | Moderate. |

| Template Section | Purpose / Notes |
| ----- | ----- |
| Use Case ID | TM-3 |
| Use Case Name | Verify Authority |
| Primary Actor | System |
| Stakeholders and Interests | Ensures only authorized actions are performed. |
| Preconditions | The user attempts an admin action. |
| Postconditions | Permission granted or denied |
| Main Success Scenario (Basic Flow) | 1\. The user requests an action. 2\. System checks role. 3\. Approves or rejects. |
| Extensions (Alternative Flows) | Unauthorized → error message. |
| Includes / Extends (Relationships) | Included in multiple admin actions. |
| Special Requirements | Role-based access enforcement. |
| Assumptions | User roles defined. |
| Frequency of Use | High — during every admin operation. |

## **3.3 Domain Model** {#3.3-domain-model}

### ***3.3.1*** **Conceptual Class Diagram**  {#3.3.1-conceptual-class-diagram}

### ***3.3.2*** **Class Descriptions** {#3.3.2-class-descriptions}

| Class Name  | Description | Key Attributes | Associations |
| :---: | ----- | ----- | ----- |
| User | Represents a real-world person using the system to share expenses within groups | user\_id, name, email, phone\_number | \- Belongs to one or more Groups \- Records multiple Expenses \- Involved in multiple Debts (owes/is owed) \- Sends and receives Transactions \- Receives Notifications |
| Group | A set of users who share expenses together (e.g., friends, roommates, trip group) | group\_id, group\_name, description, members, invitations, debts | \- Contains multiple Users \- Contains multiple Expenses \- Generates multiple Debt |
| Expense | Represents a real-world expense paid by one user on behalf of others. | payer\_user\_id, involved\_users, amount, currency, timestamp, description | \- Created by one User \- Involves multiple Users \- Belongs to one Group \- Generates Debts |
| Debt | Represents money one user owes to another due to shared expenses. | from\_user\_id, to\_user\_id, amount, currency, group\_id, confirmation\_status | \- Occurs between two Users \- Belongs to one Group \- May be settled through Transactions |
| Transaction | Represents a payment from one user to another to settle or reduce debt. | transaction\_id, from\_user\_id, to\_user\_id, amount, date, status | \- Occurs between two Users \- Used to settle one or more Debts |
| Notification | A message sent to a user informing them about group activities or financial events. | notification\_id, message, timestamp, is\_read\_status | \- Sent to one User \- A User may receive many Notifications |

##

## **3.4 Non-Functional Requirements** {#3.4-non-functional-requirements}

**NFR1 – Usability:** The system shall be easy to understand and operate.

**How to Test:**

* Conduct usability testing where users perform core tasks (create group, add expense).
* Requirement is met if most users complete tasks without assistance

**NFR2 – Security:** The system shall protect user data and allow access only to authorized users.

**How to Test:**

* Perform security tests to verify that unauthorized requests are rejected.
* Confirm all data transmission uses HTTPS.

## **3.5 External Interface Requirements** {#3.5-external-interface-requirements}

###   ***3.5.1 User Interface***  {#3.5.1-user-interface}

* **User Account Screens:** Register, login, and password management forms.
* **Group Page:** displays group expenses, members, and the user’s net balance.
* **Expense Entry:** clear form for adding new expenses (amount, description, payer, and participants).

      ***3.5.2 Hardware Interfac**e*

* **Client Devices:** Runs on any standard device with a modern web browser
* **Database:** The backend will communicate with mongodb database for storing data.
* **Web Browser:** The frontend shall use HTML, CSS.

### ***3.5.4 Communication Interface*** {#3.5.4-communication-interface}

* **Protocol:** Use HTTPS ( web protocol and secure).
* **Security:** Credential Data must be encrypted.
* **Authentication:** All api routes must have a valid user session.

**API Structure:** The application uses a structured api used by the web client for all operations

**4\. Appendices**

## **4.1 Appendix A: Data Dictionary**   {#4.1-appendix-a:-data-dictionary}

## **4.2 Appendix B: Glossary**  {#4.2-appendix-b:-glossary}

| Flask  | Python backend Framework  |
| :---- | :---- |
| **Mongo**  | No SQL database to manage storing and retrieving data  |
