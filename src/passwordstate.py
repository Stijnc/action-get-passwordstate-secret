import json
import urllib.error
import urllib.parse
import urllib.request
import warnings
from typing import Dict


class PasswordIdException(Exception):
    msg = "Either the password id or the match field id and value must be configured"


class Passwordstate(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_password_fields(self, password):
        """ get the password fields """
        if password.type == "password_id":
            return self._get_password_by_id(password.password_id)
        elif password.type == "match_field":
            return self._get_password_by_field(password)

    def _get_password_by_id(self, password_id):
        """ get the password by the password id """
        passwords = self._request("passwords/" + str(password_id), "GET")
        if len(passwords) == 0:
            warnings.warn("Password not found")
            return None
        if len(passwords) > 1:
            warnings.warn("Multiple matching passwords found")
            return None
        return passwords[0]

    def _get_password_by_field(self, password):
        """ get the password by a specific field """
        return self._get_password_by_id(self._get_password_id(password))

    def _get_password_id(self, password):
        """ get the password id by using a specific field """
        uri = (
            "passwords/" + password.password_list_id + "?QueryAll&ExcludePassword=true"
        )
        passwords = self._request(uri, "GET")
        passwords = Passwordstate._filter_passwords(
            passwords, password.match_field, password.match_field_id
        )
        if len(passwords) == 0:
            warnings.warn("Password not found")
            return None
        elif len(passwords) > 1:
            warnings.warn("Multiple matching passwords found")
            return None

        return passwords[0]["PasswordID"]

    def _request(self, uri, method, params=None):
        """ send a request to the api and return as json """
        response = self._raw_request(uri, method, params)
        if response is False:
            return []
        return json.loads(response)

    def _raw_request(self, uri, method, params=None):
        """ send a request to the api and return the raw response """
        request = self._create_request(uri, method)
        try:
            if params:
                response = urllib.request.urlopen(
                    request, urllib.parse.quote_plus(params)
                ).read()
            else:
                response = urllib.request.urlopen(request).read()
        except urllib.error.URLError as inst:
            msg = str(inst)
            if "No Passwords found in the Password Lists for PasswordListID of" in msg:
                return False
            else:
                warnings.warn("Failed: %s" % str(inst))
                return None

        return response

    def _create_request(self, uri, method):
        """ creates a request object """
        request = urllib.request.Request(self.url + "/api/" + uri)
        request.add_header("APIKey", self.token)
        request.get_method = lambda: method
        return request

    @staticmethod
    def _filter_passwords(passwords, field, value):
        """ filter out passwords which does not match the specific field value """
        return [obj for i, obj in enumerate(passwords) if obj[field] == value]


class Password(object):

    items: Dict[str, str] = dict()

    def __init__(self, api, password_list_id, matcher):
        self.api = api
        self.password_list_id = password_list_id
        if matcher["field"] == "id" or matcher["field"] == "password_id":
            self.password_id = matcher["field_id"]
        elif (
            "field" in matcher
            and "field_id" in matcher
            and matcher["field"] is not None
            and matcher["field_id"] is not None
        ):
            self.match_field = matcher["field"]
            self.match_field_id = matcher["field_id"]
        else:
            raise PasswordIdException()
        self.items = self.api.get_password_fields(self)
        # for key, value in items.items():
        #    setattr(self, key, value)

    @property
    def password(self):
        """ fetch the password from the api """
        return self.items["Password"]

    @property
    def username(self):
        """ fetch the username from the api """
        return self.items["UserName"]
    
    @property
    def title(self):
        """ fetch the title from the api """
        return self.items["Title"]

    @property
    def type(self):
        """ the method to uniquely identify the password """
        if hasattr(self, "password_id"):
            return "password_id"
        elif hasattr(self, "match_field") and hasattr(self, "match_field_id"):
            return "match_field"
        raise PasswordIdException()
