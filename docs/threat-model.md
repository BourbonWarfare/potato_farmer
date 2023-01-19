# `potato_farmer` Threat Model

## Project Description

This project manages `potato_field` and `potato_plants`. It's the main way to administrate 
containers; services that run in the backend to support the main application.

### User System

There will be a user system with a hierarchy of users, ranging from administrators to normal users
that have restricted access to applications. A user should be uniquely identified and should not 
be able to pose as another user.

### Backend Services

There will be a number of backend services that expose an API for other backend applications to
interact with. These backend services should **not** be exposed to the outside world; rather,
this should be managed by the API Gateway.

### API Gateway

The API Gateway takes requests from the outside world -- that is, from users and outside automated
services -- and collates data and operations from one or more backend services to satisfy the
request. The API Gateway should generally be the **only** way for users to access applications.

## Threats

### (1) User Impersonation

As users should be uniquely identified, it would violate the assumptions of our application if a
user was able to successfully pose as another user. This would possibly permit a user to access
another user's information, ruin their reputation in community spaces/applications, or utilize
privileges that they should not have access to, as described in (2).

### (2) Privilege Escalation

As there will be a hierarchy of users with varying capabilities, it should not be possible for a
user to gain additional privileges without them being granted by an administrator. Violation of
this assumption would allow ordinary users to take advantage of privileges they should not have
access to, potentially wreaking havoc regardless of malicious intent.

### (3) Direct Access to Backend Services

Backend services should not be directly accessible. Violation of this principle could permit actors
to access APIs they should not have access to, potentially wreaking havoc on internal state or
exposing data that should remain private to them.

### (4) API Gateway Overloading

As the API Gateway is the main way for users to interact with applications, it serves as a single
point of failure for the entire application. By overloading the API Gateway, malicious actors (or
just a sudden spike of traffic) can disrupt the availability of the application for all users.

### (5) Network Eavesdropping

There may be actors that are listening in on communications between our users or between services 
in our application. Through eavesdropping on network communications, malicious actors could learn
private user/system/operational data that they should not have access to. Further, they may be able
to construct spoofed requests for abuse in conjunction with Threat (3).

## Defense Mechanisms

### (1, 2) User Authentication

To protect against user impersonation, the application will utilize mechanisms of user authentication
to validate the user's identity prior to allowing access to any privileged operations or data (including
operations or data tied to user identity).

#### Password Authentication

Upon user creation, users will select a password to use for authentication. We will impose several
requirements to ensure the password is not trivially bruteforceable.

1. Minimum of 12 characters; maximum of 60 characters
2. Includes at least one number
3. Includes at least one uppercase and lowercase alphabetic character
4. Includes at least one non-alphabetic character (symbol)

These passwords will be stored in a User Authentication service. They will be salted and hashed to
protect against offline attacks if the password database were ever leaked.

* The salt will be a cryptographically random string.
* The chosen hash function will be computationally expensive to deter offline attacks.

TODO: pick hash function. `bcrypt` seems preferred nowadays? it may also handle salting?

#### Two Factor Authentication (2FA)

As user passwords may be shared between multiple services, may be bruteforceable, may be leaked 
through a variety of means, etc., our application will utilize 2FA to further validate user
identities.

TODO: mechanism? email?

### (1, 2) User Sessions

It is not practical to require users to authenticate for every request. This presents a poor UX
and is expensive for our backend services. To alleviate this pressure, we will implement user 
sessions to permit users to authenticate once and continue submitting requests for a time without
requiring authentication again.

User sessions will be implemented by a `SessionID` that is a 256 bit-string, the length chosen
to harden `SessionID`s against bruteforce attacks. These will be randomly generated with
cryptographically strong randomness. `SessionID`s will be stored in a Redis memory store alongside
a `UserID` and a session timeout. Sessions will timeout after 12 hours of inactivity.

Users will receive their 256-bit `SessionID` after successful user authentication. This will have
to be sent with every privileged request in a manner specified by the application API. The API
Gateway would check the Redis memory store to validate the `SessionID` before serving the request.
Failure to validate the `SessionID` would result in a failure which would be communicated to the user.

TODO: details of `SessionID` storage (do we want to use Redis?), details of timeout

### (3) Internal Docker Network

Backend services will operate within an internal Docker network that would not have exposed ports
to the outside world. Only the API Gateway would be publicly accessible. This should prevent
outside access of restricted backend services and force users to use the API Gateway to interact
with applications.

TODO: clarify details

### (4) Rate Limiting

As the application continues to grow in scale, users will be rate limited and the API Gateway will
not serve requests beyond the rate limit. If a user repeatedly violates the rate limiting rules,
the user will be banned and the source IP will be blacklisted, and users will have to appeal to an
administrator.

The rate limiting rules are as follows, per source IP (and logical user if a `SessionID` or login
details are provided):

* Maximum of ten requests per second
* First violation results in an immediate warning responses without fulfilling any requests for the
  next minute
* Second violation results in a one-minute timeout (one violation response to violating request and
  then no responses for duration of timeout)
* Third violation results in a one-hour timeout (one violation response to violating request and
  then no responses for duration of timeout)
* Fourth violation results in a ban
    * Source IP is blacklisted and logical user is marked as banned (if possible)
* A violation is disregarded after three days
    * i.e., a third violation will be lowered to a second violation after three days

The API Gateway will be responsible for recording the information required to enforce these rules,
as well as implementing the enforcement mechanisms.

TODO: look at how bigtech companies do this

### (5) TLS/SSL

All user-application communications and backend-service communications will utilize TLS/SSL for TCP
connections, and some other encryption mechanism for relevant UDP datagrams, to ensure that private
user/system/operational data is not leaked to external eavesdroppers. Thanks to Mechanism (3), it
should not be possible for eavesdroppers to have access to private backend service communications,
but these should still be encrypted as much as possible regardless to ensure a layered defense.

TODO: UDP encryption? should more details, e.g. about certs, be included here?
