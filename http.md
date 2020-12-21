# HTTP

- The Hyper Text Transfer Protocol (HTTP) is an Application Layer protocol which operates at port 80 and is the most widely used protocol for data communication over the internet.
- The Hyper Text Transfer Protocol Secure (HTTPS) is the secure form of HTTP which provides data encryption and authenticity of communication and operates at port 443. The security is provided by [TLS](tls.md).
- HTTP follows a request-resonpse cycle, where the client requests something for the server (or responding maching) and the server sends back a response.
- [What is HTTP?](https://www.youtube.com/watch?v=0OrmKCB0UrQ)
- [HTTP crash course.](https://www.youtube.com/watch?v=iYM2zFP3Zn0)


## Common HTTP methods

HTTP provides certain request methods to the client to state the action of their request on the server.

### GET

- Get/fetch data from server.
- Exposes data in the URL.

### POST

- Add data
- Secure as it does not expose data in the URL.

### PUT

- Update data

### DELETE

- Delete data

### PATCH

- Update data

### OPTIONS

- Used in the preflight request in `fetch` by the browser to ask the server what options are allowed (allowed headers and their options, methods, etc).


## Common HTTP status codes

- HTTP provides certain response codes to the server (or respoding machine) to explain the condition of the response, be it good or bad.
- HTTP status codes are made up of 3 digits that fall into 5 categories, with each category representing a certain class of code. ([Source](https://pythonise.com/series/learning-flask/flask-http-methods)) <br /> The first digit is the category and the 5 categories correspond to the following classes:
   - 1xx: Informational
   - 2xx: Success
   - 3xx: Redirection
   - 4xx: Client errors
   - 5xx: Server errors
- A comprehensive list (with meanings) can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) and on [httpstatuses.com](https://httpstatuses.com/).

### Success

- 200 OK
- 204 No Content
   - The server has successfully fulfilled the request and that there is no additional content to send in the response payload body.

### Redirection

- 304 Not Modified 
   - Indicates that there is no need to retransmit the requested resources.
   - It is an implicit redirection to a cached resource.
- 307 Temporary Redirect
   - The target resource resides temporarily under a different URI and the user agent MUST NOT change the request method if it performs an automatic redirection to that URI.

### Client Errors

- 400 Bad Request
   - Indicates that there was a client error like a malformed request syntax, an invalid request message framing or a deceptive request routing.
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
   - The user has sent too many requests in a given amount of time (rate limiting).

### Server Errors

- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout


## HTTP versions

- [Differences between HTTP 0.9, HTTP/1.0, HTTP/1.1, HTTP/2 and HTTP/3](https://www.youtube.com/watch?v=Kqgv4Xs8yDI&feature=emb_logo)
- [HTTP crash course - HTTP/1.0, HTTP/1.1, HTTP/2 and HTTP/3](https://www.youtube.com/watch?v=0OrmKCB0UrQ)
- [Chrome DevTools Network Tab - HTTP/1.1, HTTP/2 and HTTP/3 in action](https://www.youtube.com/watch?v=LBgfSwX4GDI)
- [More on the QUIC protocol used in HTTP/3](https://docs.google.com/document/d/1gY9-YNDNAB1eip-RTPbqphgySwSNSDHLq9D5Bty4FSU/edit)
- [HTTP crash course - Status codes, methods, headers and hands on with Node.js](https://www.youtube.com/watch?v=iYM2zFP3Zn0)
