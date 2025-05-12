class ReasonPhrase:
    """
    This class contains HTTP status codes and their descriptions.
    Official Documentation: https://tools.ietf.org/html/rfc7231#section-6
    """
    
    ACCEPTED = "Accepted"
    """
    The request has been received but not yet acted upon. 
    It is non-committal, meaning that there is no way in HTTP to later send an asynchronous response indicating the outcome of processing the request.
    It is intended for cases where another process or server handles the request, or for batch processing.
    """

    BAD_GATEWAY = "Bad Gateway"
    """
    This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.
    """

    BAD_REQUEST = "Bad Request"
    """
    This response means that server could not understand the request due to invalid syntax.
    """

    CONFLICT = "Conflict"
    """
    This response is sent when a request conflicts with the current state of the server.
    """

    CONTINUE = "Continue"
    """
    This interim response indicates that everything so far is OK and that the client should continue with the request or ignore it if it is already finished.
    """

    CREATED = "Created"
    """
    The request has succeeded and a new resource has been created as a result of it. This is typically the response sent after a PUT request.
    """

    EXPECTATION_FAILED = "Expectation Failed"
    """
    This response code means the expectation indicated by the Expect request header field can't be met by the server.
    """

    FAILED_DEPENDENCY = "Failed Dependency"
    """
    The request failed due to the failure of a previous request.
    """

    FORBIDDEN = "Forbidden"
    """
    The client does not have access rights to the content, i.e., they are unauthorized, so the server is rejecting to give a proper response. Unlike 401, the client's identity is known to the server.
    """

    GATEWAY_TIMEOUT = "Gateway Timeout"
    """
    This error response is given when the server is acting as a gateway and cannot get a response in time.
    """

    GONE = "Gone"
    """
    This response would be sent when the requested content has been permanently deleted from the server, with no forwarding address.
    Clients are expected to remove their caches and links to the resource.
    """

    HTTP_VERSION_NOT_SUPPORTED = "HTTP Version Not Supported"
    """
    The HTTP version used in the request is not supported by the server.
    """

    IM_A_TEAPOT = "I'm a teapot"
    """
    Any attempt to brew coffee with a teapot should result in the error code "418 I'm a teapot". The resulting entity body MAY be short and stout.
    """

    INSUFFICIENT_SPACE_ON_RESOURCE = "Insufficient Space on Resource"
    """
    The 507 (Insufficient Storage) status code means the method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.
    """

    INSUFFICIENT_STORAGE = "Insufficient Storage"
    """
    The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself and is therefore not a proper end point in the negotiation process.
    """

    INTERNAL_SERVER_ERROR = "Internal Server Error"
    """
    The server encountered an unexpected condition that prevented it from fulfilling the request.
    """

    LENGTH_REQUIRED = "Length Required"
    """
    The server rejected the request because the Content-Length header field is not defined and the server requires it.
    """

    LOCKED = "Locked"
    """
    The resource that is being accessed is locked.
    """

    METHOD_FAILURE = "Method Failure"
    """
    A deprecated response used by the Spring Framework when a method has failed.
    """

    METHOD_NOT_ALLOWED = "Method Not Allowed"
    """
    The request method is known by the server but has been disabled and cannot be used.
    """

    MOVED_PERMANENTLY = "Moved Permanently"
    """
    This response code means that the URI of the requested resource has been changed. Probably, a new URI would be given in the response.
    """

    MOVED_TEMPORARILY = "Moved Temporarily"
    """
    This response code means that the URI of the requested resource has been changed temporarily.
    """

    MULTI_STATUS = "Multi-Status"
    """
    A Multi-Status response conveys information about multiple resources in situations where multiple status codes might be appropriate.
    """

    MULTIPLE_CHOICES = "Multiple Choices"
    """
    The request has more than one possible response. User-agent or user should choose one of them. There is no standardized way to choose one of the responses.
    """

    NETWORK_AUTHENTICATION_REQUIRED = "Network Authentication Required"
    """
    The 511 status code indicates that the client needs to authenticate to gain network access.
    """

    NO_CONTENT = "No Content"
    """
    There is no content to send for this request, but the headers may be useful.
    """

    NON_AUTHORITATIVE_INFORMATION = "Non Authoritative Information"
    """
    This response code means returned meta-information set is not the exact set as available from the origin server, but collected from a local or a third-party copy.
    """

    NOT_ACCEPTABLE = "Not Acceptable"
    """
    This response is sent when the web server, after performing server-driven content negotiation, doesn't find any content following the criteria given by the user agent.
    """

    NOT_FOUND = "Not Found"
    """
    The server cannot find the requested resource. In the browser, this means the URL is not recognized.
    """

    NOT_IMPLEMENTED = "Not Implemented"
    """
    The request method is not supported by the server and cannot be handled.
    """

    NOT_MODIFIED = "Not Modified"
    """
    This is used for caching purposes. It is telling the client that the response has not been modified.
    """

    OK = "OK"
    """
    The request has succeeded. The meaning of a success varies depending on the HTTP method.
    """

    PARTIAL_CONTENT = "Partial Content"
    """
    This response code is used because of the range header sent by the client to separate download into multiple streams.
    """

    PAYMENT_REQUIRED = "Payment Required"
    """
    This response code is reserved for future use.
    """

    PERMANENT_REDIRECT = "Permanent Redirect"
    """
    This means that the resource is now permanently located at another URI.
    """

    PRECONDITION_FAILED = "Precondition Failed"
    """
    The client has indicated preconditions in its headers which the server does not meet.
    """

    PRECONDITION_REQUIRED = "Precondition Required"
    """
    The origin server requires the request to be conditional.
    """

    PROCESSING = "Processing"
    """
    This code indicates that the server has received and is processing the request, but no response is available yet.
    """

    PROXY_AUTHENTICATION_REQUIRED = "Proxy Authentication Required"
    """
    This is similar to 401 but authentication needs to be done by a proxy.
    """

    REQUEST_HEADER_FIELDS_TOO_LARGE = "Request Header Fields Too Large"
    """
    The server is unwilling to process the request because its header fields are too large.
    """

    REQUEST_TIMEOUT = "Request Timeout"
    """
    This response is sent on an idle connection by some servers, even without any previous request by the client.
    """

    REQUEST_TOO_LONG = "Request Entity Too Large"
    """
    Request entity is larger than the limits defined by the server.
    """

    REQUEST_URI_TOO_LONG = "Request-URI Too Long"
    """
    The URI requested by the client is longer than the server is willing to interpret.
    """

    REQUESTED_RANGE_NOT_SATISFIABLE = "Requested Range Not Satisfiable"
    """
    The range specified by the Range header field in the request can't be fulfilled.
    """

    RESET_CONTENT = "Reset Content"
    """
    This response code is sent after accomplishing a request to tell the user agent to reset the document view which sent this request.
    """

    SEE_OTHER = "See Other"
    """
    Server sent this response to direct the client to get the requested resource to another URI with a GET request.
    """

    SERVICE_UNAVAILABLE = "Service Unavailable"
    """
    The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded.
    """

    SWITCHING_PROTOCOLS = "Switching Protocols"
    """
    This code is sent in response to an Upgrade request header by the client and indicates the protocol the server is switching to.
    """

    TEMPORARY_REDIRECT = "Temporary Redirect"
    """
    The request should be repeated with another URI; however, future requests should still use the original URI.
    """

    TOO_MANY_REQUESTS = "Too Many Requests"
    """
    The user has sent too many requests in a given amount of time.
    """

    UNAUTHORIZED = "Unauthorized"
    """
    The client must authenticate itself to get the requested response.
    """

    UNPROCESSABLE_ENTITY = "Unprocessable Entity"
    """
    The server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.
    """

    UNSUPPORTED_MEDIA_TYPE = "Unsupported Media Type"
    """
    The media format of the requested data is not supported by the server.
    """

    UPGRADE_REQUIRED = "Upgrade Required"
    """
    The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol.
    """

    VARIANT_ALSO_NEGOTIATES = "Variant Also Negotiates"
    """
    The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself and is therefore not a proper end point in the negotiation process.
    """

    def __init__(self):
        raise NotImplementedError("This class is a collection of constants and should not be instantiated.")
