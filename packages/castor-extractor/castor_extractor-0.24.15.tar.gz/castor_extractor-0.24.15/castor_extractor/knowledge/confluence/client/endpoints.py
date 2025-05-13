class ConfluenceEndpointFactory:
    """
    Confluence rest api v2 endpoint factory.
    https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about
    """

    API = "wiki/api/v2/"
    PAGES = "pages"
    SPACES = "spaces"
    USERS = "users-bulk"

    @classmethod
    def pages(cls, space_id: str) -> str:
        """
        Endpoint to fetch all pages in the given space.
        More: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-spaces-id-pages-get
        """
        return f"{cls.API}{cls.SPACES}/{space_id}/{cls.PAGES}?body-format=atlas_doc_format"

    @classmethod
    def spaces(cls) -> str:
        """
        Endpoint to fetch all spaces.
        https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get
        """
        return f"{cls.API}{cls.SPACES}"

    @classmethod
    def users(cls) -> str:
        """
        Endpoint to fetch all user.
        More: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-user/#api-users-bulk-post
        """
        return f"{cls.API}{cls.USERS}"
