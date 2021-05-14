# HTTP

- The Hyper Text Transfer Protocol (HTTP) is a stateless Application Layer protocol which operates at port 80 and is one of the most widely used protocols for data communication over the internet.
- The Hyper Text Transfer Protocol Secure (HTTPS) is the secure form of HTTP which provides data encryption and authenticity of communication and operates at port 443. The security is provided by [TLS](tls.md).
- HTTP follows a request-response cycle, where the client requests something for the server (or responding maching) and the server sends back a response.
- The most widely used version of HTTP is HTTP/1.1. HTTP/2 is catching up and HTTP/3 (HTTP over QUIC) is the newest version.
- [What is HTTP?](https://www.youtube.com/watch?v=0OrmKCB0UrQ)
- [HTTP crash course.](https://www.youtube.com/watch?v=iYM2zFP3Zn0)


## HTTP methods

HTTP provides certain request methods to the client to state the action of their request on the server.

### GET

- Get/fetch data from server.
- Do not use it to send data to the server, as it exposes the data (request params) in the URL.
- Limitation on size of data that can be sent.

### POST

- Add data (Send data to the server.)
- Secure as it does not expose data (request params) in the URL like [GET](#get).
- No limitation on th size of data.

### PUT

- Update data

### DELETE

- Delete data

### PATCH

- Update data

### OPTIONS

- It is used to ask the server the options that are allowed (allowed headers and their options, methods, etc).
- It is used in the preflight request in `fetch` by the browser.

### CONNECT

- Starts a two-way tunnel with the target. It can be used to open a tunnel.
- This method converts the request connection to a transparent TCP/IP tunnel, usually to facilitate TLS encrypted communication (HTTPS) through an unencrypted HTTP proxy. (Source: TechMax)

### TRACE

- It performs a message loop-back test along the path to the target resource, providing a useful debugging mechanism. (Source: [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/TRACE))
   - It echoes the received request and the client can check if any changes have been made to it by intermediate servers. (Source: TechMax)

### HEAD

- It requests the headers that would be returned if the HEAD request's URL was instead requested with the [GET method](#get).
- A response to a HEAD method should not have a body. If it has one anyway, that body must be ignored. (Source: [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD))
- It is useful for retrieving meta-information written in response headers, without having to transport the content. (Source: TechMax)


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

### Client errors

- 400 Bad Request
   - Indicates that there was a client error like a malformed request syntax, an invalid request message framing or a deceptive request routing.
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
   - The user has sent too many requests in a given amount of time (rate limiting).

### Server errors

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
