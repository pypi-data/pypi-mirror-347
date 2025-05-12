class StatusCode:
    """
    This class contains HTTP status codes and their descriptions.
    """

    # 1xx: Informational
    CONTINUE = 100
    """
    This interim response indicates that everything so far is OK and that the client should continue with the request or ignore it if it is already finished.
    """

    SWITCHING_PROTOCOLS = 101
    """
    This code is sent in response to an Upgrade request header by the client, and indicates the protocol the server is switching to.
    """

    PROCESSING = 102
    """
    This code indicates that the server has received and is processing the request, but no response is available yet.
    """

    # 2xx: Success
    OK = 200
    """
    The request has succeeded. The meaning of a success varies depending on the HTTP method:
    GET: The resource has been fetched and is transmitted in the message body.
    HEAD: The entity headers are in the message body.
    POST: The resource describing the result of the action is transmitted in the message body.
    TRACE: The message body contains the request message as received by the server.
    """

    CREATED = 201
    """
    The request has succeeded and a new resource has been created as a result of it. This is typically the response sent after a PUT request.
    """

    ACCEPTED = 202
    """
    The request has been received but not yet acted upon. It is non-committal, meaning that there is no way in HTTP to later send an asynchronous response indicating the outcome of processing the request. It is intended for cases where another process or server handles the request, or for batch processing.
    """

    NON_AUTHORITATIVE_INFORMATION = 203
    """
    This response code means returned meta-information set is not exact set as available from the origin server, but collected from a local or a third-party copy.
    """

    NO_CONTENT = 204
    """
    There is no content to send for this request, but the headers may be useful. The user-agent may update its cached headers for this resource with the new ones.
    """

    RESET_CONTENT = 205
    """
    This response code is sent after accomplishing request to tell user agent reset document view which sent this request.
    """

    PARTIAL_CONTENT = 206
    """
    This response code is used because of range header sent by the client to separate download into multiple streams.
    """

    MULTI_STATUS = 207
    """
    A Multi-Status response conveys information about multiple resources in situations where multiple status codes might be appropriate.
    """

    # 3xx: Redirection
    MULTIPLE_CHOICES = 300
    """
    The request has more than one possible responses. User-agent or user should choose one of them. There is no standardized way to choose one of the responses.
    """

    MOVED_PERMANENTLY = 301
    """
    This response code means that URI of requested resource has been changed. Probably, new URI would be given in the response.
    """

    MOVED_TEMPORARILY = 302
    """
    This response code means that URI of requested resource has been changed temporarily. New changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.
    """

    SEE_OTHER = 303
    """
    Server sent this response to directing client to get requested resource to another URI with an GET request.
    """

    NOT_MODIFIED = 304
    """
    This is used for caching purposes. It is telling to client that response has not been modified. So, client can continue to use same cached version of response.
    """

    USE_PROXY = 305
    """
    Was defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy.
    """

    TEMPORARY_REDIRECT = 307
    """
    Server sent this response to directing client to get requested resource to another URI with same method that used prior request.
    """

    PERMANENT_REDIRECT = 308
    """
    This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header.
    """

    # 4xx: Client Error
    BAD_REQUEST = 400
    """
    This response means that server could not understand the request due to invalid syntax.
    """

    UNAUTHORIZED = 401
    """
    Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated".
    """

    PAYMENT_REQUIRED = 402
    """
    This response code is reserved for future use.
    """

    FORBIDDEN = 403
    """
    The client does not have access rights to the content.
    """

    NOT_FOUND = 404
    """
    The server can not find requested resource.
    """

    METHOD_NOT_ALLOWED = 405
    """
    The request method is known by the server but has been disabled and cannot be used.
    """

    NOT_ACCEPTABLE = 406
    """
    This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content following the criteria given by the user agent.
    """

    PROXY_AUTHENTICATION_REQUIRED = 407
    """
    This is similar to 401 but authentication is needed to be done by a proxy.
    """

    REQUEST_TIMEOUT = 408
    """
    This response is sent on an idle connection by some servers, even without any previous request by the client.
    """

    CONFLICT = 409
    """
    This response is sent when a request conflicts with the current state of the server.
    """

    GONE = 410
    """
    This response would be sent when the requested content has been permanently deleted from server.
    """

    LENGTH_REQUIRED = 411
    """
    The server rejected the request because the Content-Length header field is not defined and the server requires it.
    """

    PRECONDITION_FAILED = 412
    """
    The client has indicated preconditions in its headers which the server does not meet.
    """

    REQUEST_TOO_LONG = 413
    """
    Request entity is larger than limits defined by server.
    """

    REQUEST_URI_TOO_LONG = 414
    """
    The URI requested by the client is longer than the server is willing to interpret.
    """

    UNSUPPORTED_MEDIA_TYPE = 415
    """
    The media format of the requested data is not supported by the server.
    """

    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    """
    The range specified by the Range header field in the request can't be fulfilled.
    """

    EXPECTATION_FAILED = 417
    """
    This response code means the expectation indicated by the Expect request header field can't be met by the server.
    """

    IM_A_TEAPOT = 418
    """
    Any attempt to brew coffee with a teapot should result in the error code "418 I'm a teapot".
    """

    INSUFFICIENT_SPACE_ON_RESOURCE = 419
    """
    The 507 (Insufficient Storage) status code means the method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.
    """

    METHOD_FAILURE = 420
    """
    A deprecated response used by the Spring Framework when a method has failed.
    """

    MISDIRECTED_REQUEST = 421
    """
    Defined in the specification of HTTP/2 to indicate that a server is not able to produce a response for the combination of scheme and authority that are included in the request URI.
    """

    UNPROCESSABLE_ENTITY = 422
    """
    The request was well-formed but was unable to be followed due to semantic errors.
    """

    LOCKED = 423
    """
    The resource that is being accessed is locked.
    """

    FAILED_DEPENDENCY = 424
    """
    The request failed due to failure of a previous request.
    """

    PRECONDITION_REQUIRED = 428
    """
    The origin server requires the request to be conditional.
    """

    TOO_MANY_REQUESTS = 429
    """
    The user has sent too many requests in a given amount of time.
    """

    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    """
    The server is unwilling to process the request because its header fields are too large.
    """

    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    """
    The user-agent requested a resource that cannot legally be provided, such as a web page censored by a government.
    """

    # 5xx: Server Error
    INTERNAL_SERVER_ERROR = 500
    """
    The server encountered an unexpected condition that prevented it from fulfilling the request.
    """

    NOT_IMPLEMENTED = 501
    """
    The request method is not supported by the server and cannot be handled.
    """
