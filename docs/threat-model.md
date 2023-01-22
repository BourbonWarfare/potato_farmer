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

Upon user creation, users will select a password to use for authentication. If possible, we should 
include a password strength meter to help users choose a strong password. We will impose several 
requirements to ensure the password is not trivially bruteforceable.

1. Minimum of 12 characters; maximum of 60 characters
2. Includes at least one number
3. Includes at least one uppercase and lowercase alphabetic character
4. Includes at least one non-alphabetic character (symbol)

These passwords will be stored in a User Authentication service. The modern algorithm Argon2id is
considering the most secure and correct to use in modern applications, but is resource-heavy. All
passwords should be salted, but Argon2id should handle this itself. Password hashes should be
compared using only safe functions that have been vetted by security experts.

#### Two Factor Authentication (2FA)

As user passwords may be shared between multiple services, may be bruteforceable, may be leaked 
through a variety of means, etc., our application will utilize 2FA to further validate user
identities. This 2FA mechanism will be opt-in and will utilize email to send a user a six-digit 
one-time code to be validated after username/password validation succeeds. Bypassing this mechanism
requires malicious actors to also have access to the user's email.

### (1, 2) User Sessions

It is not practical to require users to authenticate for every request. This presents a poor UX
and is expensive for our backend services. To alleviate this pressure, we will implement user 
sessions to permit users to authenticate once and continue submitting requests for a time without
requiring authentication again.

User sessions will be implemented by a `SessionID` that is a 128-bit string, the length chosen
to harden `SessionID`s against bruteforce attacks. These will be randomly generated with
cryptographically strong randomness. `SessionID`s will be stored in a Redis memory store alongside
a `UserID` and a session timeout. Sessions will have an idle timeout of 1 hour and an absolute 
timeout of 1 day after authentication. We could consider introducing a renewal timeout as well,
but this would add additional complexity.

Users will receive their 128-bit `SessionID` after successful user authentication. This will have
to be sent with every privileged request in a manner specified by the application API. The API
Gateway would check the Redis memory store to validate the `SessionID` before serving the request.
Failure to validate the `SessionID` would result in a failure which would be communicated to the user.

Note that as `SessionID`s will be sent as a HTTP Cookie, it is important to properly protect against
CSRF attacks with the proper use of CSRF tokens.

### (3) Internal Docker Network

Backend services will operate within an internal Docker network that would not have exposed ports
to the outside world. Only the API Gateway will be publicly accessible. This should prevent
outside access of restricted backend services and force users to use the API Gateway to interact
with applications.

To clarify, the API Gateway will also be containerized and will access backend service APIs through
the internal Docker network. Docker containers within the internal network will be assumed to be
trustworthy and can talk at will.

### (4) Rate Limiting

As the application continues to grow in scale, users will be rate limited and the API Gateway will
not serve requests beyond the rate limit. Rate limiting should be stricter for non-authenticated
endpoints. Users who repeatedly attempt to violate rate limiting rules should be restricted from
accessing authenticated endpoints. Anonymous actors who repeatedly attempt to violate rate limiting
rules may have their source IP banned (note that this may be problematic if many machines share a
NAT).

We may consider implementing our own rate limiting mechanisms, or using off-the-shelf solutions.
This mechanism will also likely depend on the implementation of our API Gateway.

### (5) TLS/SSL/DTLS

All user-application communications and backend-service communications will utilize TLS/SSL for TCP
connections to ensure that private user/system/operational data is not leaked to external eavesdroppers. 
Thanks to Mechanism (3), it should not be possible for eavesdroppers to have access to private 
backend service communications, but these should still be encrypted as much as possible regardless 
to ensure a layered defense.

For UDP communications, we can consider a variety of integrity mechanisms. DTLS has been advertised
as an integrity mechanism analogous to TLS for TCP, but the practical usage of this protocol may 
need more investigation.

## Appendix

Consult the [Web Security Confluence Page](https://bourbonwarfare.atlassian.net/wiki/spaces/~62fd97fc88b05653fa7d6975/pages/557057/Web+Security)
for a list of some of the sources consulted in the making of this document, as well as a list of
resources on how to implement some of these security mechanisms correctly.
