from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration
import httpx

class JiraApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='jira', integration=integration, **kwargs)
        self._base_url: str | None = None 

    def get_base_url(self):

        headers = self._get_headers()
        print("DEBUG: Headers being sent to Atlassian API:", headers)  # Add this line
        url = "https://api.atlassian.com/oauth/token/accessible-resources"


        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        resources=  response.json()

        if not resources:
            raise ValueError("No accessible Jira resources found for the provided credentials.")

        first_resource = resources[0]
        resource_id = first_resource.get("id")

        if not resource_id:
            raise ValueError("Could not determine the resource ID from the first accessible resource.")

        return f"https://api.atlassian.com/ex/jira/{resource_id}" 
    @property
    def base_url(self):
        """Fetches accessible resources and sets the base_url for the first resource found."""
        if self._base_url:
            return self._base_url
        self._base_url = self.get_base_url()
        return self._base_url


    @base_url.setter
    def base_url(self, value: str) -> None:
        """Sets the base URL for the Confluence API.
        
        Args:
            value (str): The base URL to set.
        """
        self._base_url = value

    def get_banner(self) -> dict[str, Any]:
        """
        Retrieves the configuration of the announcement banner using the Jira Cloud API.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Announcement banner, important
        """
        url = f"{self.base_url}/rest/api/3/announcementBanner"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_banner(self, isDismissible=None, isEnabled=None, message=None, visibility=None) -> Any:
        """
        Updates the announcement banner configuration in Jira Cloud, including message, visibility, and dismissal settings.

        Args:
            isDismissible (boolean): Flag indicating if the announcement banner can be dismissed by the user.
            isEnabled (boolean): Flag indicating if the announcement banner is enabled or not.
            message (string): The text on the announcement banner.
            visibility (string): Visibility of the announcement banner. Can be public or private.
                Example:
                ```json
                {
                  "isDismissible": false,
                  "isEnabled": true,
                  "message": "This is a public, enabled, non-dismissible banner, set using the API",
                  "visibility": "public"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Announcement banner
        """
        request_body = {
            'isDismissible': isDismissible,
            'isEnabled': isEnabled,
            'message': message,
            'visibility': visibility,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/announcementBanner"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_custom_fields_configurations(self, fieldIdsOrKeys, id=None, fieldContextId=None, issueId=None, projectKeyOrId=None, issueTypeId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves and filters a list of custom field context configurations in Jira based on specified criteria like field ID, project, or issue type, returning paginated results.

        Args:
            fieldIdsOrKeys (array): List of IDs or keys of the custom fields. It can be a mix of IDs and keys in the same query.
                Example:
                ```json
                {
                  "fieldIdsOrKeys": [
                    "customfield_10035",
                    "customfield_10036"
                  ]
                }
                ```
            id (array): The list of configuration IDs. To include multiple configurations, separate IDs with an ampersand: `id=10000&id=10001`. Can't be provided with `fieldContextId`, `issueId`, `projectKeyOrId`, or `issueTypeId`.
            fieldContextId (array): The list of field context IDs. To include multiple field contexts, separate IDs with an ampersand: `fieldContextId=10000&fieldContextId=10001`. Can't be provided with `id`, `issueId`, `projectKeyOrId`, or `issueTypeId`.
            issueId (integer): The ID of the issue to filter results by. If the issue doesn't exist, an empty list is returned. Can't be provided with `projectKeyOrId`, or `issueTypeId`.
            projectKeyOrId (string): The ID or key of the project to filter results by. Must be provided with `issueTypeId`. Can't be provided with `issueId`.
            issueTypeId (string): The ID of the issue type to filter results by. Must be provided with `projectKeyOrId`. Can't be provided with `issueId`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field configuration (apps)
        """
        request_body = {
            'fieldIdsOrKeys': fieldIdsOrKeys,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/app/field/context/configuration/list"
        query_params = {k: v for k, v in [('id', id), ('fieldContextId', fieldContextId), ('issueId', issueId), ('projectKeyOrId', projectKeyOrId), ('issueTypeId', issueTypeId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_multiple_custom_field_values(self, generateChangelog=None, updates=None) -> Any:
        """
        Updates the value of a custom field added by a Forge app on one or more Jira issues.

        Args:
            generateChangelog (boolean): Whether to generate a changelog for this update.
            updates (array): updates
                Example:
                ```json
                {
                  "updates": [
                    {
                      "customField": "customfield_10010",
                      "issueIds": [
                        10010,
                        10011
                      ],
                      "value": "new value"
                    },
                    {
                      "customField": "customfield_10011",
                      "issueIds": [
                        10010
                      ],
                      "value": 1000
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue custom field values (apps)
        """
        request_body = {
            'updates': updates,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/app/field/value"
        query_params = {k: v for k, v in [('generateChangelog', generateChangelog)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_custom_field_configuration(self, fieldIdOrKey, id=None, fieldContextId=None, issueId=None, projectKeyOrId=None, issueTypeId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves the configuration of a custom field context in Jira using the provided field ID or key, optionally filtered by specific IDs, field context IDs, issue IDs, project keys or IDs, or issue types, and returns a paginated list of configurations.

        Args:
            fieldIdOrKey (string): fieldIdOrKey
            id (array): The list of configuration IDs. To include multiple configurations, separate IDs with an ampersand: `id=10000&id=10001`. Can't be provided with `fieldContextId`, `issueId`, `projectKeyOrId`, or `issueTypeId`.
            fieldContextId (array): The list of field context IDs. To include multiple field contexts, separate IDs with an ampersand: `fieldContextId=10000&fieldContextId=10001`. Can't be provided with `id`, `issueId`, `projectKeyOrId`, or `issueTypeId`.
            issueId (integer): The ID of the issue to filter results by. If the issue doesn't exist, an empty list is returned. Can't be provided with `projectKeyOrId`, or `issueTypeId`.
            projectKeyOrId (string): The ID or key of the project to filter results by. Must be provided with `issueTypeId`. Can't be provided with `issueId`.
            issueTypeId (string): The ID of the issue type to filter results by. Must be provided with `projectKeyOrId`. Can't be provided with `issueId`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field configuration (apps)
        """
        if fieldIdOrKey is None:
            raise ValueError("Missing required parameter 'fieldIdOrKey'")
        url = f"{self.base_url}/rest/api/3/app/field/{fieldIdOrKey}/context/configuration"
        query_params = {k: v for k, v in [('id', id), ('fieldContextId', fieldContextId), ('issueId', issueId), ('projectKeyOrId', projectKeyOrId), ('issueTypeId', issueTypeId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_custom_field_configuration(self, fieldIdOrKey, configurations) -> Any:
        """
        Updates the configuration of a custom field context in Jira using the provided field ID or key.

        Args:
            fieldIdOrKey (string): fieldIdOrKey
            configurations (array): The list of custom field configuration details.
                Example:
                ```json
                {
                  "configurations": [
                    {
                      "id": "10000"
                    },
                    {
                      "configuration": {
                        "maxValue": 10000,
                        "minValue": 0
                      },
                      "id": "10001",
                      "schema": {
                        "properties": {
                          "amount": {
                            "type": "number"
                          },
                          "currency": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "amount",
                          "currency"
                        ]
                      }
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue custom field configuration (apps)
        """
        if fieldIdOrKey is None:
            raise ValueError("Missing required parameter 'fieldIdOrKey'")
        request_body = {
            'configurations': configurations,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/app/field/{fieldIdOrKey}/context/configuration"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_custom_field_value(self, fieldIdOrKey, generateChangelog=None, updates=None) -> Any:
        """
        Updates the value of a custom field for an issue using the Jira API, but this endpoint is limited to working with fields provided by Forge apps.

        Args:
            fieldIdOrKey (string): fieldIdOrKey
            generateChangelog (boolean): Whether to generate a changelog for this update.
            updates (array): The list of custom field update details.
                Example:
                ```json
                {
                  "updates": [
                    {
                      "issueIds": [
                        10010
                      ],
                      "value": "new value"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue custom field values (apps)
        """
        if fieldIdOrKey is None:
            raise ValueError("Missing required parameter 'fieldIdOrKey'")
        request_body = {
            'updates': updates,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/app/field/{fieldIdOrKey}/value"
        query_params = {k: v for k, v in [('generateChangelog', generateChangelog)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_application_property(self, key=None, permissionLevel=None, keyFilter=None) -> list[Any]:
        """
        Retrieves application properties with optional filtering by key, permission level, or key filter.

        Args:
            key (string): The key of the application property.
            permissionLevel (string): The permission level of all items being returned in the list.
            keyFilter (string): When a `key` isn't provided, this filters the list of results by the application property `key` using a regular expression. For example, using `jira.lf.*` will return all application properties with keys that start with *jira.lf.*.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Jira settings
        """
        url = f"{self.base_url}/rest/api/3/application-properties"
        query_params = {k: v for k, v in [('key', key), ('permissionLevel', permissionLevel), ('keyFilter', keyFilter)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_advanced_settings(self) -> list[Any]:
        """
        The API retrieves Jira's advanced settings properties, returning configuration details displayed on the "General Configuration > Advanced Settings" page.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Jira settings
        """
        url = f"{self.base_url}/rest/api/3/application-properties/advanced-settings"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_application_property(self, id, id_body=None, value=None) -> dict[str, Any]:
        """
        Updates a specific Jira application property identified by its ID using a PUT request.

        Args:
            id (string): id
            id_body (string): The ID of the application property.
            value (string): The new value.
                Example:
                ```json
                {
                  "id": "jira.home",
                  "value": "/var/jira/jira-home"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Jira settings
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'id': id_body,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/application-properties/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_application_roles(self) -> list[Any]:
        """
        Retrieves information about application roles using the Jira Cloud API and returns data relevant to the specified application roles.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Application roles
        """
        url = f"{self.base_url}/rest/api/3/applicationrole"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_application_role(self, key) -> dict[str, Any]:
        """
        Retrieves details of a specific application role in Jira Cloud using the provided `key` parameter via the GET method.

        Args:
            key (string): key

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Application roles
        """
        if key is None:
            raise ValueError("Missing required parameter 'key'")
        url = f"{self.base_url}/rest/api/3/applicationrole/{key}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_attachment_content(self, id, redirect=None) -> list[Any]:
        """
        Retrieves the contents of a Jira Cloud attachment by ID and returns the binary file data or a redirect URL.

        Args:
            id (string): id
            redirect (boolean): Whether a redirect is provided for the attachment download. Clients that do not automatically follow redirects can set this to `false` to avoid making multiple requests to download the attachment.

        Returns:
            list[Any]: Returned if the request is successful when `redirect` is set to `false`.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/content/{id}"
        query_params = {k: v for k, v in [('redirect', redirect)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_attachment_meta(self) -> dict[str, Any]:
        """
        Retrieves Jira's attachment settings, including whether attachments are enabled and the maximum allowed upload size.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue attachments
        """
        url = f"{self.base_url}/rest/api/3/attachment/meta"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_attachment_thumbnail(self, id, redirect=None, fallbackToDefault=None, width=None, height=None) -> list[Any]:
        """
        Retrieves a thumbnail image for a specified attachment ID in Jira, supporting optional parameters for dimensions and redirect behavior.

        Args:
            id (string): id
            redirect (boolean): Whether a redirect is provided for the attachment download. Clients that do not automatically follow redirects can set this to `false` to avoid making multiple requests to download the attachment.
            fallbackToDefault (boolean): Whether a default thumbnail is returned when the requested thumbnail is not found.
            width (integer): The maximum width to scale the thumbnail to.
            height (integer): The maximum height to scale the thumbnail to.

        Returns:
            list[Any]: Returned if the request is successful when `redirect` is set to `false`.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/thumbnail/{id}"
        query_params = {k: v for k, v in [('redirect', redirect), ('fallbackToDefault', fallbackToDefault), ('width', width), ('height', height)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_attachment(self, id) -> Any:
        """
        Deletes an attachment from a Jira issue by its ID and returns a success status upon removal.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_attachment(self, id) -> dict[str, Any]:
        """
        Retrieves metadata for a specific attachment in Jira using the provided attachment ID.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def expand_attachment_for_humans(self, id) -> dict[str, Any]:
        """
        Retrieves human-readable metadata for a specific Jira Cloud attachment in an expanded format.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful. If an empty list is returned in the response, the attachment is empty, corrupt, or not an archive.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/{id}/expand/human"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def expand_attachment_for_machines(self, id) -> dict[str, Any]:
        """
        Retrieves the contents metadata for an expanded attachment in Jira Cloud using the "GET /rest/api/3/attachment/{id}/expand/raw" endpoint, suitable for processing without presenting the data to users.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful. If an empty list is returned in the response, the attachment is empty, corrupt, or not an archive.

        Tags:
            Issue attachments
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/attachment/{id}/expand/raw"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_audit_records(self, offset=None, limit=None, filter=None, from_=None, to=None) -> dict[str, Any]:
        """
        Retrieves Jira audit records with filtering by parameters like date range, text, and category, returning activity logs of administrative actions and changes.

        Args:
            offset (integer): The number of records to skip before returning the first result.
            limit (integer): The maximum number of results to return.
            filter (string): The strings to match with audit field content, space separated.
            from_ (string): The date and time on or after which returned audit records must have been created. If `to` is provided `from` must be before `to` or no audit records are returned.
            to (string): The date and time on or before which returned audit results must have been created. If `from` is provided `to` must be after `from` or no audit records are returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Audit records
        """
        url = f"{self.base_url}/rest/api/3/auditing/record"
        query_params = {k: v for k, v in [('offset', offset), ('limit', limit), ('filter', filter), ('from', from_), ('to', to)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_system_avatars(self, type) -> dict[str, Any]:
        """
        Retrieves a list of system avatar details for a specified owner type (e.g., user, project, issue type) via the Jira Cloud REST API.

        Args:
            type (string): type

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        url = f"{self.base_url}/rest/api/3/avatar/{type}/system"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_delete(self, selectedIssueIdsOrKeys, sendBulkNotification=None) -> dict[str, Any]:
        """
        Deletes multiple Jira issues in a single request using the Bulk Delete API.

        Args:
            selectedIssueIdsOrKeys (array): List of issue IDs or keys which are to be bulk deleted. These IDs or keys can be from different projects and issue types.
            sendBulkNotification (boolean): A boolean value that indicates whether to send a bulk change notification when the issues are being deleted.

        If `true`, dispatches a bulk notification email to users about the updates.
                Example:
                ```json
                {
                  "selectedIssueIdsOrKeys": [
                    "10001",
                    "10002"
                  ],
                  "sendBulkNotification": false
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'selectedIssueIdsOrKeys': selectedIssueIdsOrKeys,
            'sendBulkNotification': sendBulkNotification,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_bulk_editable_fields(self, issueIdsOrKeys, searchText=None, endingBefore=None, startingAfter=None) -> dict[str, Any]:
        """
        Retrieves a list of fields that can be edited in bulk for specified Jira issues, allowing for the identification of editable fields for bulk operations using query parameters such as issue IDs or keys, search text, and pagination options.

        Args:
            issueIdsOrKeys (string): The IDs or keys of the issues to get editable fields from.
            searchText (string): (Optional)The text to search for in the editable fields.
            endingBefore (string): (Optional)The end cursor for use in pagination.
            startingAfter (string): (Optional)The start cursor for use in pagination.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        url = f"{self.base_url}/rest/api/3/bulk/issues/fields"
        query_params = {k: v for k, v in [('issueIdsOrKeys', issueIdsOrKeys), ('searchText', searchText), ('endingBefore', endingBefore), ('startingAfter', startingAfter)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_edit(self, editedFieldsInput, selectedActions, selectedIssueIdsOrKeys, sendBulkNotification=None) -> dict[str, Any]:
        """
        Edits multiple Jira issues in bulk by updating fields using the Jira Cloud API.

        Args:
            editedFieldsInput (string): An object that defines the values to be updated in specified fields of an issue. The structure and content of this parameter vary depending on the type of field being edited. Although the order is not significant, ensure that field IDs align with those in selectedActions.
            selectedActions (array): List of all the field IDs that are to be bulk edited. Each field ID in this list corresponds to a specific attribute of an issue that is set to be modified in the bulk edit operation. The relevant field ID can be obtained by calling the Bulk Edit Get Fields REST API (documentation available on this page itself).
            selectedIssueIdsOrKeys (array): List of issue IDs or keys which are to be bulk edited. These IDs or keys can be from different projects and issue types.
            sendBulkNotification (boolean): A boolean value that indicates whether to send a bulk change notification when the issues are being edited.

        If `true`, dispatches a bulk notification email to users about the updates.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'editedFieldsInput': editedFieldsInput,
            'selectedActions': selectedActions,
            'selectedIssueIdsOrKeys': selectedIssueIdsOrKeys,
            'sendBulkNotification': sendBulkNotification,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/fields"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_move(self, sendBulkNotification=None, targetToSourcesMapping=None) -> dict[str, Any]:
        """
        Moves multiple issues from one Jira project to another using the POST method.

        Args:
            sendBulkNotification (boolean): A boolean value that indicates whether to send a bulk change notification when the issues are being moved.

        If `true`, dispatches a bulk notification email to users about the updates.
            targetToSourcesMapping (object): An object representing the mapping of issues and data related to destination entities, like fields and statuses, that are required during a bulk move.

        The key is a string that is created by concatenating the following three entities in order, separated by commas. The format is `<project ID or key>,<issueType ID>,<parent ID or key>`. It should be unique across mappings provided in the payload. If you provide multiple mappings for the same key, only one will be processed. However, the operation won't fail, so the error may be hard to track down.

         *  ***Destination project*** (Required): ID or key of the project to which the issues are being moved.
         *  ***Destination issueType*** (Required): ID of the issueType to which the issues are being moved.
         *  ***Destination parent ID or key*** (Optional): ID or key of the issue which will become the parent of the issues being moved. Only required when the destination issueType is a subtask.
                Example:
                ```json
                {
                  "sendBulkNotification": true,
                  "targetToSourcesMapping": {
                    "PROJECT-KEY,10001": {
                      "inferClassificationDefaults": false,
                      "inferFieldDefaults": false,
                      "inferStatusDefaults": false,
                      "inferSubtaskTypeDefault": true,
                      "issueIdsOrKeys": [
                        "ISSUE-1"
                      ],
                      "targetClassification": [
                        {
                          "classifications": {
                            "5bfa70f7-4af1-44f5-9e12-1ce185f15a38": [
                              "bd58e74c-c31b-41a7-ba69-9673ebd9dae9",
                              "-1"
                            ]
                          }
                        }
                      ],
                      "targetMandatoryFields": [
                        {
                          "fields": {
                            "customfield_10000": {
                              "retain": false,
                              "type": "raw",
                              "value": [
                                "value-1",
                                "value-2"
                              ]
                            },
                            "description": {
                              "retain": true,
                              "type": "adf",
                              "value": {
                                "content": [
                                  {
                                    "content": [
                                      {
                                        "text": "New description value",
                                        "type": "text"
                                      }
                                    ],
                                    "type": "paragraph"
                                  }
                                ],
                                "type": "doc",
                                "version": 1
                              }
                            },
                            "fixVersions": {
                              "retain": false,
                              "type": "raw",
                              "value": [
                                "10009"
                              ]
                            },
                            "labels": {
                              "retain": false,
                              "type": "raw",
                              "value": [
                                "label-1",
                                "label-2"
                              ]
                            }
                          }
                        }
                      ],
                      "targetStatus": [
                        {
                          "statuses": {
                            "10001": [
                              "10002",
                              "10003"
                            ]
                          }
                        }
                      ]
                    }
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'sendBulkNotification': sendBulkNotification,
            'targetToSourcesMapping': targetToSourcesMapping,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/move"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_available_transitions(self, issueIdsOrKeys, endingBefore=None, startingAfter=None) -> dict[str, Any]:
        """
        Retrieves valid workflow transitions for multiple Jira issues based on provided issue IDs or keys.

        Args:
            issueIdsOrKeys (string): Comma (,) separated Ids or keys of the issues to get transitions available for them.
            endingBefore (string): (Optional)The end cursor for use in pagination.
            startingAfter (string): (Optional)The start cursor for use in pagination.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        url = f"{self.base_url}/rest/api/3/bulk/issues/transition"
        query_params = {k: v for k, v in [('issueIdsOrKeys', issueIdsOrKeys), ('endingBefore', endingBefore), ('startingAfter', startingAfter)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_transition(self, bulkTransitionInputs, sendBulkNotification=None) -> dict[str, Any]:
        """
        Transitions multiple Jira issues to a specified status in bulk using the Jira REST API, allowing for streamlined workflow management and automation of repetitive tasks.

        Args:
            bulkTransitionInputs (array): List of objects and each object has two properties:

         *  Issues that will be bulk transitioned.
         *  TransitionId that corresponds to a specific transition of issues that share the same workflow.
            sendBulkNotification (boolean): A boolean value that indicates whether to send a bulk change notification when the issues are being transitioned.

        If `true`, dispatches a bulk notification email to users about the updates.
                Example:
                ```json
                {
                  "bulkTransitionInputs": [
                    {
                      "selectedIssueIdsOrKeys": [
                        "10001",
                        "10002"
                      ],
                      "transitionId": "11"
                    },
                    {
                      "selectedIssueIdsOrKeys": [
                        "TEST-1"
                      ],
                      "transitionId": "2"
                    }
                  ],
                  "sendBulkNotification": false
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'bulkTransitionInputs': bulkTransitionInputs,
            'sendBulkNotification': sendBulkNotification,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/transition"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_unwatch(self, selectedIssueIdsOrKeys) -> dict[str, Any]:
        """
        Unwatches up to 1,000 specified Jira issues in a single bulk operation via POST request, requiring write permissions and returning success/error responses.

        Args:
            selectedIssueIdsOrKeys (array): List of issue IDs or keys which are to be bulk watched or unwatched. These IDs or keys can be from different projects and issue types.
                Example:
                ```json
                {
                  "selectedIssueIdsOrKeys": [
                    "10001",
                    "10002"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'selectedIssueIdsOrKeys': selectedIssueIdsOrKeys,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/unwatch"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def submit_bulk_watch(self, selectedIssueIdsOrKeys) -> dict[str, Any]:
        """
        Adds watchers to multiple Jira issues in bulk through a single operation.

        Args:
            selectedIssueIdsOrKeys (array): List of issue IDs or keys which are to be bulk watched or unwatched. These IDs or keys can be from different projects and issue types.
                Example:
                ```json
                {
                  "selectedIssueIdsOrKeys": [
                    "10001",
                    "10002"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        request_body = {
            'selectedIssueIdsOrKeys': selectedIssueIdsOrKeys,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/bulk/issues/watch"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_bulk_operation_progress(self, taskId) -> dict[str, Any]:
        """
        Retrieves the status of a bulk operation task identified by the specified taskId.

        Args:
            taskId (string): taskId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue bulk operations
        """
        if taskId is None:
            raise ValueError("Missing required parameter 'taskId'")
        url = f"{self.base_url}/rest/api/3/bulk/queue/{taskId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_bulk_changelogs(self, issueIdsOrKeys, fieldIds=None, maxResults=None, nextPageToken=None) -> dict[str, Any]:
        """
        Retrieves changelog data for multiple Jira issues in a single request, eliminating the need for individual API calls per issue.

        Args:
            issueIdsOrKeys (array): List of issue IDs/keys to fetch changelogs for
            fieldIds (array): List of field IDs to filter changelogs
            maxResults (integer): The maximum number of items to return per page
            nextPageToken (string): The cursor for pagination

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        request_body = {
            'fieldIds': fieldIds,
            'issueIdsOrKeys': issueIdsOrKeys,
            'maxResults': maxResults,
            'nextPageToken': nextPageToken,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/changelog/bulkfetch"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_user_data_classification_levels(self, status=None, orderBy=None) -> dict[str, Any]:
        """
        Retrieves a list of all classification levels in Jira Cloud, supporting optional filtering by status and ordering using the "orderBy" parameter.

        Args:
            status (array): Optional set of statuses to filter by.
            orderBy (string): Ordering of the results by a given field. If not provided, values will not be sorted.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Classification levels
        """
        url = f"{self.base_url}/rest/api/3/classification-levels"
        query_params = {k: v for k, v in [('status', status), ('orderBy', orderBy)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_comments_by_ids(self, ids, expand=None) -> dict[str, Any]:
        """
        Fetches a paginated list of Jira comments by their IDs using a POST request.

        Args:
            ids (array): The list of comment IDs. A maximum of 1000 IDs can be specified.
                Example:
                ```json
                {
                  "ids": [
                    1,
                    2,
                    5,
                    10
                  ]
                }
                ```
            expand (string): Use [expand](#expansion) to include additional information about comments in the response. This parameter accepts a comma-separated list. Expand options include: * `renderedBody` Returns the comment body rendered in HTML. * `properties` Returns the comment's properties.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comments
        """
        request_body = {
            'ids': ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/comment/list"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_comment_property_keys(self, commentId) -> dict[str, Any]:
        """
        Retrieves the keys of all properties associated with a specified issue comment in Jira Cloud using the REST API.

        Args:
            commentId (string): commentId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comment properties
        """
        if commentId is None:
            raise ValueError("Missing required parameter 'commentId'")
        url = f"{self.base_url}/rest/api/3/comment/{commentId}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_comment_property(self, commentId, propertyKey) -> Any:
        """
        Deletes a specific property from a comment in Jira using the Jira Cloud REST API and returns a status code upon successful deletion.

        Args:
            commentId (string): commentId
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue comment properties
        """
        if commentId is None:
            raise ValueError("Missing required parameter 'commentId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/comment/{commentId}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_comment_property(self, commentId, propertyKey) -> dict[str, Any]:
        """
        Retrieves the value of a specific property for an issue comment in Jira using the comment ID and property key.

        Args:
            commentId (string): commentId
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comment properties
        """
        if commentId is None:
            raise ValueError("Missing required parameter 'commentId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/comment/{commentId}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

  
    def find_components_for_projects(self, projectIdsOrKeys=None, startAt=None, maxResults=None, orderBy=None, query=None) -> dict[str, Any]:
        """
        Retrieves a list of Jira components using the GET method at the "/rest/api/3/component" path, allowing filtering by project IDs, pagination, and sorting, and returns the results in a paginated format.

        Args:
            projectIdsOrKeys (array): The project IDs and/or project keys (case sensitive).
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field: * `description` Sorts by the component description. * `name` Sorts by component name.
            query (string): Filter the results using a literal string. Components with a matching `name` or `description` are returned (case insensitive).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        url = f"{self.base_url}/rest/api/3/component"
        query_params = {k: v for k, v in [('projectIdsOrKeys', projectIdsOrKeys), ('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy), ('query', query)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_component(self, ari=None, assignee=None, assigneeType=None, description=None, id=None, isAssigneeTypeValid=None, lead=None, leadAccountId=None, leadUserName=None, metadata=None, name=None, project=None, projectId=None, realAssignee=None, realAssigneeType=None, self_arg_body=None) -> dict[str, Any]:
        """
        Creates a new component in Jira, providing a container for issues within a project, using the POST method on the "/rest/api/3/component" endpoint.

        Args:
            ari (string): Compass component's ID. Can't be updated. Not required for creating a Project Component.
            assignee (string): The details of the user associated with `assigneeType`, if any. See `realAssignee` for details of the user assigned to issues created with this component.
            assigneeType (string): The nominal user type used to determine the assignee for issues created with this component. See `realAssigneeType` for details on how the type of the user, and hence the user, assigned to issues is determined. Can take the following values:

         *  `PROJECT_LEAD` the assignee to any issues created with this component is nominally the lead for the project the component is in.
         *  `COMPONENT_LEAD` the assignee to any issues created with this component is nominally the lead for the component.
         *  `UNASSIGNED` an assignee is not set for issues created with this component.
         *  `PROJECT_DEFAULT` the assignee to any issues created with this component is nominally the default assignee for the project that the component is in.

        Default value: `PROJECT_DEFAULT`.  
        Optional when creating or updating a component.
            description (string): The description for the component. Optional when creating or updating a component.
            id (string): The unique identifier for the component.
            isAssigneeTypeValid (boolean): Whether a user is associated with `assigneeType`. For example, if the `assigneeType` is set to `COMPONENT_LEAD` but the component lead is not set, then `false` is returned.
            lead (string): The user details for the component's lead user.
            leadAccountId (string): The accountId of the component's lead user. The accountId uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*.
            leadUserName (string): This property is no longer available and will be removed from the documentation soon. See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            metadata (object): Compass component's metadata. Can't be updated. Not required for creating a Project Component.
            name (string): The unique name for the component in the project. Required when creating a component. Optional when updating a component. The maximum length is 255 characters.
            project (string): The key of the project the component is assigned to. Required when creating a component. Can't be updated.
            projectId (integer): The ID of the project the component is assigned to.
            realAssignee (string): The user assigned to issues created with this component, when `assigneeType` does not identify a valid assignee.
            realAssigneeType (string): The type of the assignee that is assigned to issues created with this component, when an assignee cannot be set from the `assigneeType`. For example, `assigneeType` is set to `COMPONENT_LEAD` but no component lead is set. This property is set to one of the following values:

         *  `PROJECT_LEAD` when `assigneeType` is `PROJECT_LEAD` and the project lead has permission to be assigned issues in the project that the component is in.
         *  `COMPONENT_LEAD` when `assignee`Type is `COMPONENT_LEAD` and the component lead has permission to be assigned issues in the project that the component is in.
         *  `UNASSIGNED` when `assigneeType` is `UNASSIGNED` and Jira is configured to allow unassigned issues.
         *  `PROJECT_DEFAULT` when none of the preceding cases are true.
            self_arg_body (string): The URL of the component.
                Example:
                ```json
                {
                  "assigneeType": "PROJECT_LEAD",
                  "description": "This is a Jira component",
                  "isAssigneeTypeValid": false,
                  "leadAccountId": "5b10a2844c20165700ede21g",
                  "name": "Component 1",
                  "project": "HSP"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        request_body = {
            'ari': ari,
            'assignee': assignee,
            'assigneeType': assigneeType,
            'description': description,
            'id': id,
            'isAssigneeTypeValid': isAssigneeTypeValid,
            'lead': lead,
            'leadAccountId': leadAccountId,
            'leadUserName': leadUserName,
            'metadata': metadata,
            'name': name,
            'project': project,
            'projectId': projectId,
            'realAssignee': realAssignee,
            'realAssigneeType': realAssigneeType,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/component"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_component(self, id, moveIssuesTo=None) -> Any:
        """
        Deletes a specific component in Jira by ID, optionally reassigning its issues to another component.

        Args:
            id (string): id
            moveIssuesTo (string): The ID of the component to replace the deleted component. If this value is null no replacement is made.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project components
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/component/{id}"
        query_params = {k: v for k, v in [('moveIssuesTo', moveIssuesTo)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_component(self, id) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific Jira component, identified by its ID, using the Jira REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/component/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_component(self, id, ari=None, assignee=None, assigneeType=None, description=None, id_body=None, isAssigneeTypeValid=None, lead=None, leadAccountId=None, leadUserName=None, metadata=None, name=None, project=None, projectId=None, realAssignee=None, realAssigneeType=None, self_arg_body=None) -> dict[str, Any]:
        """
        Updates the specified component's details using the provided ID.

        Args:
            id (string): id
            ari (string): Compass component's ID. Can't be updated. Not required for creating a Project Component.
            assignee (string): The details of the user associated with `assigneeType`, if any. See `realAssignee` for details of the user assigned to issues created with this component.
            assigneeType (string): The nominal user type used to determine the assignee for issues created with this component. See `realAssigneeType` for details on how the type of the user, and hence the user, assigned to issues is determined. Can take the following values:

         *  `PROJECT_LEAD` the assignee to any issues created with this component is nominally the lead for the project the component is in.
         *  `COMPONENT_LEAD` the assignee to any issues created with this component is nominally the lead for the component.
         *  `UNASSIGNED` an assignee is not set for issues created with this component.
         *  `PROJECT_DEFAULT` the assignee to any issues created with this component is nominally the default assignee for the project that the component is in.

        Default value: `PROJECT_DEFAULT`.  
        Optional when creating or updating a component.
            description (string): The description for the component. Optional when creating or updating a component.
            id_body (string): The unique identifier for the component.
            isAssigneeTypeValid (boolean): Whether a user is associated with `assigneeType`. For example, if the `assigneeType` is set to `COMPONENT_LEAD` but the component lead is not set, then `false` is returned.
            lead (string): The user details for the component's lead user.
            leadAccountId (string): The accountId of the component's lead user. The accountId uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*.
            leadUserName (string): This property is no longer available and will be removed from the documentation soon. See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            metadata (object): Compass component's metadata. Can't be updated. Not required for creating a Project Component.
            name (string): The unique name for the component in the project. Required when creating a component. Optional when updating a component. The maximum length is 255 characters.
            project (string): The key of the project the component is assigned to. Required when creating a component. Can't be updated.
            projectId (integer): The ID of the project the component is assigned to.
            realAssignee (string): The user assigned to issues created with this component, when `assigneeType` does not identify a valid assignee.
            realAssigneeType (string): The type of the assignee that is assigned to issues created with this component, when an assignee cannot be set from the `assigneeType`. For example, `assigneeType` is set to `COMPONENT_LEAD` but no component lead is set. This property is set to one of the following values:

         *  `PROJECT_LEAD` when `assigneeType` is `PROJECT_LEAD` and the project lead has permission to be assigned issues in the project that the component is in.
         *  `COMPONENT_LEAD` when `assignee`Type is `COMPONENT_LEAD` and the component lead has permission to be assigned issues in the project that the component is in.
         *  `UNASSIGNED` when `assigneeType` is `UNASSIGNED` and Jira is configured to allow unassigned issues.
         *  `PROJECT_DEFAULT` when none of the preceding cases are true.
            self_arg_body (string): The URL of the component.
                Example:
                ```json
                {
                  "assigneeType": "PROJECT_LEAD",
                  "description": "This is a Jira component",
                  "isAssigneeTypeValid": false,
                  "leadAccountId": "5b10a2844c20165700ede21g",
                  "name": "Component 1"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'ari': ari,
            'assignee': assignee,
            'assigneeType': assigneeType,
            'description': description,
            'id': id_body,
            'isAssigneeTypeValid': isAssigneeTypeValid,
            'lead': lead,
            'leadAccountId': leadAccountId,
            'leadUserName': leadUserName,
            'metadata': metadata,
            'name': name,
            'project': project,
            'projectId': projectId,
            'realAssignee': realAssignee,
            'realAssigneeType': realAssigneeType,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/component/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_component_related_issues(self, id) -> dict[str, Any]:
        """
        Retrieves the issue counts related to a specific Jira component identified by its ID using the "GET" method.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/component/{id}/relatedIssueCounts"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_configuration(self) -> dict[str, Any]:
        """
        Retrieves configuration details from Jira using the GET method and returns the result in the response.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Jira settings
        """
        url = f"{self.base_url}/rest/api/3/configuration"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_selected_time_tracking_implementation(self) -> dict[str, Any]:
        """
        Retrieves the time tracking settings in Jira, including time format and default time unit, using the GET method at "/rest/api/3/configuration/timetracking".

        Returns:
            dict[str, Any]: Returned if the request is successful and time tracking is enabled.

        Tags:
            Time tracking
        """
        url = f"{self.base_url}/rest/api/3/configuration/timetracking"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def select_time_tracking_implementation(self, key, name=None, url=None) -> Any:
        """
        Updates time tracking settings in Jira using the Jira Cloud platform REST API at "/rest/api/3/configuration/timetracking" with a "PUT" method, allowing configurations such as time format and default time unit.

        Args:
            key (string): The key for the time tracking provider. For example, *JIRA*.
            name (string): The name of the time tracking provider. For example, *JIRA provided time tracking*.
            url (string): The URL of the configuration page for the time tracking provider app. For example, */example/config/url*. This property is only returned if the `adminPageKey` property is set in the module descriptor of the time tracking provider app.
                Example:
                ```json
                {
                  "key": "Jira"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Time tracking
        """
        request_body = {
            'key': key,
            'name': name,
            'url': url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/configuration/timetracking"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_available_time_tracking_implementations(self) -> list[Any]:
        """
        Retrieves a list of all configured time tracking providers in Jira, including the active provider if time tracking is enabled.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Time tracking
        """
        url = f"{self.base_url}/rest/api/3/configuration/timetracking/list"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_shared_time_tracking_configuration(self) -> dict[str, Any]:
        """
        Retrieves time tracking configuration settings such as time format and default units using the Jira Cloud REST API.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Time tracking
        """
        url = f"{self.base_url}/rest/api/3/configuration/timetracking/options"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_shared_time_tracking_configuration(self, defaultUnit, timeFormat, workingDaysPerWeek, workingHoursPerDay) -> dict[str, Any]:
        """
        Updates Jira time tracking configuration settings including time format, working hours, and default time unit.

        Args:
            defaultUnit (string): The default unit of time applied to logged time.
            timeFormat (string): The format that will appear on an issue's *Time Spent* field.
            workingDaysPerWeek (number): The number of days in a working week.
            workingHoursPerDay (number): The number of hours in a working day.
                Example:
                ```json
                {
                  "defaultUnit": "hour",
                  "timeFormat": "pretty",
                  "workingDaysPerWeek": 5.5,
                  "workingHoursPerDay": 7.6
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Time tracking
        """
        request_body = {
            'defaultUnit': defaultUnit,
            'timeFormat': timeFormat,
            'workingDaysPerWeek': workingDaysPerWeek,
            'workingHoursPerDay': workingHoursPerDay,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/configuration/timetracking/options"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_custom_field_option(self, id) -> dict[str, Any]:
        """
        Retrieves a full representation of a custom field option by its ID using the Jira REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/customFieldOption/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_dashboards(self, filter=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of Jira dashboards using the GET method, allowing for optional filtering, pagination with start and max results parameters.

        Args:
            filter (string): The filter applied to the list of dashboards. Valid values are: * `favourite` Returns dashboards the user has marked as favorite. * `my` Returns dashboards owned by the user.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        url = f"{self.base_url}/rest/api/3/dashboard"
        query_params = {k: v for k, v in [('filter', filter), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_dashboard(self, editPermissions, name, sharePermissions, extendAdminPermissions=None, description=None) -> dict[str, Any]:
        """
        Creates a new dashboard in Jira Cloud using the REST API and returns a response indicating the success or failure of the operation.

        Args:
            editPermissions (array): The edit permissions for the dashboard.
            name (string): The name of the dashboard.
            sharePermissions (array): The share permissions for the dashboard.
            extendAdminPermissions (boolean): Whether admin level permissions are used. It should only be true if the user has *Administer Jira* [global permission](
            description (string): The description of the dashboard.
                Example:
                ```json
                {
                  "description": "A dashboard to help auditors identify sample of issues to check.",
                  "editPermissions": [],
                  "name": "Auditors dashboard",
                  "sharePermissions": [
                    {
                      "type": "global"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        request_body = {
            'description': description,
            'editPermissions': editPermissions,
            'name': name,
            'sharePermissions': sharePermissions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard"
        query_params = {k: v for k, v in [('extendAdminPermissions', extendAdminPermissions)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_edit_dashboards(self, action, entityIds, changeOwnerDetails=None, extendAdminPermissions=None, permissionDetails=None) -> dict[str, Any]:
        """
        Bulk updates permissions and settings for multiple Jira dashboards in a single operation.

        Args:
            action (string): Allowed action for bulk edit shareable entity
            entityIds (array): The id list of shareable entities to be changed.
            changeOwnerDetails (string): The details of change owner action.
            extendAdminPermissions (boolean): Whether the actions are executed by users with Administer Jira global permission.
            permissionDetails (string): The permission details to be changed.
                Example:
                ```json
                {
                  "action": "changePermission",
                  "entityIds": [
                    10001,
                    10002
                  ],
                  "extendAdminPermissions": true,
                  "permissionDetails": {
                    "editPermissions": [
                      {
                        "group": {
                          "groupId": "276f955c-63d7-42c8-9520-92d01dca0625",
                          "name": "jira-administrators",
                          "self": "https://your-domain.atlassian.net/rest/api/~ver~/group?groupId=276f955c-63d7-42c8-9520-92d01dca0625"
                        },
                        "id": 10010,
                        "type": "group"
                      }
                    ],
                    "sharePermissions": [
                      {
                        "id": 10000,
                        "type": "global"
                      }
                    ]
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        request_body = {
            'action': action,
            'changeOwnerDetails': changeOwnerDetails,
            'entityIds': entityIds,
            'extendAdminPermissions': extendAdminPermissions,
            'permissionDetails': permissionDetails,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard/bulk/edit"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_available_dashboard_gadgets(self) -> dict[str, Any]:
        """
        Retrieves a list of available gadgets that can be added to Jira dashboards using the Jira Cloud API.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        url = f"{self.base_url}/rest/api/3/dashboard/gadgets"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dashboards_paginated(self, dashboardName=None, accountId=None, owner=None, groupname=None, groupId=None, projectId=None, orderBy=None, startAt=None, maxResults=None, status=None, expand=None) -> dict[str, Any]:
        """
        Searches for Jira dashboards using specified criteria, such as dashboard name, account ID, owner, group name, group ID, project ID, and other parameters, and returns a list of matching dashboards.

        Args:
            dashboardName (string): String used to perform a case-insensitive partial match with `name`.
            accountId (string): User account ID used to return dashboards with the matching `owner.accountId`. This parameter cannot be used with the `owner` parameter.
            owner (string): This parameter is deprecated because of privacy changes. Use `accountId` instead. See the [migration guide]( for details. User name used to return dashboards with the matching `owner.name`. This parameter cannot be used with the `accountId` parameter.
            groupname (string): As a group's name can change, use of `groupId` is recommended. Group name used to return dashboards that are shared with a group that matches `sharePermissions.group.name`. This parameter cannot be used with the `groupId` parameter.
            groupId (string): Group ID used to return dashboards that are shared with a group that matches `sharePermissions.group.groupId`. This parameter cannot be used with the `groupname` parameter.
            projectId (integer): Project ID used to returns dashboards that are shared with a project that matches `sharePermissions.project.id`.
            orderBy (string): [Order](#ordering) the results by a field: * `description` Sorts by dashboard description. Note that this sort works independently of whether the expand to display the description field is in use. * `favourite_count` Sorts by dashboard popularity. * `id` Sorts by dashboard ID. * `is_favourite` Sorts by whether the dashboard is marked as a favorite. * `name` Sorts by dashboard name. * `owner` Sorts by dashboard owner name.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            status (string): The status to filter by. It may be active, archived or deleted.
            expand (string): Use [expand](#expansion) to include additional information about dashboard in the response. This parameter accepts a comma-separated list. Expand options include: * `description` Returns the description of the dashboard. * `owner` Returns the owner of the dashboard. * `viewUrl` Returns the URL that is used to view the dashboard. * `favourite` Returns `isFavourite`, an indicator of whether the user has set the dashboard as a favorite. * `favouritedCount` Returns `popularity`, a count of how many users have set this dashboard as a favorite. * `sharePermissions` Returns details of the share permissions defined for the dashboard. * `editPermissions` Returns details of the edit permissions defined for the dashboard. * `isWritable` Returns whether the current user has permission to edit the dashboard.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        url = f"{self.base_url}/rest/api/3/dashboard/search"
        query_params = {k: v for k, v in [('dashboardName', dashboardName), ('accountId', accountId), ('owner', owner), ('groupname', groupname), ('groupId', groupId), ('projectId', projectId), ('orderBy', orderBy), ('startAt', startAt), ('maxResults', maxResults), ('status', status), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_gadgets(self, dashboardId, moduleKey=None, uri=None, gadgetId=None) -> dict[str, Any]:
        """
        Retrieves a specific gadget or all gadgets from a Jira dashboard.

        Args:
            dashboardId (string): dashboardId
            moduleKey (array): The list of gadgets module keys. To include multiple module keys, separate module keys with ampersand: `moduleKey=key:one&moduleKey=key:two`.
            uri (array): The list of gadgets URIs. To include multiple URIs, separate URIs with ampersand: `uri=/rest/example/uri/1&uri=/rest/example/uri/2`.
            gadgetId (array): The list of gadgets IDs. To include multiple IDs, separate IDs with ampersand: `gadgetId=10000&gadgetId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/gadget"
        query_params = {k: v for k, v in [('moduleKey', moduleKey), ('uri', uri), ('gadgetId', gadgetId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_gadget(self, dashboardId, color=None, ignoreUriAndModuleKeyValidation=None, moduleKey=None, position=None, title=None, uri=None) -> dict[str, Any]:
        """
        Adds a gadget to a specified Jira dashboard using the provided configuration and returns the created gadget details upon success.

        Args:
            dashboardId (string): dashboardId
            color (string): The color of the gadget. Should be one of `blue`, `red`, `yellow`, `green`, `cyan`, `purple`, `gray`, or `white`.
            ignoreUriAndModuleKeyValidation (boolean): Whether to ignore the validation of module key and URI. For example, when a gadget is created that is a part of an application that isn't installed.
            moduleKey (string): The module key of the gadget type. Can't be provided with `uri`.
            position (string): The position of the gadget. When the gadget is placed into the position, other gadgets in the same column are moved down to accommodate it.
            title (string): The title of the gadget.
            uri (string): The URI of the gadget type. Can't be provided with `moduleKey`.
                Example:
                ```json
                {
                  "color": "blue",
                  "ignoreUriAndModuleKeyValidation": false,
                  "moduleKey": "com.atlassian.plugins.atlassian-connect-plugin:com.atlassian.connect.node.sample-addon__sample-dashboard-item",
                  "position": {
                    "column": 1,
                    "row": 0
                  },
                  "title": "Issue statistics"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        request_body = {
            'color': color,
            'ignoreUriAndModuleKeyValidation': ignoreUriAndModuleKeyValidation,
            'moduleKey': moduleKey,
            'position': position,
            'title': title,
            'uri': uri,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/gadget"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_gadget(self, dashboardId, gadgetId) -> Any:
        """
        Removes a specific gadget from a Jira Cloud dashboard using the DELETE method, where other gadgets in the same column are automatically moved up to fill the emptied position.

        Args:
            dashboardId (string): dashboardId
            gadgetId (string): gadgetId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        if gadgetId is None:
            raise ValueError("Missing required parameter 'gadgetId'")
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_gadget(self, dashboardId, gadgetId, color=None, position=None, title=None) -> Any:
        """
        Updates a gadget's configuration (e.g., color, position, title) on a specified Jira dashboard.

        Args:
            dashboardId (string): dashboardId
            gadgetId (string): gadgetId
            color (string): The color of the gadget. Should be one of `blue`, `red`, `yellow`, `green`, `cyan`, `purple`, `gray`, or `white`.
            position (string): The position of the gadget.
            title (string): The title of the gadget.
                Example:
                ```json
                {
                  "color": "red",
                  "position": {
                    "column": 1,
                    "row": 1
                  },
                  "title": "My new gadget title"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        if gadgetId is None:
            raise ValueError("Missing required parameter 'gadgetId'")
        request_body = {
            'color': color,
            'position': position,
            'title': title,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/gadget/{gadgetId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dashboard_item_property_keys(self, dashboardId, itemId) -> dict[str, Any]:
        """
        Retrieves all property keys for a specific dashboard item in Jira using provided dashboard and item IDs.

        Args:
            dashboardId (string): dashboardId
            itemId (string): itemId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        if itemId is None:
            raise ValueError("Missing required parameter 'itemId'")
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_dashboard_item_property(self, dashboardId, itemId, propertyKey) -> Any:
        """
        Deletes a dashboard item property (identified by propertyKey) from a specific dashboard item, accessible anonymously but requiring dashboard ownership for successful deletion.

        Args:
            dashboardId (string): dashboardId
            itemId (string): itemId
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the dashboard item property is deleted.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        if itemId is None:
            raise ValueError("Missing required parameter 'itemId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dashboard_item_property(self, dashboardId, itemId, propertyKey) -> dict[str, Any]:
        """
        Retrieves a specific property of a dashboard item using the Jira API, returning the property value associated with the given dashboard ID, item ID, and property key.

        Args:
            dashboardId (string): dashboardId
            itemId (string): itemId
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if dashboardId is None:
            raise ValueError("Missing required parameter 'dashboardId'")
        if itemId is None:
            raise ValueError("Missing required parameter 'itemId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def delete_dashboard(self, id) -> Any:
        """
        Deletes a dashboard identified by its ID using the "DELETE" method and returns a successful status if the operation is completed without errors.

        Args:
            id (string): id

        Returns:
            Any: Returned if the dashboard is deleted.

        Tags:
            Dashboards
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/dashboard/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dashboard(self, id) -> dict[str, Any]:
        """
        Retrieves the details of a specific Jira dashboard by ID.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/dashboard/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_dashboard(self, id, editPermissions, name, sharePermissions, extendAdminPermissions=None, description=None) -> dict[str, Any]:
        """
        Updates a dashboard with the specified ID using the PUT method, optionally extending admin permissions, and returns a status message if successful.

        Args:
            id (string): id
            editPermissions (array): The edit permissions for the dashboard.
            name (string): The name of the dashboard.
            sharePermissions (array): The share permissions for the dashboard.
            extendAdminPermissions (boolean): Whether admin level permissions are used. It should only be true if the user has *Administer Jira* [global permission](
            description (string): The description of the dashboard.
                Example:
                ```json
                {
                  "description": "A dashboard to help auditors identify sample of issues to check.",
                  "editPermissions": [],
                  "name": "Auditors dashboard",
                  "sharePermissions": [
                    {
                      "type": "global"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'editPermissions': editPermissions,
            'name': name,
            'sharePermissions': sharePermissions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard/{id}"
        query_params = {k: v for k, v in [('extendAdminPermissions', extendAdminPermissions)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def copy_dashboard(self, id, editPermissions, name, sharePermissions, extendAdminPermissions=None, description=None) -> dict[str, Any]:
        """
        Copies a dashboard and replaces specified parameters in the copied dashboard, returning the new dashboard details.

        Args:
            id (string): id
            editPermissions (array): The edit permissions for the dashboard.
            name (string): The name of the dashboard.
            sharePermissions (array): The share permissions for the dashboard.
            extendAdminPermissions (boolean): Whether admin level permissions are used. It should only be true if the user has *Administer Jira* [global permission](
            description (string): The description of the dashboard.
                Example:
                ```json
                {
                  "description": "A dashboard to help auditors identify sample of issues to check.",
                  "editPermissions": [],
                  "name": "Auditors dashboard",
                  "sharePermissions": [
                    {
                      "type": "global"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dashboards
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'editPermissions': editPermissions,
            'name': name,
            'sharePermissions': sharePermissions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/dashboard/{id}/copy"
        query_params = {k: v for k, v in [('extendAdminPermissions', extendAdminPermissions)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_policy(self) -> dict[str, Any]:
        """
        Retrieves details about the data policy for a workspace using the Jira Cloud REST API, returning information on whether data policies are enabled for the workspace.

        Returns:
            dict[str, Any]: Returned if the request is successful

        Tags:
            App data policies
        """
        url = f"{self.base_url}/rest/api/3/data-policy"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_policies(self, ids=None) -> dict[str, Any]:
        """
        Retrieves data policies affecting specific projects in Jira using the "/rest/api/3/data-policy/project" endpoint, returning details about which projects are impacted by data security policies.

        Args:
            ids (string): A list of project identifiers. This parameter accepts a comma-separated list.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            App data policies
        """
        url = f"{self.base_url}/rest/api/3/data-policy/project"
        query_params = {k: v for k, v in [('ids', ids)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_events(self) -> list[Any]:
        """
        Retrieves a list of events using the Jira Cloud API by sending a GET request to "/rest/api/3/events," providing a paginated response based on the specified parameters.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        url = f"{self.base_url}/rest/api/3/events"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def analyse_expression(self, expressions, check=None, contextVariables=None) -> dict[str, Any]:
        """
        Analyzes a Jira expression to statically check its characteristics, such as complexity, without evaluating it, using a POST method at "/rest/api/3/expression/analyse" with the option to specify what to check via a query parameter.

        Args:
            expressions (array): The list of Jira expressions to analyse. Example: "issues.map(issue => issue.properties['property_key'])".
            check (string): The check to perform: * `syntax` Each expression's syntax is checked to ensure the expression can be parsed. Also, syntactic limits are validated. For example, the expression's length. * `type` EXPERIMENTAL. Each expression is type checked and the final type of the expression inferred. Any type errors that would result in the expression failure at runtime are reported. For example, accessing properties that don't exist or passing the wrong number of arguments to functions. Also performs the syntax check. * `complexity` EXPERIMENTAL. Determines the formulae for how many [expensive operations]( each expression may execute.
            contextVariables (object): Context variables and their types. The type checker assumes that [common context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables), such as `issue` or `project`, are available in context and sets their type. Use this property to override the default types or provide details of new variables.
                Example:
                ```json
                {
                  "contextVariables": {
                    "listOfStrings": "List<String>",
                    "record": "{ a: Number, b: String }",
                    "value": "User"
                  },
                  "expressions": [
                    "issues.map(issue => issue.properties['property_key'])"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Jira expressions
        """
        request_body = {
            'contextVariables': contextVariables,
            'expressions': expressions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/expression/analyse"
        query_params = {k: v for k, v in [('check', check)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def evaluate_jira_expression(self, expression, expand=None, context=None) -> dict[str, Any]:
        """
        Evaluates Jira expressions using an enhanced search API for scalable processing of JQL queries and returns primitive values, lists, or objects.

        Args:
            expression (string): The Jira expression to evaluate. Example: '{ key: issue.key, type: issue.issueType.name, links: issue.links.map(link => link.linkedIssue.id) }'.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts `meta.complexity` that returns information about the expression complexity. For example, the number of expensive operations used by the expression and how close the expression is to reaching the [complexity limit]( Useful when designing and debugging your expressions.
            context (string): The context in which the Jira expression is evaluated.
                Example:
                ```json
                {
                  "context": {
                    "board": 10100,
                    "custom": {
                      "config": {
                        "type": "json",
                        "value": {
                          "userId": "10002"
                        }
                      },
                      "issuesList": [
                        {
                          "key": "ACJIRA-1471",
                          "type": "issue"
                        },
                        {
                          "id": 100001,
                          "type": "issue"
                        }
                      ],
                      "myUser": {
                        "accountId": "100001",
                        "type": "user"
                      },
                      "nullField": {
                        "type": "json"
                      }
                    },
                    "customerRequest": 1450,
                    "issue": {
                      "key": "ACJIRA-1470"
                    },
                    "issues": {
                      "jql": {
                        "maxResults": 100,
                        "query": "project = HSP",
                        "startAt": 0,
                        "validation": "strict"
                      }
                    },
                    "project": {
                      "key": "ACJIRA"
                    },
                    "serviceDesk": 10023,
                    "sprint": 10001
                  },
                  "expression": "{ key: issue.key, type: issue.issueType.name, links: issue.links.map(link => link.linkedIssue.id), listCustomVariable: issuesList.includes(issue), customVariables: myUser.accountId == config.userId}"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the evaluation results in a value. The result is a JSON primitive value, list, or object.

        Tags:
            Jira expressions
        """
        request_body = {
            'context': context,
            'expression': expression,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/expression/eval"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def evaluate_jsisjira_expression(self, expression, expand=None, context=None) -> dict[str, Any]:
        """
        Evaluates Jira expressions using the enhanced search API with support for pagination and eventually consistent JQL queries, returning primitive values, lists, or objects.

        Args:
            expression (string): The Jira expression to evaluate. Example: '{ key: issue.key, type: issue.issueType.name, links: issue.links.map(link => link.linkedIssue.id) }'.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts `meta.complexity` that returns information about the expression complexity. For example, the number of expensive operations used by the expression and how close the expression is to reaching the [complexity limit]( Useful when designing and debugging your expressions.
            context (string): The context in which the Jira expression is evaluated.
                Example:
                ```json
                {
                  "context": {
                    "board": 10100,
                    "custom": {
                      "config": {
                        "type": "json",
                        "value": {
                          "userId": "10002"
                        }
                      },
                      "issuesList": [
                        {
                          "key": "ACJIRA-1471",
                          "type": "issue"
                        },
                        {
                          "id": 100001,
                          "type": "issue"
                        }
                      ],
                      "myUser": {
                        "accountId": "100001",
                        "type": "user"
                      },
                      "nullField": {
                        "type": "json"
                      }
                    },
                    "customerRequest": 1450,
                    "issue": {
                      "key": "ACJIRA-1470"
                    },
                    "issues": {
                      "jql": {
                        "maxResults": 100,
                        "nextPageToken": "EgQIlMIC",
                        "query": "project = HSP"
                      }
                    },
                    "project": {
                      "key": "ACJIRA"
                    },
                    "serviceDesk": 10023,
                    "sprint": 10001
                  },
                  "expression": "{ key: issue.key, type: issue.issueType.name, links: issue.links.map(link => link.linkedIssue.id), listCustomVariable: issuesList.includes(issue), customVariables: myUser.accountId == config.userId}"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the evaluation results in a value. The result is a JSON primitive value, list, or object.

        Tags:
            Jira expressions
        """
        request_body = {
            'context': context,
            'expression': expression,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/expression/evaluate"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_fields(self) -> list[Any]:
        """
        Retrieves a list of available fields in Jira using the GET method at the "/rest/api/3/field" path.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue fields
        """
        url = f"{self.base_url}/rest/api/3/field"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_custom_field(self, name, type, description=None, searcherKey=None) -> dict[str, Any]:
        """
        Creates a custom field using a definition and returns a successful creation message when the operation is completed successfully.

        Args:
            name (string): The name of the custom field, which is displayed in Jira. This is not the unique identifier.
            type (string): The type of the custom field. These built-in custom field types are available:

         *  `cascadingselect`: Enables values to be selected from two levels of select lists (value: `com.atlassian.jira.plugin.system.customfieldtypes:cascadingselect`)
         *  `datepicker`: Stores a date using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:datepicker`)
         *  `datetime`: Stores a date with a time component (value: `com.atlassian.jira.plugin.system.customfieldtypes:datetime`)
         *  `float`: Stores and validates a numeric (floating point) input (value: `com.atlassian.jira.plugin.system.customfieldtypes:float`)
         *  `grouppicker`: Stores a user group using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:grouppicker`)
         *  `importid`: A read-only field that stores the ID the issue had in the system it was imported from (value: `com.atlassian.jira.plugin.system.customfieldtypes:importid`)
         *  `labels`: Stores labels (value: `com.atlassian.jira.plugin.system.customfieldtypes:labels`)
         *  `multicheckboxes`: Stores multiple values using checkboxes (value: ``)
         *  `multigrouppicker`: Stores multiple user groups using a picker control (value: ``)
         *  `multiselect`: Stores multiple values using a select list (value: `com.atlassian.jira.plugin.system.customfieldtypes:multicheckboxes`)
         *  `multiuserpicker`: Stores multiple users using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:multigrouppicker`)
         *  `multiversion`: Stores multiple versions from the versions available in a project using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:multiversion`)
         *  `project`: Stores a project from a list of projects that the user is permitted to view (value: `com.atlassian.jira.plugin.system.customfieldtypes:project`)
         *  `radiobuttons`: Stores a value using radio buttons (value: `com.atlassian.jira.plugin.system.customfieldtypes:radiobuttons`)
         *  `readonlyfield`: Stores a read-only text value, which can only be populated via the API (value: `com.atlassian.jira.plugin.system.customfieldtypes:readonlyfield`)
         *  `select`: Stores a value from a configurable list of options (value: `com.atlassian.jira.plugin.system.customfieldtypes:select`)
         *  `textarea`: Stores a long text string using a multiline text area (value: `com.atlassian.jira.plugin.system.customfieldtypes:textarea`)
         *  `textfield`: Stores a text string using a single-line text box (value: `com.atlassian.jira.plugin.system.customfieldtypes:textfield`)
         *  `url`: Stores a URL (value: `com.atlassian.jira.plugin.system.customfieldtypes:url`)
         *  `userpicker`: Stores a user using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:userpicker`)
         *  `version`: Stores a version using a picker control (value: `com.atlassian.jira.plugin.system.customfieldtypes:version`)

        To create a field based on a [Forge custom field type](https://developer.atlassian.com/platform/forge/manifest-reference/modules/#jira-custom-field-type--beta-), use the ID of the Forge custom field type as the value. For example, `ari:cloud:ecosystem::extension/e62f20a2-4b61-4dbe-bfb9-9a88b5e3ac84/548c5df1-24aa-4f7c-bbbb-3038d947cb05/static/my-cf-type-key`.
            description (string): The description of the custom field, which is displayed in Jira.
            searcherKey (string): The searcher defines the way the field is searched in Jira. For example, *com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher*.  
        The search UI (basic search and JQL search) will display different operations and values for the field, based on the field searcher. You must specify a searcher that is valid for the field type, as listed below (abbreviated values shown):

         *  `cascadingselect`: `cascadingselectsearcher`
         *  `datepicker`: `daterange`
         *  `datetime`: `datetimerange`
         *  `float`: `exactnumber` or `numberrange`
         *  `grouppicker`: `grouppickersearcher`
         *  `importid`: `exactnumber` or `numberrange`
         *  `labels`: `labelsearcher`
         *  `multicheckboxes`: `multiselectsearcher`
         *  `multigrouppicker`: `multiselectsearcher`
         *  `multiselect`: `multiselectsearcher`
         *  `multiuserpicker`: `userpickergroupsearcher`
         *  `multiversion`: `versionsearcher`
         *  `project`: `projectsearcher`
         *  `radiobuttons`: `multiselectsearcher`
         *  `readonlyfield`: `textsearcher`
         *  `select`: `multiselectsearcher`
         *  `textarea`: `textsearcher`
         *  `textfield`: `textsearcher`
         *  `url`: `exacttextsearcher`
         *  `userpicker`: `userpickergroupsearcher`
         *  `version`: `versionsearcher`

        If no searcher is provided, the field isn't searchable. However, [Forge custom fields](https://developer.atlassian.com/platform/forge/manifest-reference/modules/#jira-custom-field-type--beta-) have a searcher set automatically, so are always searchable.
                Example:
                ```json
                {
                  "description": "Custom field for picking groups",
                  "name": "New custom field",
                  "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:grouppickersearcher",
                  "type": "com.atlassian.jira.plugin.system.customfieldtypes:grouppicker"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the custom field is created.

        Tags:
            Issue fields
        """
        request_body = {
            'description': description,
            'name': name,
            'searcherKey': searcherKey,
            'type': type,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_associations(self, associationContexts, fields) -> Any:
        """
        Deletes an association between a field and its related entities, returning response codes for success or error conditions.

        Args:
            associationContexts (array): Contexts to associate/unassociate the fields with.
            fields (array): Fields to associate/unassociate with projects.
                Example:
                ```json
                {
                  "associationContexts": [
                    {
                      "identifier": 10000,
                      "type": "PROJECT_ID"
                    },
                    {
                      "identifier": 10001,
                      "type": "PROJECT_ID"
                    }
                  ],
                  "fields": [
                    {
                      "identifier": "customfield_10000",
                      "type": "FIELD_ID"
                    },
                    {
                      "identifier": "customfield_10001",
                      "type": "FIELD_ID"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the field association validation passes.

        Tags:
            Issue custom field associations
        """
        request_body = {
            'associationContexts': associationContexts,
            'fields': fields,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/association"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_associations(self, associationContexts, fields) -> Any:
        """
        Associates or unassociates custom fields with projects and issue types in Jira using the PUT method.

        Args:
            associationContexts (array): Contexts to associate/unassociate the fields with.
            fields (array): Fields to associate/unassociate with projects.
                Example:
                ```json
                {
                  "associationContexts": [
                    {
                      "identifier": 10000,
                      "type": "PROJECT_ID"
                    },
                    {
                      "identifier": 10001,
                      "type": "PROJECT_ID"
                    }
                  ],
                  "fields": [
                    {
                      "identifier": "customfield_10000",
                      "type": "FIELD_ID"
                    },
                    {
                      "identifier": "customfield_10001",
                      "type": "FIELD_ID"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the field association validation passes.

        Tags:
            Issue custom field associations
        """
        request_body = {
            'associationContexts': associationContexts,
            'fields': fields,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/association"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_fields_paginated(self, startAt=None, maxResults=None, type=None, id=None, query=None, orderBy=None, expand=None, projectIds=None) -> dict[str, Any]:
        """
        Retrieves and filters Jira fields by criteria such as ID, type, or name, supporting pagination and field expansion.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            type (array): The type of fields to search.
            id (array): The IDs of the custom fields to return or, where `query` is specified, filter.
            query (string): String used to perform a case-insensitive partial match with field names or descriptions.
            orderBy (string): [Order](#ordering) the results by: * `contextsCount` sorts by the number of contexts related to a field * `lastUsed` sorts by the date when the value of the field last changed * `name` sorts by the field name * `screensCount` sorts by the number of screens related to a field
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `key` returns the key for each field * `stableId` returns the stableId for each field * `lastUsed` returns the date when the value of the field last changed * `screensCount` returns the number of screens related to a field * `contextsCount` returns the number of contexts related to a field * `isLocked` returns information about whether the field is locked * `searcherKey` returns the searcher key for each custom field
            projectIds (array): Comma-separated list of project IDs to filter the field search results by, restricting them to fields used in the specified projects.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue fields
        """
        url = f"{self.base_url}/rest/api/3/field/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('type', type), ('id', id), ('query', query), ('orderBy', orderBy), ('expand', expand), ('projectIds', projectIds)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_trashed_fields_paginated(self, startAt=None, maxResults=None, id=None, query=None, expand=None, orderBy=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of custom fields that have been trashed in Jira, allowing filtering by field ID, name, or description.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): **id**: The parameter used to filter trashed fields by their unique identifier.
            query (string): String used to perform a case-insensitive partial match with field names or descriptions.
            expand (string): The "expand" parameter allows you to specify which additional fields or entities of the response should be expanded with more detailed information, using a comma-separated list of entity names.
            orderBy (string): [Order](#ordering) the results by a field: * `name` sorts by the field name * `trashDate` sorts by the date the field was moved to the trash * `plannedDeletionDate` sorts by the planned deletion date

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue fields
        """
        url = f"{self.base_url}/rest/api/3/field/search/trashed"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('query', query), ('expand', expand), ('orderBy', orderBy)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_custom_field(self, fieldId, description=None, name=None, searcherKey=None) -> Any:
        """
        Updates a Jira custom field using the `PUT` method, specifying the field ID in the path, and returns a status response upon successful modification.

        Args:
            fieldId (string): fieldId
            description (string): The description of the custom field. The maximum length is 40000 characters.
            name (string): The name of the custom field. It doesn't have to be unique. The maximum length is 255 characters.
            searcherKey (string): The searcher that defines the way the field is searched in Jira. It can be set to `null`, otherwise you must specify the valid searcher for the field type, as listed below (abbreviated values shown):

         *  `cascadingselect`: `cascadingselectsearcher`
         *  `datepicker`: `daterange`
         *  `datetime`: `datetimerange`
         *  `float`: `exactnumber` or `numberrange`
         *  `grouppicker`: `grouppickersearcher`
         *  `importid`: `exactnumber` or `numberrange`
         *  `labels`: `labelsearcher`
         *  `multicheckboxes`: `multiselectsearcher`
         *  `multigrouppicker`: `multiselectsearcher`
         *  `multiselect`: `multiselectsearcher`
         *  `multiuserpicker`: `userpickergroupsearcher`
         *  `multiversion`: `versionsearcher`
         *  `project`: `projectsearcher`
         *  `radiobuttons`: `multiselectsearcher`
         *  `readonlyfield`: `textsearcher`
         *  `select`: `multiselectsearcher`
         *  `textarea`: `textsearcher`
         *  `textfield`: `textsearcher`
         *  `url`: `exacttextsearcher`
         *  `userpicker`: `userpickergroupsearcher`
         *  `version`: `versionsearcher`
                Example:
                ```json
                {
                  "description": "Select the manager and the corresponding employee.",
                  "name": "Managers and employees list",
                  "searcherKey": "com.atlassian.jira.plugin.system.customfieldtypes:cascadingselectsearcher"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue fields
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        request_body = {
            'description': description,
            'name': name,
            'searcherKey': searcherKey,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_contexts_for_field(self, fieldId, isAnyIssueType=None, isGlobalContext=None, contextId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of custom field contexts for a specified field in Jira using the path "/rest/api/3/field/{fieldId}/context" with optional filters for issue type and global context.

        Args:
            fieldId (string): fieldId
            isAnyIssueType (boolean): Whether to return contexts that apply to all issue types.
            isGlobalContext (boolean): Whether to return contexts that apply to all projects.
            contextId (array): The list of context IDs. To include multiple contexts, separate IDs with ampersand: `contextId=10000&contextId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context"
        query_params = {k: v for k, v in [('isAnyIssueType', isAnyIssueType), ('isGlobalContext', isGlobalContext), ('contextId', contextId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_custom_field_context(self, fieldId, name, description=None, id=None, issueTypeIds=None, projectIds=None) -> dict[str, Any]:
        """
        Creates a new custom field context for the specified field ID, defining its project and issue type associations.

        Args:
            fieldId (string): fieldId
            name (string): The name of the context.
            description (string): The description of the context.
            id (string): The ID of the context.
            issueTypeIds (array): The list of issue types IDs for the context. If the list is empty, the context refers to all issue types.
            projectIds (array): The list of project IDs associated with the context. If the list is empty, the context is global.
                Example:
                ```json
                {
                  "description": "A context used to define the custom field options for bugs.",
                  "issueTypeIds": [
                    "10010"
                  ],
                  "name": "Bug fields context",
                  "projectIds": []
                }
                ```

        Returns:
            dict[str, Any]: Returned if the custom field context is created.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        request_body = {
            'description': description,
            'id': id,
            'issueTypeIds': issueTypeIds,
            'name': name,
            'projectIds': projectIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_default_values(self, fieldId, contextId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves the default values for contexts of a specified custom field in Jira, including optional pagination parameters for larger datasets.

        Args:
            fieldId (string): fieldId
            contextId (array): The IDs of the contexts.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/defaultValue"
        query_params = {k: v for k, v in [('contextId', contextId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_default_values(self, fieldId, defaultValues=None) -> Any:
        """
        Sets the default value for a specified custom field context via the Jira REST API.

        Args:
            fieldId (string): fieldId
            defaultValues (array): defaultValues
                Example:
                ```json
                {
                  "defaultValues": [
                    {
                      "contextId": "10100",
                      "optionId": "10001",
                      "type": "option.single"
                    },
                    {
                      "contextId": "10101",
                      "optionId": "10003",
                      "type": "option.single"
                    },
                    {
                      "contextId": "10103",
                      "optionId": "10005",
                      "type": "option.single"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if operation is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        request_body = {
            'defaultValues': defaultValues,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/defaultValue"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_mappings_for_contexts(self, fieldId, contextId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of context to issue type mappings for a specified custom field using the Jira Cloud API, allowing for filters by context ID, start index, and maximum results.

        Args:
            fieldId (string): fieldId
            contextId (array): The ID of the context. To include multiple contexts, provide an ampersand-separated list. For example, `contextId=10001&contextId=10002`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if operation is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/issuetypemapping"
        query_params = {k: v for k, v in [('contextId', contextId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_custom_field_contexts_for_projects_and_issue_types(self, fieldId, mappings, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves and maps custom field contexts to specific projects and issue types for a given custom field ID.

        Args:
            fieldId (string): fieldId
            mappings (array): The project and issue type mappings.
                Example:
                ```json
                {
                  "mappings": [
                    {
                      "issueTypeId": "10000",
                      "projectId": "10000"
                    },
                    {
                      "issueTypeId": "10001",
                      "projectId": "10000"
                    },
                    {
                      "issueTypeId": "10002",
                      "projectId": "10001"
                    }
                  ]
                }
                ```
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        request_body = {
            'mappings': mappings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/mapping"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_context_mapping(self, fieldId, contextId=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves paginated mappings between projects and custom field contexts, optionally filtered by context ID.

        Args:
            fieldId (string): fieldId
            contextId (array): The list of context IDs. To include multiple context, separate IDs with ampersand: `contextId=10000&contextId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/projectmapping"
        query_params = {k: v for k, v in [('contextId', contextId), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_custom_field_context(self, fieldId, contextId) -> Any:
        """
        Deletes a custom field context in Jira using the provided `fieldId` and `contextId`, removing it from the system.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId

        Returns:
            Any: Returned if the context is deleted.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_custom_field_context(self, fieldId, contextId, description=None, name=None) -> Any:
        """
        Updates a custom field context's configuration in Jira, including associated projects and issue types.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            description (string): The description of the custom field context. The maximum length is 255 characters.
            name (string): The name of the custom field context. The name must be unique. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "description": "A context used to define the custom field options for bugs.",
                  "name": "Bug fields context"
                }
                ```

        Returns:
            Any: Returned if the context is updated.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_issue_types_to_context(self, fieldId, contextId, issueTypeIds) -> Any:
        """
        Updates the issue type associations for a specific custom field context in Jira using the specified field and context IDs.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            issueTypeIds (array): The list of issue type IDs.
                Example:
                ```json
                {
                  "issueTypeIds": [
                    "10001",
                    "10005",
                    "10006"
                  ]
                }
                ```

        Returns:
            Any: Returned if operation is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'issueTypeIds': issueTypeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/issuetype"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_issue_types_from_context(self, fieldId, contextId, issueTypeIds) -> Any:
        """
        Removes issue types from a custom field context in Jira, reverting them to apply to all issue types if none remain.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            issueTypeIds (array): The list of issue type IDs.
                Example:
                ```json
                {
                  "issueTypeIds": [
                    "10001",
                    "10005",
                    "10006"
                  ]
                }
                ```

        Returns:
            Any: Returned if operation is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'issueTypeIds': issueTypeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/issuetype/remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_options_for_context(self, fieldId, contextId, optionId=None, onlyOptions=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves and paginates custom field options (single/multiple choice values) for a specific field and context in Jira, including filtering by option ID.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            optionId (integer): The ID of the option.
            onlyOptions (boolean): Whether only options are returned.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option"
        query_params = {k: v for k, v in [('optionId', optionId), ('onlyOptions', onlyOptions), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_custom_field_option(self, fieldId, contextId, options=None) -> dict[str, Any]:
        """
        Creates new custom field options for a specific context in Jira using the POST method, allowing for the addition of options to select lists or similar fields.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            options (array): Details of options to create.
                Example:
                ```json
                {
                  "options": [
                    {
                      "disabled": false,
                      "value": "Scranton"
                    },
                    {
                      "disabled": true,
                      "optionId": "10000",
                      "value": "Manhattan"
                    },
                    {
                      "disabled": false,
                      "value": "The Electric City"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'options': options,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_custom_field_option(self, fieldId, contextId, options=None) -> dict[str, Any]:
        """
        Updates options for a custom field context in Jira using the provided field and context IDs, but this endpoint is not explicitly documented for a PUT method; typically, such endpoints involve updating or adding options to a select field within a specific context.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            options (array): Details of the options to update.
                Example:
                ```json
                {
                  "options": [
                    {
                      "disabled": false,
                      "id": "10001",
                      "value": "Scranton"
                    },
                    {
                      "disabled": true,
                      "id": "10002",
                      "value": "Manhattan"
                    },
                    {
                      "disabled": false,
                      "id": "10003",
                      "value": "The Electric City"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'options': options,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def reorder_custom_field_options(self, fieldId, contextId, customFieldOptionIds, after=None, position=None) -> Any:
        """
        Reorders custom field options or cascading options within a specified context using the provided IDs and position parameters.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            customFieldOptionIds (array): A list of IDs of custom field options to move. The order of the custom field option IDs in the list is the order they are given after the move. The list must contain custom field options or cascading options, but not both.
            after (string): The ID of the custom field option or cascading option to place the moved options after. Required if `position` isn't provided.
            position (string): The position the custom field options should be moved to. Required if `after` isn't provided.
                Example:
                ```json
                {
                  "customFieldOptionIds": [
                    "10001",
                    "10002"
                  ],
                  "position": "First"
                }
                ```

        Returns:
            Any: Returned if options are reordered.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'after': after,
            'customFieldOptionIds': customFieldOptionIds,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option/move"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_custom_field_option(self, fieldId, contextId, optionId) -> Any:
        """
        Deletes a specific custom field option within a designated custom field context in Jira.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            optionId (string): optionId

        Returns:
            Any: Returned if the option is deleted.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def replace_custom_field_option(self, fieldId, contextId, optionId, replaceWith=None, jql=None) -> Any:
        """
        Deletes a specific custom field option within a context for a Jira field, allowing optional replacement via query parameters.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            optionId (string): optionId
            replaceWith (integer): The ID of the option that will replace the currently selected option.
            jql (string): A JQL query that specifies the issues to be updated. For example, *project=10000*.

        Returns:
            Any: API response data.

        Tags:
            Issue custom field options
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/option/{optionId}/issue"
        query_params = {k: v for k, v in [('replaceWith', replaceWith), ('jql', jql)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_projects_to_custom_field_context(self, fieldId, contextId, projectIds) -> Any:
        """
        Updates a custom field context by adding a project to it, using the Jira Cloud platform REST API, and returns a status message based on the operation's success or failure.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            projectIds (array): The IDs of projects.
                Example:
                ```json
                {
                  "projectIds": [
                    "10001",
                    "10005",
                    "10006"
                  ]
                }
                ```

        Returns:
            Any: Returned if operation is successful.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'projectIds': projectIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_custom_field_context_from_projects(self, fieldId, contextId, projectIds) -> Any:
        """
        Removes specified projects from a custom field context in Jira, causing it to apply to all projects if no projects remain.

        Args:
            fieldId (string): fieldId
            contextId (string): contextId
            projectIds (array): The IDs of projects.
                Example:
                ```json
                {
                  "projectIds": [
                    "10001",
                    "10005",
                    "10006"
                  ]
                }
                ```

        Returns:
            Any: Returned if the custom field context is removed from the projects.

        Tags:
            Issue custom field contexts
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        if contextId is None:
            raise ValueError("Missing required parameter 'contextId'")
        request_body = {
            'projectIds': projectIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/context/{contextId}/project/remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_contexts_for_field_deprecated(self, fieldId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of contexts for a specified custom field in Jira, allowing filtering by start index and maximum number of results.

        Args:
            fieldId (string): fieldId
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue fields
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/contexts"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_screens_for_field(self, fieldId, startAt=None, maxResults=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of screens that include a specified field, identified by the `fieldId` parameter, allowing for pagination and expansion of results.

        Args:
            fieldId (string): fieldId
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            expand (string): Use [expand](#expansion) to include additional information about screens in the response. This parameter accepts `tab` which returns details about the screen tabs the field is used in.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screens
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldId}/screens"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_issue_field_options(self, fieldKey, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of all custom field options for a specified field, supporting pagination via startAt and maxResults parameters.

        Args:
            fieldKey (string): fieldKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_field_option(self, fieldKey, value, config=None, properties=None) -> dict[str, Any]:
        """
        Adds a new option to a specified custom field in Jira using the POST method, requiring the field's key as a path parameter.

        Args:
            fieldKey (string): fieldKey
            value (string): The option's name, which is displayed in Jira.
            config (object): Details of the projects the option is available in.
            properties (object): The properties of the option as arbitrary key-value pairs. These properties can be searched using JQL, if the extractions (see https://developer.atlassian.com/cloud/jira/platform/modules/issue-field-option-property-index/) are defined in the descriptor for the issue field module.
                Example:
                ```json
                {
                  "config": {
                    "attributes": [],
                    "scope": {
                      "global": {},
                      "projects": [],
                      "projects2": [
                        {
                          "attributes": [
                            "notSelectable"
                          ],
                          "id": 1001
                        },
                        {
                          "attributes": [
                            "notSelectable"
                          ],
                          "id": 1002
                        }
                      ]
                    }
                  },
                  "properties": {
                    "description": "The team's description",
                    "founded": "2016-06-06",
                    "leader": {
                      "email": "lname@example.com",
                      "name": "Leader Name"
                    },
                    "members": 42
                  },
                  "value": "Team 1"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        request_body = {
            'config': config,
            'properties': properties,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_selectable_issue_field_options(self, fieldKey, startAt=None, maxResults=None, projectId=None) -> dict[str, Any]:
        """
        Retrieves paginated suggestions for editable options of a specific custom field, filtered by project ID if provided, in Jira Cloud.

        Args:
            fieldKey (string): fieldKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            projectId (integer): Filters the results to options that are only available in the specified project.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/suggestions/edit"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_visible_issue_field_options(self, fieldKey, startAt=None, maxResults=None, projectId=None) -> dict[str, Any]:
        """
        Searches for and returns a list of option suggestions for a specific custom field in Jira, based on the provided field key, allowing for pagination using query parameters like `startAt` and `maxResults`.

        Args:
            fieldKey (string): fieldKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            projectId (integer): Filters the results to options that are only available in the specified project.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/suggestions/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_field_option(self, fieldKey, optionId) -> Any:
        """
        Deletes a specific custom field option in Jira and initiates asynchronous cleanup of associated issue data.

        Args:
            fieldKey (string): fieldKey
            optionId (string): optionId

        Returns:
            Any: Returned if the field option is deleted.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/{optionId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_field_option(self, fieldKey, optionId) -> dict[str, Any]:
        """
        Retrieves a specific custom field option's details for a given field key and option ID in Jira.

        Args:
            fieldKey (string): fieldKey
            optionId (string): optionId

        Returns:
            dict[str, Any]: Returned if the requested option is returned.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/{optionId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_field_option(self, fieldKey, optionId, id, value, config=None, properties=None) -> dict[str, Any]:
        """
        Updates a custom field option identified by its ID in Jira using the PUT method, allowing for modification of existing option details such as value or status.

        Args:
            fieldKey (string): fieldKey
            optionId (string): optionId
            id (integer): The unique identifier for the option. This is only unique within the select field's set of options.
            value (string): The option's name, which is displayed in Jira.
            config (object): Details of the projects the option is available in.
            properties (object): The properties of the object, as arbitrary key-value pairs. These properties can be searched using JQL, if the extractions (see [Issue Field Option Property Index](https://developer.atlassian.com/cloud/jira/platform/modules/issue-field-option-property-index/)) are defined in the descriptor for the issue field module.
                Example:
                ```json
                {
                  "config": {
                    "attributes": [],
                    "scope": {
                      "global": {},
                      "projects": [],
                      "projects2": [
                        {
                          "attributes": [
                            "notSelectable"
                          ],
                          "id": 1001
                        },
                        {
                          "attributes": [
                            "notSelectable"
                          ],
                          "id": 1002
                        }
                      ]
                    }
                  },
                  "id": 1,
                  "properties": {
                    "description": "The team's description",
                    "founded": "2016-06-06",
                    "leader": {
                      "email": "lname@example.com",
                      "name": "Leader Name"
                    },
                    "members": 42
                  },
                  "value": "Team 1"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the option is updated or created.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        request_body = {
            'config': config,
            'id': id,
            'properties': properties,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/{optionId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def replace_issue_field_option(self, fieldKey, optionId, replaceWith=None, jql=None, overrideScreenSecurity=None, overrideEditableFlag=None) -> Any:
        """
        Deletes a custom field option from specific issues using the Jira API, allowing for parameters such as replacing the option, filtering by JQL, and overriding screen security and editable flags.

        Args:
            fieldKey (string): fieldKey
            optionId (string): optionId
            replaceWith (integer): The ID of the option that will replace the currently selected option.
            jql (string): A JQL query that specifies the issues to be updated. For example, *project=10000*.
            overrideScreenSecurity (boolean): Whether screen security is overridden to enable hidden fields to be edited. Available to Connect and Forge app users with admin permission.
            overrideEditableFlag (boolean): Whether screen security is overridden to enable uneditable fields to be edited. Available to Connect and Forge app users with *Administer Jira* [global permission](

        Returns:
            Any: API response data.

        Tags:
            Issue custom field options (apps)
        """
        if fieldKey is None:
            raise ValueError("Missing required parameter 'fieldKey'")
        if optionId is None:
            raise ValueError("Missing required parameter 'optionId'")
        url = f"{self.base_url}/rest/api/3/field/{fieldKey}/option/{optionId}/issue"
        query_params = {k: v for k, v in [('replaceWith', replaceWith), ('jql', jql), ('overrideScreenSecurity', overrideScreenSecurity), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_custom_field(self, id) -> Any:
        """
        Deletes a custom field in Jira Cloud using the REST API with the "DELETE" method at the path "/rest/api/3/field/{id}", where "{id}" is the identifier of the field to be deleted.

        Args:
            id (string): id

        Returns:
            Any: API response data.

        Tags:
            Issue fields
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/field/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def restore_custom_field(self, id) -> Any:
        """
        Restores a custom field from trash in Jira using the specified field ID.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue fields
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/field/{id}/restore"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def trash_custom_field(self, id) -> Any:
        """
        Moves a custom field to trash in Jira using the specified field ID, requiring admin permissions.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue fields
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/field/{id}/trash"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_field_configurations(self, startAt=None, maxResults=None, id=None, isDefault=None, query=None) -> dict[str, Any]:
        """
        Retrieves field configurations from Jira using the GET method at the "/rest/api/3/fieldconfiguration" path, allowing filtering by parameters such as startAt, maxResults, id, isDefault, and query.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of field configuration IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.
            isDefault (boolean): If *true* returns default field configurations only.
            query (string): The query string used to match against field configuration names and descriptions.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        url = f"{self.base_url}/rest/api/3/fieldconfiguration"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('isDefault', isDefault), ('query', query)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_field_configuration(self, name, description=None) -> dict[str, Any]:
        """
        Creates a new field configuration in Jira to manage field visibility and behavior, returning the configuration details upon success.

        Args:
            name (string): The name of the field configuration. Must be unique.
            description (string): The description of the field configuration.
                Example:
                ```json
                {
                  "description": "My field configuration description",
                  "name": "My Field Configuration"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfiguration"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_field_configuration(self, id) -> Any:
        """
        Deletes a Jira field configuration by ID and returns a success status upon completion.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/fieldconfiguration/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_field_configuration(self, id, name, description=None) -> Any:
        """
        Updates a field configuration (name and description) in company-managed Jira projects, requiring Administer Jira permissions.

        Args:
            id (string): id
            name (string): The name of the field configuration. Must be unique.
            description (string): The description of the field configuration.
                Example:
                ```json
                {
                  "description": "A brand new description",
                  "name": "My Modified Field Configuration"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfiguration/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_field_configuration_items(self, id, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of fields associated with a field configuration specified by its ID, allowing pagination via optional startAt and maxResults parameters.

        Args:
            id (string): id
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/fieldconfiguration/{id}/fields"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_field_configuration_items(self, id, fieldConfigurationItems) -> Any:
        """
        Updates the fields of a field configuration in Jira using the PUT method with the specified configuration ID.

        Args:
            id (string): id
            fieldConfigurationItems (array): Details of fields in a field configuration.
                Example:
                ```json
                {
                  "fieldConfigurationItems": [
                    {
                      "description": "The new description of this item.",
                      "id": "customfield_10012",
                      "isHidden": false
                    },
                    {
                      "id": "customfield_10011",
                      "isRequired": true
                    },
                    {
                      "description": "Another new description.",
                      "id": "customfield_10010",
                      "isHidden": false,
                      "isRequired": false,
                      "renderer": "wiki-renderer"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'fieldConfigurationItems': fieldConfigurationItems,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfiguration/{id}/fields"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_field_configuration_schemes(self, startAt=None, maxResults=None, id=None) -> dict[str, Any]:
        """
        Retrieves field configuration schemes in Jira with support for pagination and optional ID filtering.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of field configuration scheme IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_field_configuration_scheme(self, name, description=None) -> dict[str, Any]:
        """
        Creates a field configuration scheme using the Jira Cloud platform REST API.

        Args:
            name (string): The name of the field configuration scheme. The name must be unique.
            description (string): The description of the field configuration scheme.
                Example:
                ```json
                {
                  "description": "We can use this one for software projects.",
                  "name": "Field Configuration Scheme for software related projects"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_field_configuration_scheme_mappings(self, startAt=None, maxResults=None, fieldConfigurationSchemeId=None) -> dict[str, Any]:
        """
        Retrieves mappings for a specified field configuration scheme using the Jira API, providing details of how fields are configured across projects.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            fieldConfigurationSchemeId (array): The list of field configuration scheme IDs. To include multiple field configuration schemes separate IDs with ampersand: `fieldConfigurationSchemeId=10000&fieldConfigurationSchemeId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/mapping"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('fieldConfigurationSchemeId', fieldConfigurationSchemeId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_field_configuration_scheme_project_mapping(self, projectId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of field configuration schemes for a specified project, including the projects that use each scheme, using the `GET` method at the `/rest/api/3/fieldconfigurationscheme/project` path.

        Args:
            projectId (array): The list of project IDs. To include multiple projects, separate IDs with ampersand: `projectId=10000&projectId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_field_configuration_scheme_to_project(self, projectId, fieldConfigurationSchemeId=None) -> Any:
        """
        Updates a field configuration scheme associated with a project using the Jira Cloud API, specifically for company-managed (classic) projects.

        Args:
            projectId (string): The ID of the project.
            fieldConfigurationSchemeId (string): The ID of the field configuration scheme. If the field configuration scheme ID is `null`, the operation assigns the default field configuration scheme.
                Example:
                ```json
                {
                  "fieldConfigurationSchemeId": "10000",
                  "projectId": "10000"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        request_body = {
            'fieldConfigurationSchemeId': fieldConfigurationSchemeId,
            'projectId': projectId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_field_configuration_scheme(self, id) -> Any:
        """
        Deletes a field configuration scheme from Jira by ID, requiring Administer Jira permissions.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_field_configuration_scheme(self, id, name, description=None) -> Any:
        """
        Updates a field configuration scheme using its ID, applicable only to company-managed projects, requiring the *Administer Jira* global permission.

        Args:
            id (string): id
            name (string): The name of the field configuration scheme. The name must be unique.
            description (string): The description of the field configuration scheme.
                Example:
                ```json
                {
                  "description": "We can use this one for software projects.",
                  "name": "Field Configuration Scheme for software related projects"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_field_configuration_scheme_mapping(self, id, mappings) -> Any:
        """
        Updates the field configuration scheme mapping using the Jira Cloud API and returns a status message.

        Args:
            id (string): id
            mappings (array): Field configuration to issue type mappings.
                Example:
                ```json
                {
                  "mappings": [
                    {
                      "fieldConfigurationId": "10000",
                      "issueTypeId": "default"
                    },
                    {
                      "fieldConfigurationId": "10002",
                      "issueTypeId": "10001"
                    },
                    {
                      "fieldConfigurationId": "10001",
                      "issueTypeId": "10002"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'mappings': mappings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/{id}/mapping"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_issue_types_from_global_field_configuration_scheme(self, id, issueTypeIds) -> Any:
        """
        Removes specified issue types from a field configuration scheme in Jira via a POST request.

        Args:
            id (string): id
            issueTypeIds (array): The list of issue type IDs. Must contain unique values not longer than 255 characters and not be empty. Maximum of 100 IDs.
                Example:
                ```json
                {
                  "issueTypeIds": [
                    "10000",
                    "10001",
                    "10002"
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue field configurations
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'issueTypeIds': issueTypeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/fieldconfigurationscheme/{id}/mapping/delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_filter(self, name, expand=None, overrideSharePermissions=None, approximateLastUsed=None, description=None, editPermissions=None, favourite=None, favouritedCount=None, id=None, jql=None, owner=None, searchUrl=None, self_arg_body=None, sharePermissions=None, sharedUsers=None, subscriptions=None, viewUrl=None) -> dict[str, Any]:
        """
        Creates a Jira filter with specified parameters such as name, JQL query, and visibility, returning the newly created filter details.

        Args:
            name (string): The name of the filter. Must be unique.
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.
            overrideSharePermissions (boolean): EXPERIMENTAL: Whether share permissions are overridden to enable filters with any share permissions to be created. Available to users with *Administer Jira* [global permission](
            approximateLastUsed (string): \[Experimental\] Approximate last used time. Returns the date and time when the filter was last used. Returns `null` if the filter hasn't been used after tracking was enabled. For performance reasons, timestamps aren't updated in real time and therefore may not be exactly accurate.
            description (string): A description of the filter.
            editPermissions (array): The groups and projects that can edit the filter.
            favourite (boolean): Whether the filter is selected as a favorite.
            favouritedCount (integer): The count of how many users have selected this filter as a favorite, including the filter owner.
            id (string): The unique identifier for the filter.
            jql (string): The JQL query for the filter. For example, *project = SSP AND issuetype = Bug*.
            owner (string): The user who owns the filter. This is defaulted to the creator of the filter, however Jira administrators can change the owner of a shared filter in the admin settings.
            searchUrl (string): A URL to view the filter results in Jira, using the [Search for issues using JQL](#api-rest-api-3-filter-search-get) operation with the filter's JQL string to return the filter results. For example, *https://your-domain.atlassian.net/rest/api/3/search?jql=project+%3D+SSP+AND+issuetype+%3D+Bug*.
            self_arg_body (string): The URL of the filter.
            sharePermissions (array): The groups and projects that the filter is shared with.
            sharedUsers (string): A paginated list of the users that the filter is shared with. This includes users that are members of the groups or can browse the projects that the filter is shared with.
            subscriptions (string): A paginated list of the users that are subscribed to the filter.
            viewUrl (string): A URL to view the filter results in Jira, using the ID of the filter. For example, *https://your-domain.atlassian.net/issues/?filter=10100*.
                Example:
                ```json
                {
                  "description": "Lists all open bugs",
                  "jql": "type = Bug and resolution is empty",
                  "name": "All Open Bugs"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        request_body = {
            'approximateLastUsed': approximateLastUsed,
            'description': description,
            'editPermissions': editPermissions,
            'favourite': favourite,
            'favouritedCount': favouritedCount,
            'id': id,
            'jql': jql,
            'name': name,
            'owner': owner,
            'searchUrl': searchUrl,
            'self': self_arg_body,
            'sharePermissions': sharePermissions,
            'sharedUsers': sharedUsers,
            'subscriptions': subscriptions,
            'viewUrl': viewUrl,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter"
        query_params = {k: v for k, v in [('expand', expand), ('overrideSharePermissions', overrideSharePermissions)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_default_share_scope(self) -> dict[str, Any]:
        """
        Retrieves the default sharing scope setting for Jira filters.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        url = f"{self.base_url}/rest/api/3/filter/defaultShareScope"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_default_share_scope(self, scope) -> dict[str, Any]:
        """
        Sets the default share scope for new filters and dashboards using the Jira Cloud REST API, allowing users to set the scope to either GLOBAL or PRIVATE.

        Args:
            scope (string): The scope of the default sharing for new filters and dashboards:

         *  `AUTHENTICATED` Shared with all logged-in users.
         *  `GLOBAL` Shared with all logged-in users. This shows as `AUTHENTICATED` in the response.
         *  `PRIVATE` Not shared with any users.
                Example:
                ```json
                {
                  "scope": "GLOBAL"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        request_body = {
            'scope': scope,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter/defaultShareScope"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_favourite_filters(self, expand=None) -> list[Any]:
        """
        Retrieves the user's visible favorite filters with optional expansion details.

        Args:
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        url = f"{self.base_url}/rest/api/3/filter/favourite"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_my_filters(self, expand=None, includeFavourites=None) -> list[Any]:
        """
        Retrieves a list of filters accessible by the user, with options to expand and include favorite filters, using the Jira REST API.

        Args:
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.
            includeFavourites (boolean): Include the user's favorite filters in the response.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        url = f"{self.base_url}/rest/api/3/filter/my"
        query_params = {k: v for k, v in [('expand', expand), ('includeFavourites', includeFavourites)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_filters_paginated(self, filterName=None, accountId=None, owner=None, groupname=None, groupId=None, projectId=None, id=None, orderBy=None, startAt=None, maxResults=None, expand=None, overrideSharePermissions=None, isSubstringMatch=None) -> dict[str, Any]:
        """
        Retrieves a list of filters accessible to the user based on parameters like name, owner, project, or group, supporting pagination and substring matching.

        Args:
            filterName (string): String used to perform a case-insensitive partial match with `name`.
            accountId (string): User account ID used to return filters with the matching `owner.accountId`. This parameter cannot be used with `owner`.
            owner (string): This parameter is deprecated because of privacy changes. Use `accountId` instead. See the [migration guide]( for details. User name used to return filters with the matching `owner.name`. This parameter cannot be used with `accountId`.
            groupname (string): As a group's name can change, use of `groupId` is recommended to identify a group. Group name used to returns filters that are shared with a group that matches `sharePermissions.group.groupname`. This parameter cannot be used with the `groupId` parameter.
            groupId (string): Group ID used to returns filters that are shared with a group that matches `sharePermissions.group.groupId`. This parameter cannot be used with the `groupname` parameter.
            projectId (integer): Project ID used to returns filters that are shared with a project that matches `sharePermissions.project.id`.
            id (array): The list of filter IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`. Do not exceed 200 filter IDs.
            orderBy (string): [Order](#ordering) the results by a field: * `description` Sorts by filter description. Note that this sorting works independently of whether the expand to display the description field is in use. * `favourite_count` Sorts by the count of how many users have this filter as a favorite. * `is_favourite` Sorts by whether the filter is marked as a favorite. * `id` Sorts by filter ID. * `name` Sorts by filter name. * `owner` Sorts by the ID of the filter owner. * `is_shared` Sorts by whether the filter is shared.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `description` Returns the description of the filter. * `favourite` Returns an indicator of whether the user has set the filter as a favorite. * `favouritedCount` Returns a count of how many users have set this filter as a favorite. * `jql` Returns the JQL query that the filter uses. * `owner` Returns the owner of the filter. * `searchUrl` Returns a URL to perform the filter's JQL query. * `sharePermissions` Returns the share permissions defined for the filter. * `editPermissions` Returns the edit permissions defined for the filter. * `isWritable` Returns whether the current user has permission to edit the filter. * `approximateLastUsed` \[Experimental\] Returns the approximate date and time when the filter was last evaluated. * `subscriptions` Returns the users that are subscribed to the filter. * `viewUrl` Returns a URL to view the filter.
            overrideSharePermissions (boolean): EXPERIMENTAL: Whether share permissions are overridden to enable filters with any share permissions to be returned. Available to users with *Administer Jira* [global permission](
            isSubstringMatch (boolean): When `true` this will perform a case-insensitive substring match for the provided `filterName`. When `false` the filter name will be searched using [full text search syntax](

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        url = f"{self.base_url}/rest/api/3/filter/search"
        query_params = {k: v for k, v in [('filterName', filterName), ('accountId', accountId), ('owner', owner), ('groupname', groupname), ('groupId', groupId), ('projectId', projectId), ('id', id), ('orderBy', orderBy), ('startAt', startAt), ('maxResults', maxResults), ('expand', expand), ('overrideSharePermissions', overrideSharePermissions), ('isSubstringMatch', isSubstringMatch)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_filter(self, id) -> Any:
        """
        Deletes a specific Jira filter by its ID using the Jira API and returns a success status if the operation is successful.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_filter(self, id, expand=None, overrideSharePermissions=None) -> dict[str, Any]:
        """
        Retrieves a specific filter's details by ID from Jira, optionally expanding fields or overriding share permissions.

        Args:
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.
            overrideSharePermissions (boolean): EXPERIMENTAL: Whether share permissions are overridden to enable filters with any share permissions to be returned. Available to users with *Administer Jira* [global permission](

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}"
        query_params = {k: v for k, v in [('expand', expand), ('overrideSharePermissions', overrideSharePermissions)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_filter(self, id, name, expand=None, overrideSharePermissions=None, approximateLastUsed=None, description=None, editPermissions=None, favourite=None, favouritedCount=None, id_body=None, jql=None, owner=None, searchUrl=None, self_arg_body=None, sharePermissions=None, sharedUsers=None, subscriptions=None, viewUrl=None) -> dict[str, Any]:
        """
        Updates an existing Jira filter (including permissions if overrideSharePermissions is specified) and returns the modified filter.

        Args:
            id (string): id
            name (string): The name of the filter. Must be unique.
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.
            overrideSharePermissions (boolean): EXPERIMENTAL: Whether share permissions are overridden to enable the addition of any share permissions to filters. Available to users with *Administer Jira* [global permission](
            approximateLastUsed (string): \[Experimental\] Approximate last used time. Returns the date and time when the filter was last used. Returns `null` if the filter hasn't been used after tracking was enabled. For performance reasons, timestamps aren't updated in real time and therefore may not be exactly accurate.
            description (string): A description of the filter.
            editPermissions (array): The groups and projects that can edit the filter.
            favourite (boolean): Whether the filter is selected as a favorite.
            favouritedCount (integer): The count of how many users have selected this filter as a favorite, including the filter owner.
            id_body (string): The unique identifier for the filter.
            jql (string): The JQL query for the filter. For example, *project = SSP AND issuetype = Bug*.
            owner (string): The user who owns the filter. This is defaulted to the creator of the filter, however Jira administrators can change the owner of a shared filter in the admin settings.
            searchUrl (string): A URL to view the filter results in Jira, using the [Search for issues using JQL](#api-rest-api-3-filter-search-get) operation with the filter's JQL string to return the filter results. For example, *https://your-domain.atlassian.net/rest/api/3/search?jql=project+%3D+SSP+AND+issuetype+%3D+Bug*.
            self_arg_body (string): The URL of the filter.
            sharePermissions (array): The groups and projects that the filter is shared with.
            sharedUsers (string): A paginated list of the users that the filter is shared with. This includes users that are members of the groups or can browse the projects that the filter is shared with.
            subscriptions (string): A paginated list of the users that are subscribed to the filter.
            viewUrl (string): A URL to view the filter results in Jira, using the ID of the filter. For example, *https://your-domain.atlassian.net/issues/?filter=10100*.
                Example:
                ```json
                {
                  "description": "Lists all open bugs",
                  "jql": "type = Bug and resolution is empty",
                  "name": "All Open Bugs"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'approximateLastUsed': approximateLastUsed,
            'description': description,
            'editPermissions': editPermissions,
            'favourite': favourite,
            'favouritedCount': favouritedCount,
            'id': id_body,
            'jql': jql,
            'name': name,
            'owner': owner,
            'searchUrl': searchUrl,
            'self': self_arg_body,
            'sharePermissions': sharePermissions,
            'sharedUsers': sharedUsers,
            'subscriptions': subscriptions,
            'viewUrl': viewUrl,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter/{id}"
        query_params = {k: v for k, v in [('expand', expand), ('overrideSharePermissions', overrideSharePermissions)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def reset_columns(self, id) -> Any:
        """
        Deletes the columns configuration for a specific filter in Jira using the filter ID.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/columns"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_columns(self, id) -> list[Any]:
        """
        Retrieves the column configuration for a specified filter in Jira using the filter ID.

        Args:
            id (string): id

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/columns"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_columns(self, id, columns=None) -> Any:
        """
        Updates the columns of a specific filter in Jira using the REST API and returns a response indicating the status of the update operation.

        Args:
            id (string): id
            columns (array): columns

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'columns': columns,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter/{id}/columns"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_favourite_for_filter(self, id, expand=None) -> dict[str, Any]:
        """
        Removes a filter with the specified ID from the user's favorites list using the Jira Cloud API.

        Args:
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/favourite"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_favourite_for_filter(self, id, expand=None) -> dict[str, Any]:
        """
        Adds a filter to the user's favorites list in Jira and returns the updated filter details.

        Args:
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include: * `sharedUsers` Returns the users that the filter is shared with. This includes users that can browse projects that the filter is shared with. If you don't specify `sharedUsers`, then the `sharedUsers` object is returned but it doesn't list any users. The list of users returned is limited to 1000, to access additional users append `[start-index:end-index]` to the expand request. For example, to access the next 1000 users, use `?expand=sharedUsers[1001:2000]`. * `subscriptions` Returns the users that are subscribed to the filter. If you don't specify `subscriptions`, the `subscriptions` object is returned but it doesn't list any subscriptions. The list of subscriptions returned is limited to 1000, to access additional subscriptions append `[start-index:end-index]` to the expand request. For example, to access the next 1000 subscriptions, use `?expand=subscriptions[1001:2000]`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/favourite"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._put(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def change_filter_owner(self, id, accountId) -> Any:
        """
        Updates the owner of a Jira filter specified by ID via PUT request, requiring admin rights or ownership and returning a 204 status on success.

        Args:
            id (string): id
            accountId (string): The account ID of the new owner.
                Example:
                ```json
                {
                  "accountId": "0000-0000-0000-0000"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Filters
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'accountId': accountId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter/{id}/owner"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_share_permissions(self, id) -> list[Any]:
        """
        Retrieves the permissions for a specific Jira filter identified by its ID using the GET method, returning details about the permissions assigned to the filter.

        Args:
            id (string): id

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/permission"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_share_permission(self, id, type, accountId=None, groupId=None, groupname=None, projectId=None, projectRoleId=None, rights=None) -> list[Any]:
        """
        Adds permissions to an existing filter using the filter ID, allowing control over who can access or modify the filter via the API.

        Args:
            id (string): id
            type (string): The type of the share permission.Specify the type as follows:

         *  `user` Share with a user.
         *  `group` Share with a group. Specify `groupname` as well.
         *  `project` Share with a project. Specify `projectId` as well.
         *  `projectRole` Share with a project role in a project. Specify `projectId` and `projectRoleId` as well.
         *  `global` Share globally, including anonymous users. If set, this type overrides all existing share permissions and must be deleted before any non-global share permissions is set.
         *  `authenticated` Share with all logged-in users. This shows as `loggedin` in the response. If set, this type overrides all existing share permissions and must be deleted before any non-global share permissions is set.
            accountId (string): The user account ID that the filter is shared with. For a request, specify the `accountId` property for the user.
            groupId (string): The ID of the group, which uniquely identifies the group across all Atlassian products.For example, *952d12c3-5b5b-4d04-bb32-44d383afc4b2*. Cannot be provided with `groupname`.
            groupname (string): The name of the group to share the filter with. Set `type` to `group`. Please note that the name of a group is mutable, to reliably identify a group use `groupId`.
            projectId (string): The ID of the project to share the filter with. Set `type` to `project`.
            projectRoleId (string): The ID of the project role to share the filter with. Set `type` to `projectRole` and the `projectId` for the project that the role is in.
            rights (integer): The rights for the share permission.
                Example:
                ```json
                {
                  "groupname": "jira-administrators",
                  "rights": 1,
                  "type": "group"
                }
                ```

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'accountId': accountId,
            'groupId': groupId,
            'groupname': groupname,
            'projectId': projectId,
            'projectRoleId': projectRoleId,
            'rights': rights,
            'type': type,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/filter/{id}/permission"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_share_permission(self, id, permissionId) -> Any:
        """
        Deletes a specific permission associated with a filter in Jira using the REST API.

        Args:
            id (string): id
            permissionId (string): permissionId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if permissionId is None:
            raise ValueError("Missing required parameter 'permissionId'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/permission/{permissionId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_share_permission(self, id, permissionId) -> dict[str, Any]:
        """
        Retrieves the specified permission details for a given filter ID in the API, allowing access to specific permission information.

        Args:
            id (string): id
            permissionId (string): permissionId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Filter sharing
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if permissionId is None:
            raise ValueError("Missing required parameter 'permissionId'")
        url = f"{self.base_url}/rest/api/3/filter/{id}/permission/{permissionId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_group(self, groupname=None, groupId=None, swapGroup=None, swapGroupId=None) -> Any:
        """
        Deletes a group from the organization's directory using the `DELETE` method, allowing for optional group swapping, and returns a status message based on the operation's success or failure.

        Args:
            groupname (string): The name of the group to be deleted, specified as a query parameter.
            groupId (string): The ID of the group. This parameter cannot be used with the `groupname` parameter.
            swapGroup (string): As a group's name can change, use of `swapGroupId` is recommended to identify a group. The group to transfer restrictions to. Only comments and worklogs are transferred. If restrictions are not transferred, comments and worklogs are inaccessible after the deletion. This parameter cannot be used with the `swapGroupId` parameter.
            swapGroupId (string): The ID of the group to transfer restrictions to. Only comments and worklogs are transferred. If restrictions are not transferred, comments and worklogs are inaccessible after the deletion. This parameter cannot be used with the `swapGroup` parameter.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/group"
        query_params = {k: v for k, v in [('groupname', groupname), ('groupId', groupId), ('swapGroup', swapGroup), ('swapGroupId', swapGroupId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_group(self, groupname=None, groupId=None, expand=None) -> dict[str, Any]:
        """
        Retrieves group information from Jira by group name or ID, optionally expanding the response with additional details.

        Args:
            groupname (string): As a group's name can change, use of `groupId` is recommended to identify a group. The name of the group. This parameter cannot be used with the `groupId` parameter.
            groupId (string): The ID of the group. This parameter cannot be used with the `groupName` parameter.
            expand (string): List of fields to expand.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/group"
        query_params = {k: v for k, v in [('groupname', groupname), ('groupId', groupId), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_group(self, name) -> dict[str, Any]:
        """
        Creates a new group using the Jira Cloud REST API and returns a response indicating the creation status.

        Args:
            name (string): The name of the group.
                Example:
                ```json
                {
                  "name": "power-users"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/group"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_get_groups(self, startAt=None, maxResults=None, groupId=None, groupName=None, accessType=None, applicationKey=None) -> dict[str, Any]:
        """
        Retrieves multiple groups in bulk from Jira Cloud based on query parameters such as group IDs, names, and access types.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            groupId (array): The ID of a group. To specify multiple IDs, pass multiple `groupId` parameters. For example, `groupId=5b10a2844c20165700ede21g&groupId=5b10ac8d82e05b22cc7d4ef5`. Example: '3571b9a7-348f-414a-9087-8e1ea03a7df8'.
            groupName (array): The name of a group. To specify multiple names, pass multiple `groupName` parameters. For example, `groupName=administrators&groupName=jira-software-users`.
            accessType (string): The access level of a group. Valid values: 'site-admin', 'admin', 'user'.
            applicationKey (string): The application key of the product user groups to search for. Valid values: 'jira-servicedesk', 'jira-software', 'jira-product-discovery', 'jira-core'.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/group/bulk"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('groupId', groupId), ('groupName', groupName), ('accessType', accessType), ('applicationKey', applicationKey)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_users_from_group(self, groupname=None, groupId=None, includeInactiveUsers=None, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves paginated members of a Jira group with optional filtering for inactive users, supporting group identification via name or ID.

        Args:
            groupname (string): As a group's name can change, use of `groupId` is recommended to identify a group. The name of the group. This parameter cannot be used with the `groupId` parameter.
            groupId (string): The ID of the group. This parameter cannot be used with the `groupName` parameter.
            includeInactiveUsers (boolean): Include inactive users.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page (number should be between 1 and 50).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/group/member"
        query_params = {k: v for k, v in [('groupname', groupname), ('groupId', groupId), ('includeInactiveUsers', includeInactiveUsers), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_user_from_group(self, accountId, groupname=None, groupId=None, username=None) -> Any:
        """
        Removes a specified user from a group in Jira Cloud using account ID, username, groupname, or groupId as parameters.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            groupname (string): As a group's name can change, use of `groupId` is recommended to identify a group. The name of the group. This parameter cannot be used with the `groupId` parameter.
            groupId (string): The ID of the group. This parameter cannot be used with the `groupName` parameter.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/group/user"
        query_params = {k: v for k, v in [('groupname', groupname), ('groupId', groupId), ('username', username), ('accountId', accountId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_user_to_group(self, groupname=None, groupId=None, accountId=None, name=None) -> dict[str, Any]:
        """
        Adds a user to a specified Jira group using the "POST" method at the "/rest/api/3/group/user" endpoint, requiring a group ID or name to identify the target group.

        Args:
            groupname (string): As a group's name can change, use of `groupId` is recommended to identify a group. The name of the group. This parameter cannot be used with the `groupId` parameter.
            groupId (string): The ID of the group. This parameter cannot be used with the `groupName` parameter.
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*.
            name (string): This property is no longer available. See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
                Example:
                ```json
                {
                  "accountId": "5b10ac8d82e05b22cc7d4ef5"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        request_body = {
            'accountId': accountId,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/group/user"
        query_params = {k: v for k, v in [('groupname', groupname), ('groupId', groupId)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_groups(self, accountId=None, query=None, exclude=None, excludeId=None, maxResults=None, caseInsensitive=None, userName=None) -> dict[str, Any]:
        """
        Searches for groups matching query parameters and returns results with highlighted matches and a picker-friendly header indicating the number of matching groups.

        Args:
            accountId (string): This parameter is deprecated, setting it does not affect the results. To find groups containing a particular user, use [Get user groups](#api-rest-api-3-user-groups-get).
            query (string): The string to find in group names. Example: 'query'.
            exclude (array): As a group's name can change, use of `excludeGroupIds` is recommended to identify a group. A group to exclude from the result. To exclude multiple groups, provide an ampersand-separated list. For example, `exclude=group1&exclude=group2`. This parameter cannot be used with the `excludeGroupIds` parameter.
            excludeId (array): A group ID to exclude from the result. To exclude multiple groups, provide an ampersand-separated list. For example, `excludeId=group1-id&excludeId=group2-id`. This parameter cannot be used with the `excludeGroups` parameter.
            maxResults (integer): The maximum number of groups to return. The maximum number of groups that can be returned is limited by the system property `jira.ajax.autocomplete.limit`.
            caseInsensitive (boolean): Whether the search for groups should be case insensitive.
            userName (string): This parameter is no longer available. See the [deprecation notice]( for details.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Groups
        """
        url = f"{self.base_url}/rest/api/3/groups/picker"
        query_params = {k: v for k, v in [('accountId', accountId), ('query', query), ('exclude', exclude), ('excludeId', excludeId), ('maxResults', maxResults), ('caseInsensitive', caseInsensitive), ('userName', userName)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_and_groups(self, query, maxResults=None, showAvatar=None, fieldId=None, projectId=None, issueTypeId=None, avatarSize=None, caseInsensitive=None, excludeConnectAddons=None) -> dict[str, Any]:
        """
        Searches for users and groups matching a query string in Jira Cloud and returns results with HTML highlighting for picker fields.

        Args:
            query (string): The search string.
            maxResults (integer): The maximum number of items to return in each list.
            showAvatar (boolean): Whether the user avatar should be returned. If an invalid value is provided, the default value is used.
            fieldId (string): The custom field ID of the field this request is for.
            projectId (array): The ID of a project that returned users and groups must have permission to view. To include multiple projects, provide an ampersand-separated list. For example, `projectId=10000&projectId=10001`. This parameter is only used when `fieldId` is present.
            issueTypeId (array): The ID of an issue type that returned users and groups must have permission to view. To include multiple issue types, provide an ampersand-separated list. For example, `issueTypeId=10000&issueTypeId=10001`. Special values, such as `-1` (all standard issue types) and `-2` (all subtask issue types), are supported. This parameter is only used when `fieldId` is present.
            avatarSize (string): The size of the avatar to return. If an invalid value is provided, the default value is used.
            caseInsensitive (boolean): Whether the search for groups should be case insensitive.
            excludeConnectAddons (boolean): Whether Connect app users and groups should be excluded from the search results. If an invalid value is provided, the default value is used.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Group and user picker
        """
        url = f"{self.base_url}/rest/api/3/groupuserpicker"
        query_params = {k: v for k, v in [('query', query), ('maxResults', maxResults), ('showAvatar', showAvatar), ('fieldId', fieldId), ('projectId', projectId), ('issueTypeId', issueTypeId), ('avatarSize', avatarSize), ('caseInsensitive', caseInsensitive), ('excludeConnectAddons', excludeConnectAddons)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_license(self) -> dict[str, Any]:
        """
        Retrieves licensing information about a Jira instance, returning details such as license metrics using the Jira Cloud REST API.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            License metrics
        """
        url = f"{self.base_url}/rest/api/3/instance/license"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue(self, updateHistory=None, fields=None, historyMetadata=None, properties=None, transition=None, update=None) -> dict[str, Any]:
        """
        Creates a new Jira issue using the specified project and issue type, returning a successful creation response if valid.

        Args:
            updateHistory (boolean): Whether the project in which the issue is created is added to the user's **Recently viewed** project list, as shown under **Projects** in Jira. When provided, the issue type and request type are added to the user's history for a project. These values are then used to provide defaults on the issue create screen.
            fields (object): List of issue screen fields to update, specifying the sub-field to update and its value for each field. This field provides a straightforward option when setting a sub-field. When multiple sub-fields or other operations are required, use `update`. Fields included in here cannot be included in `update`.
            historyMetadata (string): Additional issue history details.
            properties (array): Details of issue properties to be add or update.
            transition (string): Details of a transition. Required when performing a transition, optional when creating or editing an issue.
            update (object): A Map containing the field field name and a list of operations to perform on the issue screen field. Note that fields included in here cannot be included in `fields`.
                Example:
                ```json
                {
                  "fields": {
                    "assignee": {
                      "id": "5b109f2e9729b51b54dc274d"
                    },
                    "components": [
                      {
                        "id": "10000"
                      }
                    ],
                    "customfield_10000": "09/Jun/19",
                    "customfield_20000": "06/Jul/19 3:25 PM",
                    "customfield_30000": [
                      "10000",
                      "10002"
                    ],
                    "customfield_40000": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "Occurs on all orders",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "customfield_50000": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "Could impact day-to-day work.",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "customfield_60000": "jira-software-users",
                    "customfield_70000": [
                      "jira-administrators",
                      "jira-software-users"
                    ],
                    "customfield_80000": {
                      "value": "red"
                    },
                    "description": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "Order entry fails when selecting supplier.",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "duedate": "2019-05-11",
                    "environment": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "UAT",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "fixVersions": [
                      {
                        "id": "10001"
                      }
                    ],
                    "issuetype": {
                      "id": "10000"
                    },
                    "labels": [
                      "bugfix",
                      "blitz_test"
                    ],
                    "parent": {
                      "key": "PROJ-123"
                    },
                    "priority": {
                      "id": "20000"
                    },
                    "project": {
                      "id": "10000"
                    },
                    "reporter": {
                      "id": "5b10a2844c20165700ede21g"
                    },
                    "security": {
                      "id": "10000"
                    },
                    "summary": "Main order flow broken",
                    "timetracking": {
                      "originalEstimate": "10",
                      "remainingEstimate": "5"
                    },
                    "versions": [
                      {
                        "id": "10000"
                      }
                    ]
                  },
                  "update": {}
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues, important
        """
        request_body = {
            'fields': fields,
            'historyMetadata': historyMetadata,
            'properties': properties,
            'transition': transition,
            'update': update,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue"
        query_params = {k: v for k, v in [('updateHistory', updateHistory)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def archive_issues_async(self, jql=None) -> Any:
        """
        Archives Jira issues via ID/key using a POST request, returning async status codes for success/failure.

        Args:
            jql (string): jql
                Example:
                ```json
                {
                  "jql": "project = FOO AND updated < -2y"
                }
                ```

        Returns:
            Any: Returns the URL to check the status of the submitted request.

        Tags:
            Issues
        """
        request_body = {
            'jql': jql,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/archive"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def archive_issues(self, issueIdsOrKeys=None) -> dict[str, Any]:
        """
        Archives Jira issues via the specified issue IDs/keys using the PUT method, handling bulk operations and returning status/error details.

        Args:
            issueIdsOrKeys (array): issueIdsOrKeys
                Example:
                ```json
                {
                  "issueIdsOrKeys": [
                    "PR-1",
                    "1001",
                    "PROJECT-2"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if there is at least one valid issue to archive in the request. The return message will include the count of archived issues and subtasks, as well as error details for issues which failed to get archived.

        Tags:
            Issues
        """
        request_body = {
            'issueIdsOrKeys': issueIdsOrKeys,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/archive"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issues(self, issueUpdates=None) -> dict[str, Any]:
        """
        Performs bulk operations on Jira issues, such as moving or editing multiple issues at once, using the POST method at the "/rest/api/3/issue/bulk" endpoint.

        Args:
            issueUpdates (array): issueUpdates
                Example:
                ```json
                {
                  "issueUpdates": [
                    {
                      "fields": {
                        "assignee": {
                          "id": "5b109f2e9729b51b54dc274d"
                        },
                        "components": [
                          {
                            "id": "10000"
                          }
                        ],
                        "customfield_10000": "09/Jun/19",
                        "customfield_20000": "06/Jul/19 3:25 PM",
                        "customfield_30000": [
                          "10000",
                          "10002"
                        ],
                        "customfield_40000": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Occurs on all orders",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "customfield_50000": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Could impact day-to-day work.",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "customfield_60000": "jira-software-users",
                        "customfield_70000": [
                          "jira-administrators",
                          "jira-software-users"
                        ],
                        "customfield_80000": {
                          "value": "red"
                        },
                        "description": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Order entry fails when selecting supplier.",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "duedate": "2011-03-11",
                        "environment": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "UAT",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "fixVersions": [
                          {
                            "id": "10001"
                          }
                        ],
                        "issuetype": {
                          "id": "10000"
                        },
                        "labels": [
                          "bugfix",
                          "blitz_test"
                        ],
                        "priority": {
                          "id": "20000"
                        },
                        "project": {
                          "id": "10000"
                        },
                        "reporter": {
                          "id": "5b10a2844c20165700ede21g"
                        },
                        "security": {
                          "id": "10000"
                        },
                        "summary": "Main order flow broken",
                        "timetracking": {
                          "originalEstimate": "10",
                          "remainingEstimate": "5"
                        },
                        "versions": [
                          {
                            "id": "10000"
                          }
                        ]
                      },
                      "update": {
                        "worklog": [
                          {
                            "add": {
                              "started": "2019-07-05T11:05:00.000+0000",
                              "timeSpent": "60m"
                            }
                          }
                        ]
                      }
                    },
                    {
                      "fields": {
                        "assignee": {
                          "id": "5b109f2e9729b51b54dc274d"
                        },
                        "components": [
                          {
                            "id": "10000"
                          }
                        ],
                        "customfield_10000": "09/Jun/19",
                        "customfield_20000": "06/Jul/19 3:25 PM",
                        "customfield_30000": [
                          "10000",
                          "10002"
                        ],
                        "customfield_40000": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Occurs on all orders",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "customfield_50000": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Could impact day-to-day work.",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "customfield_60000": "jira-software-users",
                        "customfield_70000": [
                          "jira-administrators",
                          "jira-software-users"
                        ],
                        "customfield_80000": {
                          "value": "red"
                        },
                        "description": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "Order remains pending after approved.",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "duedate": "2019-04-16",
                        "environment": {
                          "content": [
                            {
                              "content": [
                                {
                                  "text": "UAT",
                                  "type": "text"
                                }
                              ],
                              "type": "paragraph"
                            }
                          ],
                          "type": "doc",
                          "version": 1
                        },
                        "fixVersions": [
                          {
                            "id": "10001"
                          }
                        ],
                        "issuetype": {
                          "id": "10000"
                        },
                        "labels": [
                          "new_release"
                        ],
                        "priority": {
                          "id": "20000"
                        },
                        "project": {
                          "id": "1000"
                        },
                        "reporter": {
                          "id": "5b10a2844c20165700ede21g"
                        },
                        "security": {
                          "id": "10000"
                        },
                        "summary": "Order stuck in pending",
                        "timetracking": {
                          "originalEstimate": "15",
                          "remainingEstimate": "5"
                        },
                        "versions": [
                          {
                            "id": "10000"
                          }
                        ]
                      },
                      "update": {}
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if any of the issue or subtask creation requests were successful. A request may be unsuccessful when it:

         *  is missing required fields.
         *  contains invalid field values.
         *  contains fields that cannot be set for the issue type.
         *  is by a user who does not have the necessary permission.
         *  is to create a subtype in a project different that of the parent issue.
         *  is for a subtask when the option to create subtasks is disabled.
         *  is invalid for any other reason.

        Tags:
            Issues
        """
        request_body = {
            'issueUpdates': issueUpdates,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/bulk"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_fetch_issues(self, issueIdsOrKeys, expand=None, fields=None, fieldsByKeys=None, properties=None) -> dict[str, Any]:
        """
        Fetches multiple issues in bulk from Jira using the POST method at "/rest/api/3/issue/bulkfetch", returning the specified issues based on provided issue IDs or keys.

        Args:
            issueIdsOrKeys (array): An array of issue IDs or issue keys to fetch. You can mix issue IDs and keys in the same query.
            expand (array): Use [expand](#expansion) to include additional information about issues in the response. Note that, unlike the majority of instances where `expand` is specified, `expand` is defined as a list of values. The expand options are:

         *  `renderedFields` Returns field values rendered in HTML format.
         *  `names` Returns the display name of each field.
         *  `schema` Returns the schema describing a field type.
         *  `transitions` Returns all possible transitions for the issue.
         *  `operations` Returns all possible operations for the issue.
         *  `editmeta` Returns information about how each field can be edited.
         *  `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent.
         *  `versionedRepresentations` Instead of `fields`, returns `versionedRepresentations` a JSON array containing each version of a field's value, with the highest numbered item representing the most recent version.
            fields (array): A list of fields to return for each issue, use it to retrieve a subset of fields. This parameter accepts a comma-separated list. Expand options include:

         *  `*all` Returns all fields.
         *  `*navigable` Returns navigable fields.
         *  Any issue field, prefixed with a minus to exclude.

        The default is `*navigable`.

        Examples:

         *  `summary,comment` Returns the summary and comments fields only.
         *  `-description` Returns all navigable (default) fields except description.
         *  `*all,-comment` Returns all fields except comments.

        Multiple `fields` parameters can be included in a request.

        Note: All navigable fields are returned by default. This differs from [GET issue](#api-rest-api-3-issue-issueIdOrKey-get) where the default is all fields.
            fieldsByKeys (boolean): Reference fields by their key (rather than ID). The default is `false`.
            properties (array): A list of issue property keys of issue properties to be included in the results. A maximum of 5 issue property keys can be specified.
                Example:
                ```json
                {
                  "expand": [
                    "names"
                  ],
                  "fields": [
                    "summary",
                    "project",
                    "assignee"
                  ],
                  "fieldsByKeys": false,
                  "issueIdsOrKeys": [
                    "EX-1",
                    "EX-2",
                    "10005"
                  ],
                  "properties": []
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful. A response may contain both successful issues and issue errors.

        Tags:
            Issues, important
        """
        request_body = {
            'expand': expand,
            'fields': fields,
            'fieldsByKeys': fieldsByKeys,
            'issueIdsOrKeys': issueIdsOrKeys,
            'properties': properties,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/bulkfetch"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_create_issue_meta(self, projectIds=None, projectKeys=None, issuetypeIds=None, issuetypeNames=None, expand=None) -> dict[str, Any]:
        """
        Retrieves metadata including required fields, default values, and allowed configurations for creating Jira issues based on specified projects and issue types.

        Args:
            projectIds (array): List of project IDs. This parameter accepts a comma-separated list. Multiple project IDs can also be provided using an ampersand-separated list. For example, `projectIds=10000,10001&projectIds=10020,10021`. This parameter may be provided with `projectKeys`.
            projectKeys (array): List of project keys. This parameter accepts a comma-separated list. Multiple project keys can also be provided using an ampersand-separated list. For example, `projectKeys=proj1,proj2&projectKeys=proj3`. This parameter may be provided with `projectIds`.
            issuetypeIds (array): List of issue type IDs. This parameter accepts a comma-separated list. Multiple issue type IDs can also be provided using an ampersand-separated list. For example, `issuetypeIds=10000,10001&issuetypeIds=10020,10021`. This parameter may be provided with `issuetypeNames`.
            issuetypeNames (array): List of issue type names. This parameter accepts a comma-separated list. Multiple issue type names can also be provided using an ampersand-separated list. For example, `issuetypeNames=name1,name2&issuetypeNames=name3`. This parameter may be provided with `issuetypeIds`.
            expand (string): Use [expand](#expansion) to include additional information about issue metadata in the response. This parameter accepts `projects.issuetypes.fields`, which returns information about the fields in the issue creation screen for each issue type. Fields hidden from the screen are not returned. Use the information to populate the `fields` and `update` fields in [Create issue](#api-rest-api-3-issue-post) and [Create issues](#api-rest-api-3-issue-bulk-post).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        url = f"{self.base_url}/rest/api/3/issue/createmeta"
        query_params = {k: v for k, v in [('projectIds', projectIds), ('projectKeys', projectKeys), ('issuetypeIds', issuetypeIds), ('issuetypeNames', issuetypeNames), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_create_issue_meta_issue_types(self, projectIdOrKey, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves metadata for creating issues in Jira for a specific project's issue types, including available fields and mandatory requirements.

        Args:
            projectIdOrKey (string): projectIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_create_issue_meta_issue_type_id(self, projectIdOrKey, issueTypeId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves metadata for specific issue types within a project in Jira using the "GET" method, returning details such as available fields and their schemas based on the project and issue type identifiers.

        Args:
            projectIdOrKey (string): projectIdOrKey
            issueTypeId (string): issueTypeId
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if issueTypeId is None:
            raise ValueError("Missing required parameter 'issueTypeId'")
        url = f"{self.base_url}/rest/api/3/issue/createmeta/{projectIdOrKey}/issuetypes/{issueTypeId}"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_limit_report(self, isReturningKeys=None) -> dict[str, Any]:
        """
        Retrieves a report of issues approaching their worklog limit thresholds using the specified parameters.

        Args:
            isReturningKeys (boolean): Return issue keys instead of issue ids in the response. Usage: Add `?isReturningKeys=true` to the end of the path to request issue keys.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        url = f"{self.base_url}/rest/api/3/issue/limit/report"
        query_params = {k: v for k, v in [('isReturningKeys', isReturningKeys)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_picker_resource(self, query=None, currentJQL=None, currentIssueKey=None, currentProjectId=None, showSubTasks=None, showSubTaskParent=None) -> dict[str, Any]:
        """
        Provides auto-completion suggestions for Jira issues based on search queries and JQL filters, returning matching issues from user history and current searches.

        Args:
            query (string): A string to match against text fields in the issue such as title, description, or comments. Example: 'query'.
            currentJQL (string): A JQL query defining a list of issues to search for the query term. Note that `username` and `userkey` cannot be used as search terms for this parameter, due to privacy reasons. Use `accountId` instead.
            currentIssueKey (string): The key of an issue to exclude from search results. For example, the issue the user is viewing when they perform this query.
            currentProjectId (string): The ID of a project that suggested issues must belong to.
            showSubTasks (boolean): Indicate whether to include subtasks in the suggestions list.
            showSubTaskParent (boolean): When `currentIssueKey` is a subtask, whether to include the parent issue in the suggestions if it matches the query.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        url = f"{self.base_url}/rest/api/3/issue/picker"
        query_params = {k: v for k, v in [('query', query), ('currentJQL', currentJQL), ('currentIssueKey', currentIssueKey), ('currentProjectId', currentProjectId), ('showSubTasks', showSubTasks), ('showSubTaskParent', showSubTaskParent)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_set_issues_properties_list(self, entitiesIds=None, properties=None) -> Any:
        """
        Sets or updates multiple issue properties for specified issues using JIRA's REST API, supporting bulk operations on custom data storage.

        Args:
            entitiesIds (array): A list of entity property IDs.
            properties (object): A list of entity property keys and values.

        Returns:
            Any: API response data.

        Tags:
            Issue properties
        """
        request_body = {
            'entitiesIds': entitiesIds,
            'properties': properties,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/properties"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_set_issue_properties_by_issue(self, issues=None) -> Any:
        """
        Sets or updates custom properties on multiple Jira issues in a single request and returns the task status for asynchronous processing.

        Args:
            issues (array): A list of issue IDs and their respective properties.
                Example:
                ```json
                {
                  "issues": [
                    {
                      "issueID": 1000,
                      "properties": {
                        "myProperty": {
                          "owner": "admin",
                          "weight": 100
                        }
                      }
                    },
                    {
                      "issueID": 1001,
                      "properties": {
                        "myOtherProperty": {
                          "cost": 150,
                          "transportation": "car"
                        }
                      }
                    }
                  ]
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Issue properties
        """
        request_body = {
            'issues': issues,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/properties/multi"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_delete_issue_property(self, propertyKey, currentValue=None, entityIds=None) -> Any:
        """
        Deletes a specified issue property from multiple Jira issues using filter criteria including entity IDs or property values.

        Args:
            propertyKey (string): propertyKey
            currentValue (string): The value of properties to perform the bulk operation on.
            entityIds (array): List of issues to perform the bulk delete operation on.
                Example:
                ```json
                {
                  "currentValue": "deprecated value",
                  "entityIds": [
                    10100,
                    100010
                  ]
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Issue properties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        request_body = {
            'currentValue': currentValue,
            'entityIds': entityIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_set_issue_property(self, propertyKey, expression=None, filter=None, value=None) -> Any:
        """
        Updates or sets a custom property value for a Jira issue identified by the property key, returning a status reference for asynchronous processing.

        Args:
            propertyKey (string): propertyKey
            expression (string): EXPERIMENTAL. The Jira expression to calculate the value of the property. The value of the expression must be an object that can be converted to JSON, such as a number, boolean, string, list, or map. The context variables available to the expression are `issue` and `user`. Issues for which the expression returns a value whose JSON representation is longer than 32768 characters are ignored.
            filter (string): The bulk operation filter.
            value (string): The value of the property. The value must be a [valid](https://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.
                Example:
                ```json
                {
                  "filter": {
                    "currentValue": {
                      "owner": "admin",
                      "weight": 50
                    },
                    "entityIds": [
                      10100,
                      100010
                    ],
                    "hasProperty": true
                  },
                  "value": {
                    "owner": "admin",
                    "weight": 100
                  }
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Issue properties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        request_body = {
            'expression': expression,
            'filter': filter,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/properties/{propertyKey}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def unarchive_issues(self, issueIdsOrKeys=None) -> dict[str, Any]:
        """
        Unarchives up to 1000 Jira issues in a single request using their IDs or keys, returning the count of unarchived issues and any errors encountered.

        Args:
            issueIdsOrKeys (array): issueIdsOrKeys
                Example:
                ```json
                {
                  "issueIdsOrKeys": [
                    "PR-1",
                    "1001",
                    "PROJECT-2"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if there is at least one valid issue to unarchive in the request. It will return the count of unarchived issues, which also includes the count of the subtasks unarchived, and it will show the detailed errors for those issues which are not unarchived.

        Tags:
            Issues
        """
        request_body = {
            'issueIdsOrKeys': issueIdsOrKeys,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/unarchive"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_is_watching_issue_bulk(self, issueIds) -> dict[str, Any]:
        """
        Determines whether the current user is watching specific issues using the Jira Cloud API, returning a status of whether the user is watching each provided issue.

        Args:
            issueIds (array): The list of issue IDs.
                Example:
                ```json
                {
                  "issueIds": [
                    "10001",
                    "10002",
                    "10005"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful

        Tags:
            Issue watchers
        """
        request_body = {
            'issueIds': issueIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/watching"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue(self, issueIdOrKey, deleteSubtasks=None) -> Any:
        """
        Deletes a Jira issue identified by its ID or key, optionally deleting associated subtasks if the `deleteSubtasks` query parameter is set to `true`.

        Args:
            issueIdOrKey (string): issueIdOrKey
            deleteSubtasks (string): Whether the issue's subtasks are deleted when the issue is deleted.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}"
        query_params = {k: v for k, v in [('deleteSubtasks', deleteSubtasks)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue(self, issueIdOrKey, fields=None, fieldsByKeys=None, expand=None, properties=None, updateHistory=None, failFast=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a Jira issue using its ID or key, allowing optional parameters to specify fields, expansions, and additional data.

        Args:
            issueIdOrKey (string): issueIdOrKey
            fields (array): A list of fields to return for the issue. This parameter accepts a comma-separated list. Use it to retrieve a subset of fields. Allowed values: * `*all` Returns all fields. * `*navigable` Returns navigable fields. * Any issue field, prefixed with a minus to exclude. Examples: * `summary,comment` Returns only the summary and comments fields. * `-description` Returns all (default) fields except description. * `*navigable,-comment` Returns all navigable fields except comment. This parameter may be specified multiple times. For example, `fields=field1,field2& fields=field3`. Note: All fields are returned by default. This differs from [Search for issues using JQL (GET)](#api-rest-api-3-search-get) and [Search for issues using JQL (POST)](#api-rest-api-3-search-post) where the default is all navigable fields.
            fieldsByKeys (boolean): Whether fields in `fields` are referenced by keys rather than IDs. This parameter is useful where fields have been added by a connect app and a field's key may differ from its ID.
            expand (string): Use [expand](#expansion) to include additional information about the issues in the response. This parameter accepts a comma-separated list. Expand options include: * `renderedFields` Returns field values rendered in HTML format. * `names` Returns the display name of each field. * `schema` Returns the schema describing a field type. * `transitions` Returns all possible transitions for the issue. * `editmeta` Returns information about how each field can be edited. * `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent. * `versionedRepresentations` Returns a JSON array for each version of a field's value, with the highest number representing the most recent version. Note: When included in the request, the `fields` parameter is ignored.
            properties (array): A list of issue properties to return for the issue. This parameter accepts a comma-separated list. Allowed values: * `*all` Returns all issue properties. * Any issue property key, prefixed with a minus to exclude. Examples: * `*all` Returns all properties. * `*all,-prop1` Returns all properties except `prop1`. * `prop1,prop2` Returns `prop1` and `prop2` properties. This parameter may be specified multiple times. For example, `properties=prop1,prop2& properties=prop3`.
            updateHistory (boolean): Whether the project in which the issue is created is added to the user's **Recently viewed** project list, as shown under **Projects** in Jira. This also populates the [JQL issues search](#api-rest-api-3-search-get) `lastViewed` field.
            failFast (boolean): Whether to fail the request quickly in case of an error while loading fields for an issue. For `failFast=true`, if one field fails, the entire operation fails. For `failFast=false`, the operation will continue even if a field fails. It will return a valid response, but without values for the failed field(s).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}"
        query_params = {k: v for k, v in [('fields', fields), ('fieldsByKeys', fieldsByKeys), ('expand', expand), ('properties', properties), ('updateHistory', updateHistory), ('failFast', failFast)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def edit_issue(self, issueIdOrKey, notifyUsers=None, overrideScreenSecurity=None, overrideEditableFlag=None, returnIssue=None, expand=None, fields=None, historyMetadata=None, properties=None, transition=None, update=None) -> Any:
        """
        Updates an issue in Jira using the specified issue ID or key, allowing modification of issue fields, with optional parameters to control notification, screen security, editable flags, and response details.

        Args:
            issueIdOrKey (string): issueIdOrKey
            notifyUsers (boolean): Whether a notification email about the issue update is sent to all watchers. To disable the notification, administer Jira or administer project permissions are required. If the user doesn't have the necessary permission the request is ignored.
            overrideScreenSecurity (boolean): Whether screen security is overridden to enable hidden fields to be edited. Available to Connect app users with *Administer Jira* [global permission]( and Forge apps acting on behalf of users with *Administer Jira* [global permission](
            overrideEditableFlag (boolean): Whether screen security is overridden to enable uneditable fields to be edited. Available to Connect app users with *Administer Jira* [global permission]( and Forge apps acting on behalf of users with *Administer Jira* [global permission](
            returnIssue (boolean): Whether the response should contain the issue with fields edited in this request. The returned issue will have the same format as in the [Get issue API](#api-rest-api-3-issue-issueidorkey-get).
            expand (string): The Get issue API expand parameter to use in the response if the `returnIssue` parameter is `true`.
            fields (object): List of issue screen fields to update, specifying the sub-field to update and its value for each field. This field provides a straightforward option when setting a sub-field. When multiple sub-fields or other operations are required, use `update`. Fields included in here cannot be included in `update`.
            historyMetadata (string): Additional issue history details.
            properties (array): Details of issue properties to be add or update.
            transition (string): Details of a transition. Required when performing a transition, optional when creating or editing an issue.
            update (object): A Map containing the field field name and a list of operations to perform on the issue screen field. Note that fields included in here cannot be included in `fields`.
                Example:
                ```json
                {
                  "fields": {
                    "customfield_10000": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "Investigation underway",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "customfield_10010": 1,
                    "summary": "Completed orders still displaying in pending"
                  },
                  "historyMetadata": {
                    "activityDescription": "Complete order processing",
                    "actor": {
                      "avatarUrl": "http://mysystem/avatar/tony.jpg",
                      "displayName": "Tony",
                      "id": "tony",
                      "type": "mysystem-user",
                      "url": "http://mysystem/users/tony"
                    },
                    "cause": {
                      "id": "myevent",
                      "type": "mysystem-event"
                    },
                    "description": "From the order testing process",
                    "extraData": {
                      "Iteration": "10a",
                      "Step": "4"
                    },
                    "generator": {
                      "id": "mysystem-1",
                      "type": "mysystem-application"
                    },
                    "type": "myplugin:type"
                  },
                  "properties": [
                    {
                      "key": "key1",
                      "value": "Order number 10784"
                    },
                    {
                      "key": "key2",
                      "value": "Order number 10923"
                    }
                  ],
                  "update": {
                    "components": [
                      {
                        "set": ""
                      }
                    ],
                    "labels": [
                      {
                        "add": "triaged"
                      },
                      {
                        "remove": "blocker"
                      }
                    ],
                    "summary": [
                      {
                        "set": "Bug in business logic"
                      }
                    ],
                    "timetracking": [
                      {
                        "edit": {
                          "originalEstimate": "1w 1d",
                          "remainingEstimate": "4d"
                        }
                      }
                    ]
                  }
                }
                ```

        Returns:
            Any: Returned if the request is successful and the `returnIssue` parameter is `true`

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'fields': fields,
            'historyMetadata': historyMetadata,
            'properties': properties,
            'transition': transition,
            'update': update,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}"
        query_params = {k: v for k, v in [('notifyUsers', notifyUsers), ('overrideScreenSecurity', overrideScreenSecurity), ('overrideEditableFlag', overrideEditableFlag), ('returnIssue', returnIssue), ('expand', expand)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_issue(self, issueIdOrKey, accountId=None, accountType=None, active=None, applicationRoles=None, avatarUrls=None, displayName=None, emailAddress=None, expand=None, groups=None, key=None, locale=None, name=None, self_arg_body=None, timeZone=None) -> Any:
        """
        Assigns or unassigns a Jira issue to a specific user, sets it to unassigned, or assigns it to the project's default assignee using the provided account ID or null value.

        Args:
            issueIdOrKey (string): issueIdOrKey
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Required in requests.
            accountType (string): The user account type. Can take the following values:

         *  `atlassian` regular Atlassian user account
         *  `app` system account used for Connect applications and OAuth to represent external systems
         *  `customer` Jira Service Desk account representing an external service desk
            active (boolean): Whether the user is active.
            applicationRoles (string): The application roles the user is assigned to.
            avatarUrls (string): The avatars of the user.
            displayName (string): The display name of the user. Depending on the user’s privacy setting, this may return an alternative value.
            emailAddress (string): The email address of the user. Depending on the user’s privacy setting, this may be returned as null.
            expand (string): Expand options that include additional user details in the response.
            groups (string): The groups that the user belongs to.
            key (string): This property is no longer available and will be removed from the documentation soon. See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            locale (string): The locale of the user. Depending on the user’s privacy setting, this may be returned as null.
            name (string): This property is no longer available and will be removed from the documentation soon. See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            self_arg_body (string): The URL of the user.
            timeZone (string): The time zone specified in the user's profile. If the user's time zone is not visible to the current user (due to user's profile setting), or if a time zone has not been set, the instance's default time zone will be returned.
                Example:
                ```json
                {
                  "accountId": "5b10ac8d82e05b22cc7d4ef5"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'accountId': accountId,
            'accountType': accountType,
            'active': active,
            'applicationRoles': applicationRoles,
            'avatarUrls': avatarUrls,
            'displayName': displayName,
            'emailAddress': emailAddress,
            'expand': expand,
            'groups': groups,
            'key': key,
            'locale': locale,
            'name': name,
            'self': self_arg_body,
            'timeZone': timeZone,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/assignee"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()


    def get_change_logs(self, issueIdOrKey, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves paginated changelog history for a specified Jira issue, including parameters for result pagination.

        Args:
            issueIdOrKey (string): issueIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/changelog"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_change_logs_by_ids(self, issueIdOrKey, changelogIds) -> dict[str, Any]:
        """
        Retrieves the full changelog history for a specified Jira issue using its ID or key, allowing for pagination and retrieval of all changes.

        Args:
            issueIdOrKey (string): issueIdOrKey
            changelogIds (array): The list of changelog IDs.
                Example:
                ```json
                {
                  "changelogIds": [
                    10001,
                    10002
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'changelogIds': changelogIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/changelog/list"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_comments(self, issueIdOrKey, startAt=None, maxResults=None, orderBy=None, expand=None) -> dict[str, Any]:
        """
        Retrieves all comments for a specified Jira issue using pagination parameters.

        Args:
            issueIdOrKey (string): issueIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field. Accepts *created* to sort comments by their created date.
            expand (string): Use [expand](#expansion) to include additional information about comments in the response. This parameter accepts `renderedBody`, which returns the comment body rendered in HTML.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comments ,important
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/comment"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_comment(self, issueIdOrKey, expand=None, author=None, body=None, created=None, id=None, jsdAuthorCanSeeRequest=None, jsdPublic=None, properties=None, renderedBody=None, self_arg_body=None, updateAuthor=None, updated=None, visibility=None) -> dict[str, Any]:
        """
        Adds a comment to a Jira issue with support for visibility settings and returns the created comment.

        Args:
            issueIdOrKey (string): issueIdOrKey
            expand (string): Use [expand](#expansion) to include additional information about comments in the response. This parameter accepts `renderedBody`, which returns the comment body rendered in HTML.
            author (string): The ID of the user who created the comment.
            body (string): The comment text in [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).
            created (string): The date and time at which the comment was created.
            id (string): The ID of the comment.
            jsdAuthorCanSeeRequest (boolean): Whether the comment was added from an email sent by a person who is not part of the issue. See [Allow external emails to be added as comments on issues](https://support.atlassian.com/jira-service-management-cloud/docs/allow-external-emails-to-be-added-as-comments-on-issues/)for information on setting up this feature.
            jsdPublic (boolean): Whether the comment is visible in Jira Service Desk. Defaults to true when comments are created in the Jira Cloud Platform. This includes when the site doesn't use Jira Service Desk or the project isn't a Jira Service Desk project and, therefore, there is no Jira Service Desk for the issue to be visible on. To create a comment with its visibility in Jira Service Desk set to false, use the Jira Service Desk REST API [Create request comment](https://developer.atlassian.com/cloud/jira/service-desk/rest/#api-rest-servicedeskapi-request-issueIdOrKey-comment-post) operation.
            properties (array): A list of comment properties. Optional on create and update.
            renderedBody (string): The rendered version of the comment.
            self_arg_body (string): The URL of the comment.
            updateAuthor (string): The ID of the user who updated the comment last.
            updated (string): The date and time at which the comment was updated last.
            visibility (string): The group or role to which this comment is visible. Optional on create and update.
                Example:
                ```json
                {
                  "body": {
                    "content": [
                      {
                        "content": [
                          {
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget venenatis elit. Duis eu justo eget augue iaculis fermentum. Sed semper quam laoreet nisi egestas at posuere augue semper.",
                            "type": "text"
                          }
                        ],
                        "type": "paragraph"
                      }
                    ],
                    "type": "doc",
                    "version": 1
                  },
                  "visibility": {
                    "identifier": "Administrators",
                    "type": "role",
                    "value": "Administrators"
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comments
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'author': author,
            'body': body,
            'created': created,
            'id': id,
            'jsdAuthorCanSeeRequest': jsdAuthorCanSeeRequest,
            'jsdPublic': jsdPublic,
            'properties': properties,
            'renderedBody': renderedBody,
            'self': self_arg_body,
            'updateAuthor': updateAuthor,
            'updated': updated,
            'visibility': visibility,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/comment"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_comment(self, issueIdOrKey, id) -> Any:
        """
        Deletes a specific comment from a Jira issue using the comment ID and issue identifier.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue comments
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/comment/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_comment(self, issueIdOrKey, id, expand=None) -> dict[str, Any]:
        """
        Retrieves a specific comment from a Jira issue using its ID and returns the comment details.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about comments in the response. This parameter accepts `renderedBody`, which returns the comment body rendered in HTML.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comments
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/comment/{id}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_comment(self, issueIdOrKey, id, notifyUsers=None, overrideEditableFlag=None, expand=None, author=None, body=None, created=None, id_body=None, jsdAuthorCanSeeRequest=None, jsdPublic=None, properties=None, renderedBody=None, self_arg_body=None, updateAuthor=None, updated=None, visibility=None) -> dict[str, Any]:
        """
        Updates an existing comment on a Jira issue and returns the modified comment details.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id
            notifyUsers (boolean): Whether users are notified when a comment is updated.
            overrideEditableFlag (boolean): Whether screen security is overridden to enable uneditable fields to be edited. Available to Connect app users with the *Administer Jira* [global permission]( and Forge apps acting on behalf of users with *Administer Jira* [global permission](
            expand (string): Use [expand](#expansion) to include additional information about comments in the response. This parameter accepts `renderedBody`, which returns the comment body rendered in HTML.
            author (string): The ID of the user who created the comment.
            body (string): The comment text in [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).
            created (string): The date and time at which the comment was created.
            id_body (string): The ID of the comment.
            jsdAuthorCanSeeRequest (boolean): Whether the comment was added from an email sent by a person who is not part of the issue. See [Allow external emails to be added as comments on issues](https://support.atlassian.com/jira-service-management-cloud/docs/allow-external-emails-to-be-added-as-comments-on-issues/)for information on setting up this feature.
            jsdPublic (boolean): Whether the comment is visible in Jira Service Desk. Defaults to true when comments are created in the Jira Cloud Platform. This includes when the site doesn't use Jira Service Desk or the project isn't a Jira Service Desk project and, therefore, there is no Jira Service Desk for the issue to be visible on. To create a comment with its visibility in Jira Service Desk set to false, use the Jira Service Desk REST API [Create request comment](https://developer.atlassian.com/cloud/jira/service-desk/rest/#api-rest-servicedeskapi-request-issueIdOrKey-comment-post) operation.
            properties (array): A list of comment properties. Optional on create and update.
            renderedBody (string): The rendered version of the comment.
            self_arg_body (string): The URL of the comment.
            updateAuthor (string): The ID of the user who updated the comment last.
            updated (string): The date and time at which the comment was updated last.
            visibility (string): The group or role to which this comment is visible. Optional on create and update.
                Example:
                ```json
                {
                  "body": {
                    "content": [
                      {
                        "content": [
                          {
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget venenatis elit. Duis eu justo eget augue iaculis fermentum. Sed semper quam laoreet nisi egestas at posuere augue semper.",
                            "type": "text"
                          }
                        ],
                        "type": "paragraph"
                      }
                    ],
                    "type": "doc",
                    "version": 1
                  },
                  "visibility": {
                    "identifier": "Administrators",
                    "type": "role",
                    "value": "Administrators"
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue comments
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'author': author,
            'body': body,
            'created': created,
            'id': id_body,
            'jsdAuthorCanSeeRequest': jsdAuthorCanSeeRequest,
            'jsdPublic': jsdPublic,
            'properties': properties,
            'renderedBody': renderedBody,
            'self': self_arg_body,
            'updateAuthor': updateAuthor,
            'updated': updated,
            'visibility': visibility,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/comment/{id}"
        query_params = {k: v for k, v in [('notifyUsers', notifyUsers), ('overrideEditableFlag', overrideEditableFlag), ('expand', expand)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_edit_issue_meta(self, issueIdOrKey, overrideScreenSecurity=None, overrideEditableFlag=None) -> dict[str, Any]:
        """
        Retrieves editable field metadata and supported operations for a specific Jira issue to guide modifications via the API.

        Args:
            issueIdOrKey (string): issueIdOrKey
            overrideScreenSecurity (boolean): Whether hidden fields are returned. Available to Connect app users with *Administer Jira* [global permission]( and Forge apps acting on behalf of users with *Administer Jira* [global permission](
            overrideEditableFlag (boolean): Whether non-editable fields are returned. Available to Connect app users with *Administer Jira* [global permission]( and Forge apps acting on behalf of users with *Administer Jira* [global permission](

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/editmeta"
        query_params = {k: v for k, v in [('overrideScreenSecurity', overrideScreenSecurity), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def notify(self, issueIdOrKey, htmlBody=None, restrict=None, subject=None, textBody=None, to=None) -> Any:
        """
        Sends notifications related to a specific Jira issue, identified by its ID or key, allowing customization of the notification content and recipients.

        Args:
            issueIdOrKey (string): issueIdOrKey
            htmlBody (string): The HTML body of the email notification for the issue.
            restrict (string): Restricts the notifications to users with the specified permissions.
            subject (string): The subject of the email notification for the issue. If this is not specified, then the subject is set to the issue key and summary.
            textBody (string): The plain text body of the email notification for the issue.
            to (string): The recipients of the email notification for the issue.
                Example:
                ```json
                {
                  "htmlBody": "The <strong>latest</strong> test results for this ticket are now available.",
                  "restrict": {
                    "groupIds": [],
                    "groups": [
                      {
                        "name": "notification-group"
                      }
                    ],
                    "permissions": [
                      {
                        "key": "BROWSE"
                      }
                    ]
                  },
                  "subject": "Latest test results",
                  "textBody": "The latest test results for this ticket are now available.",
                  "to": {
                    "assignee": false,
                    "groupIds": [],
                    "groups": [
                      {
                        "name": "notification-group"
                      }
                    ],
                    "reporter": false,
                    "users": [
                      {
                        "accountId": "5b10a2844c20165700ede21g",
                        "active": false
                      }
                    ],
                    "voters": true,
                    "watchers": true
                  }
                }
                ```

        Returns:
            Any: Returned if the email is queued for sending.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'htmlBody': htmlBody,
            'restrict': restrict,
            'subject': subject,
            'textBody': textBody,
            'to': to,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/notify"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_property_keys(self, issueIdOrKey) -> dict[str, Any]:
        """
        Retrieves the URLs and keys of all properties associated with a specified Jira issue using the issue ID or key.

        Args:
            issueIdOrKey (string): issueIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_property(self, issueIdOrKey, propertyKey) -> Any:
        """
        Deletes a specific property from an issue in Jira, identified by its issue ID or key and the property key, using the Jira API.

        Args:
            issueIdOrKey (string): issueIdOrKey
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_property(self, issueIdOrKey, propertyKey) -> dict[str, Any]:
        """
        Retrieves the value of a specific property associated with a Jira issue using the provided issue ID or key and property key.

        Args:
            issueIdOrKey (string): issueIdOrKey
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_remote_issue_link_by_global_id(self, issueIdOrKey, globalId) -> Any:
        """
        Deletes a remote issue link from a Jira issue using either the link's internal ID or its global ID.

        Args:
            issueIdOrKey (string): issueIdOrKey
            globalId (string): The global ID of a remote issue link. Example: 'system=http://www.mycompany.com/support&id=1'.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink"
        query_params = {k: v for k, v in [('globalId', globalId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_remote_issue_links(self, issueIdOrKey, globalId=None) -> dict[str, Any]:
        """
        Retrieves a list of remote links associated with a specified Jira issue, identified by its ID or key, using the GET method at the "/rest/api/3/issue/{issueIdOrKey}/remotelink" path, allowing for optional filtering by global ID.

        Args:
            issueIdOrKey (string): issueIdOrKey
            globalId (string): The global ID of the remote issue link.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink"
        query_params = {k: v for k, v in [('globalId', globalId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_or_update_remote_issue_link(self, issueIdOrKey, object, application=None, globalId=None, relationship=None) -> dict[str, Any]:
        """
        Creates a remote link to an external object for a specified Jira issue, allowing users to associate external resources with issue tracking in Jira.

        Args:
            issueIdOrKey (string): issueIdOrKey
            object (string): Details of the item linked to.
            application (string): Details of the remote application the linked item is in. For example, trello.
            globalId (string): An identifier for the remote item in the remote system. For example, the global ID for a remote item in Confluence would consist of the app ID and page ID, like this: `appId=456&pageId=123`.

        Setting this field enables the remote issue link details to be updated or deleted using remote system and item details as the record identifier, rather than using the record's Jira ID.

        The maximum length is 255 characters.
            relationship (string): Description of the relationship between the issue and the linked item. If not set, the relationship description "links to" is used in Jira.
                Example:
                ```json
                {
                  "application": {
                    "name": "My Acme Tracker",
                    "type": "com.acme.tracker"
                  },
                  "globalId": "system=http://www.mycompany.com/support&id=1",
                  "object": {
                    "icon": {
                      "title": "Support Ticket",
                      "url16x16": "http://www.mycompany.com/support/ticket.png"
                    },
                    "status": {
                      "icon": {
                        "link": "http://www.mycompany.com/support?id=1&details=closed",
                        "title": "Case Closed",
                        "url16x16": "http://www.mycompany.com/support/resolved.png"
                      },
                      "resolved": true
                    },
                    "summary": "Customer support issue",
                    "title": "TSTSUP-111",
                    "url": "http://www.mycompany.com/support?id=1"
                  },
                  "relationship": "causes"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the remote issue link is updated.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'application': application,
            'globalId': globalId,
            'object': object,
            'relationship': relationship,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_remote_issue_link_by_id(self, issueIdOrKey, linkId) -> Any:
        """
        Deletes a remote issue link from a specified Jira issue using the link's internal ID.

        Args:
            issueIdOrKey (string): issueIdOrKey
            linkId (string): linkId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if linkId is None:
            raise ValueError("Missing required parameter 'linkId'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_remote_issue_link_by_id(self, issueIdOrKey, linkId) -> dict[str, Any]:
        """
        Retrieves a specific remote link by its ID associated with a Jira issue, identified by the issue ID or key.

        Args:
            issueIdOrKey (string): issueIdOrKey
            linkId (string): linkId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if linkId is None:
            raise ValueError("Missing required parameter 'linkId'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_remote_issue_link(self, issueIdOrKey, linkId, object, application=None, globalId=None, relationship=None) -> Any:
        """
        Updates a specific remote issue link by ID using a PUT request for the specified Jira issue.

        Args:
            issueIdOrKey (string): issueIdOrKey
            linkId (string): linkId
            object (string): Details of the item linked to.
            application (string): Details of the remote application the linked item is in. For example, trello.
            globalId (string): An identifier for the remote item in the remote system. For example, the global ID for a remote item in Confluence would consist of the app ID and page ID, like this: `appId=456&pageId=123`.

        Setting this field enables the remote issue link details to be updated or deleted using remote system and item details as the record identifier, rather than using the record's Jira ID.

        The maximum length is 255 characters.
            relationship (string): Description of the relationship between the issue and the linked item. If not set, the relationship description "links to" is used in Jira.
                Example:
                ```json
                {
                  "application": {
                    "name": "My Acme Tracker",
                    "type": "com.acme.tracker"
                  },
                  "globalId": "system=http://www.mycompany.com/support&id=1",
                  "object": {
                    "icon": {
                      "title": "Support Ticket",
                      "url16x16": "http://www.mycompany.com/support/ticket.png"
                    },
                    "status": {
                      "icon": {
                        "link": "http://www.mycompany.com/support?id=1&details=closed",
                        "title": "Case Closed",
                        "url16x16": "http://www.mycompany.com/support/resolved.png"
                      },
                      "resolved": true
                    },
                    "summary": "Customer support issue",
                    "title": "TSTSUP-111",
                    "url": "http://www.mycompany.com/support?id=1"
                  },
                  "relationship": "causes"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue remote links
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if linkId is None:
            raise ValueError("Missing required parameter 'linkId'")
        request_body = {
            'application': application,
            'globalId': globalId,
            'object': object,
            'relationship': relationship,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_transitions(self, issueIdOrKey, expand=None, transitionId=None, skipRemoteOnlyCondition=None, includeUnavailableTransitions=None, sortByOpsBarAndStatus=None) -> dict[str, Any]:
        """
        Retrieves all available transitions for a Jira issue in its current status, including optional details like required fields and validation rules.

        Args:
            issueIdOrKey (string): issueIdOrKey
            expand (string): Use [expand](#expansion) to include additional information about transitions in the response. This parameter accepts `transitions.fields`, which returns information about the fields in the transition screen for each transition. Fields hidden from the screen are not returned. Use this information to populate the `fields` and `update` fields in [Transition issue](#api-rest-api-3-issue-issueIdOrKey-transitions-post).
            transitionId (string): The ID of the transition.
            skipRemoteOnlyCondition (boolean): Whether transitions with the condition *Hide From User Condition* are included in the response.
            includeUnavailableTransitions (boolean): Whether details of transitions that fail a condition are included in the response
            sortByOpsBarAndStatus (boolean): Whether the transitions are sorted by ops-bar sequence value first then category order (Todo, In Progress, Done) or only by ops-bar sequence value.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/transitions"
        query_params = {k: v for k, v in [('expand', expand), ('transitionId', transitionId), ('skipRemoteOnlyCondition', skipRemoteOnlyCondition), ('includeUnavailableTransitions', includeUnavailableTransitions), ('sortByOpsBarAndStatus', sortByOpsBarAndStatus)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def do_transition(self, issueIdOrKey, fields=None, historyMetadata=None, properties=None, transition=None, update=None) -> Any:
        """
        Transitions a Jira issue to a new workflow status using the specified transition ID.

        Args:
            issueIdOrKey (string): issueIdOrKey
            fields (object): List of issue screen fields to update, specifying the sub-field to update and its value for each field. This field provides a straightforward option when setting a sub-field. When multiple sub-fields or other operations are required, use `update`. Fields included in here cannot be included in `update`.
            historyMetadata (string): Additional issue history details.
            properties (array): Details of issue properties to be add or update.
            transition (string): Details of a transition. Required when performing a transition, optional when creating or editing an issue.
            update (object): A Map containing the field field name and a list of operations to perform on the issue screen field. Note that fields included in here cannot be included in `fields`.
                Example:
                ```json
                {
                  "fields": {
                    "assignee": {
                      "name": "bob"
                    },
                    "resolution": {
                      "name": "Fixed"
                    }
                  },
                  "historyMetadata": {
                    "activityDescription": "Complete order processing",
                    "actor": {
                      "avatarUrl": "http://mysystem/avatar/tony.jpg",
                      "displayName": "Tony",
                      "id": "tony",
                      "type": "mysystem-user",
                      "url": "http://mysystem/users/tony"
                    },
                    "cause": {
                      "id": "myevent",
                      "type": "mysystem-event"
                    },
                    "description": "From the order testing process",
                    "extraData": {
                      "Iteration": "10a",
                      "Step": "4"
                    },
                    "generator": {
                      "id": "mysystem-1",
                      "type": "mysystem-application"
                    },
                    "type": "myplugin:type"
                  },
                  "transition": {
                    "id": "5"
                  },
                  "update": {
                    "comment": [
                      {
                        "add": {
                          "body": {
                            "content": [
                              {
                                "content": [
                                  {
                                    "text": "Bug has been fixed",
                                    "type": "text"
                                  }
                                ],
                                "type": "paragraph"
                              }
                            ],
                            "type": "doc",
                            "version": 1
                          }
                        }
                      }
                    ]
                  }
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issues
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'fields': fields,
            'historyMetadata': historyMetadata,
            'properties': properties,
            'transition': transition,
            'update': update,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/transitions"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_vote(self, issueIdOrKey) -> Any:
        """
        Deletes a user's vote from a specified Jira issue, identified by its ID or key, using the Jira REST API.

        Args:
            issueIdOrKey (string): issueIdOrKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue votes
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/votes"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_votes(self, issueIdOrKey) -> dict[str, Any]:
        """
        Retrieves details about the votes on a specific Jira issue, identified by its issue ID or key.

        Args:
            issueIdOrKey (string): issueIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue votes
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/votes"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_vote(self, issueIdOrKey) -> Any:
        """
        Casts a vote on a Jira issue and returns no content on success.

        Args:
            issueIdOrKey (string): issueIdOrKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue votes
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/votes"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_watcher(self, issueIdOrKey, username=None, accountId=None) -> Any:
        """
        Removes a specified user as a watcher from a Jira issue via their username or account ID and returns a success status upon completion.

        Args:
            issueIdOrKey (string): issueIdOrKey
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Required. Example: '5b10ac8d82e05b22cc7d4ef5'.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue watchers
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/watchers"
        query_params = {k: v for k, v in [('username', username), ('accountId', accountId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_watchers(self, issueIdOrKey) -> dict[str, Any]:
        """
        Retrieves the list of watchers for a specific Jira issue using the provided issue ID or key.

        Args:
            issueIdOrKey (string): issueIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful

        Tags:
            Issue watchers
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/watchers"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def bulk_delete_worklogs(self, issueIdOrKey, ids, adjustEstimate=None, overrideEditableFlag=None) -> Any:
        """
        Deletes a worklog from a specific issue in Jira using the provided issue ID or key, allowing for optional adjustments to the estimate and overriding of editable flags.

        Args:
            issueIdOrKey (string): issueIdOrKey
            ids (array): A list of worklog IDs.
                Example:
                ```json
                {
                  "ids": [
                    1,
                    2,
                    5,
                    10
                  ]
                }
                ```
            adjustEstimate (string): Defines how to update the issue's time estimate, the options are: * `leave` Leaves the estimate unchanged. * `auto` Reduces the estimate by the aggregate value of `timeSpent` across all worklogs being deleted.
            overrideEditableFlag (boolean): Whether the work log entries should be removed to the issue even if the issue is not editable, because jira.issue.editable set to false or missing. For example, the issue is closed. Connect and Forge app users with admin permission can use this flag.

        Returns:
            Any: Returned if the bulk deletion request was partially successful, with a message indicating partial success.

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'ids': ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog"
        query_params = {k: v for k, v in [('adjustEstimate', adjustEstimate), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_worklog(self, issueIdOrKey, startAt=None, maxResults=None, startedAfter=None, startedBefore=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of worklogs for a specific Jira issue using the "GET" method, allowing filtering by start date and other parameters.

        Args:
            issueIdOrKey (string): issueIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            startedAfter (integer): The worklog start date and time, as a UNIX timestamp in milliseconds, after which worklogs are returned.
            startedBefore (integer): The worklog start date and time, as a UNIX timestamp in milliseconds, before which worklogs are returned.
            expand (string): Use [expand](#expansion) to include additional information about worklogs in the response. This parameter accepts`properties`, which returns worklog properties.

        Returns:
            dict[str, Any]: Returned if the request is successful

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('startedAfter', startedAfter), ('startedBefore', startedBefore), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_worklog(self, issueIdOrKey, notifyUsers=None, adjustEstimate=None, newEstimate=None, reduceBy=None, expand=None, overrideEditableFlag=None, author=None, comment=None, created=None, id=None, issueId=None, properties=None, self_arg_body=None, started=None, timeSpent=None, timeSpentSeconds=None, updateAuthor=None, updated=None, visibility=None) -> dict[str, Any]:
        """
        Adds a worklog entry to a Jira issue for time tracking and returns the created worklog details.

        Args:
            issueIdOrKey (string): issueIdOrKey
            notifyUsers (boolean): Whether users watching the issue are notified by email.
            adjustEstimate (string): Defines how to update the issue's time estimate, the options are: * `new` Sets the estimate to a specific value, defined in `newEstimate`. * `leave` Leaves the estimate unchanged. * `manual` Reduces the estimate by amount specified in `reduceBy`. * `auto` Reduces the estimate by the value of `timeSpent` in the worklog.
            newEstimate (string): The value to set as the issue's remaining time estimate, as days (\#d), hours (\#h), or minutes (\#m or \#). For example, *2d*. Required when `adjustEstimate` is `new`.
            reduceBy (string): The amount to reduce the issue's remaining estimate by, as days (\#d), hours (\#h), or minutes (\#m). For example, *2d*. Required when `adjustEstimate` is `manual`.
            expand (string): Use [expand](#expansion) to include additional information about work logs in the response. This parameter accepts `properties`, which returns worklog properties.
            overrideEditableFlag (boolean): Whether the worklog entry should be added to the issue even if the issue is not editable, because jira.issue.editable set to false or missing. For example, the issue is closed. Connect and Forge app users with *Administer Jira* [global permission]( can use this flag.
            author (string): Details of the user who created the worklog.
            comment (string): A comment about the worklog in [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/). Optional when creating or updating a worklog.
            created (string): The datetime on which the worklog was created.
            id (string): The ID of the worklog record.
            issueId (string): The ID of the issue this worklog is for.
            properties (array): Details of properties for the worklog. Optional when creating or updating a worklog.
            self_arg_body (string): The URL of the worklog item.
            started (string): The datetime on which the worklog effort was started. Required when creating a worklog. Optional when updating a worklog.
            timeSpent (string): The time spent working on the issue as days (\#d), hours (\#h), or minutes (\#m or \#). Required when creating a worklog if `timeSpentSeconds` isn't provided. Optional when updating a worklog. Cannot be provided if `timeSpentSecond` is provided.
            timeSpentSeconds (integer): The time in seconds spent working on the issue. Required when creating a worklog if `timeSpent` isn't provided. Optional when updating a worklog. Cannot be provided if `timeSpent` is provided.
            updateAuthor (string): Details of the user who last updated the worklog.
            updated (string): The datetime on which the worklog was last updated.
            visibility (string): Details about any restrictions in the visibility of the worklog. Optional when creating or updating a worklog.
                Example:
                ```json
                {
                  "comment": {
                    "content": [
                      {
                        "content": [
                          {
                            "text": "I did some work here.",
                            "type": "text"
                          }
                        ],
                        "type": "paragraph"
                      }
                    ],
                    "type": "doc",
                    "version": 1
                  },
                  "started": "2021-01-17T12:34:00.000+0000",
                  "timeSpentSeconds": 12000,
                  "visibility": {
                    "identifier": "276f955c-63d7-42c8-9520-92d01dca0625",
                    "type": "group"
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'author': author,
            'comment': comment,
            'created': created,
            'id': id,
            'issueId': issueId,
            'properties': properties,
            'self': self_arg_body,
            'started': started,
            'timeSpent': timeSpent,
            'timeSpentSeconds': timeSpentSeconds,
            'updateAuthor': updateAuthor,
            'updated': updated,
            'visibility': visibility,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog"
        query_params = {k: v for k, v in [('notifyUsers', notifyUsers), ('adjustEstimate', adjustEstimate), ('newEstimate', newEstimate), ('reduceBy', reduceBy), ('expand', expand), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_move_worklogs(self, issueIdOrKey, adjustEstimate=None, overrideEditableFlag=None, ids=None, issueIdOrKey_body=None) -> Any:
        """
        Moves worklogs from one Jira issue to another using the `POST` method, allowing adjustments to estimates and overriding editable flags if necessary.

        Args:
            issueIdOrKey (string): issueIdOrKey
            adjustEstimate (string): Defines how to update the issues' time estimate, the options are: * `leave` Leaves the estimate unchanged. * `auto` Reduces the estimate by the aggregate value of `timeSpent` across all worklogs being moved in the source issue, and increases it in the destination issue.
            overrideEditableFlag (boolean): Whether the work log entry should be moved to and from the issues even if the issues are not editable, because jira.issue.editable set to false or missing. For example, the issue is closed. Connect and Forge app users with admin permission can use this flag.
            ids (array): A list of worklog IDs.
            issueIdOrKey_body (string): The issue id or key of the destination issue
                Example:
                ```json
                {
                  "ids": [
                    1,
                    2,
                    5,
                    10
                  ],
                  "issueIdOrKey": "ABC-1234"
                }
                ```

        Returns:
            Any: Returned if the request is partially successful.

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        request_body = {
            'ids': ids,
            'issueIdOrKey': issueIdOrKey_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/move"
        query_params = {k: v for k, v in [('adjustEstimate', adjustEstimate), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_worklog(self, issueIdOrKey, id, notifyUsers=None, adjustEstimate=None, newEstimate=None, increaseBy=None, overrideEditableFlag=None) -> Any:
        """
        Deletes a specific worklog entry from a Jira issue using the worklog ID and returns a success status upon removal.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id
            notifyUsers (boolean): Whether users watching the issue are notified by email.
            adjustEstimate (string): Defines how to update the issue's time estimate, the options are: * `new` Sets the estimate to a specific value, defined in `newEstimate`. * `leave` Leaves the estimate unchanged. * `manual` Increases the estimate by amount specified in `increaseBy`. * `auto` Reduces the estimate by the value of `timeSpent` in the worklog.
            newEstimate (string): The value to set as the issue's remaining time estimate, as days (\#d), hours (\#h), or minutes (\#m or \#). For example, *2d*. Required when `adjustEstimate` is `new`.
            increaseBy (string): The amount to increase the issue's remaining estimate by, as days (\#d), hours (\#h), or minutes (\#m or \#). For example, *2d*. Required when `adjustEstimate` is `manual`.
            overrideEditableFlag (boolean): Whether the work log entry should be added to the issue even if the issue is not editable, because jira.issue.editable set to false or missing. For example, the issue is closed. Connect and Forge app users with admin permission can use this flag.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{id}"
        query_params = {k: v for k, v in [('notifyUsers', notifyUsers), ('adjustEstimate', adjustEstimate), ('newEstimate', newEstimate), ('increaseBy', increaseBy), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_worklog(self, issueIdOrKey, id, expand=None) -> dict[str, Any]:
        """
        Retrieves a specific worklog by its ID for a given Jira issue using the GET method.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about work logs in the response. This parameter accepts `properties`, which returns worklog properties.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{id}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_worklog(self, issueIdOrKey, id, notifyUsers=None, adjustEstimate=None, newEstimate=None, expand=None, overrideEditableFlag=None, author=None, comment=None, created=None, id_body=None, issueId=None, properties=None, self_arg_body=None, started=None, timeSpent=None, timeSpentSeconds=None, updateAuthor=None, updated=None, visibility=None) -> dict[str, Any]:
        """
        Updates a specific worklog for an issue in Jira using the PUT method, allowing modifications to attributes such as the worklog comments, time spent, and start date, while requiring permissions to access and edit issue worklogs.

        Args:
            issueIdOrKey (string): issueIdOrKey
            id (string): id
            notifyUsers (boolean): Whether users watching the issue are notified by email.
            adjustEstimate (string): Defines how to update the issue's time estimate, the options are: * `new` Sets the estimate to a specific value, defined in `newEstimate`. * `leave` Leaves the estimate unchanged. * `auto` Updates the estimate by the difference between the original and updated value of `timeSpent` or `timeSpentSeconds`.
            newEstimate (string): The value to set as the issue's remaining time estimate, as days (\#d), hours (\#h), or minutes (\#m or \#). For example, *2d*. Required when `adjustEstimate` is `new`.
            expand (string): Use [expand](#expansion) to include additional information about worklogs in the response. This parameter accepts `properties`, which returns worklog properties.
            overrideEditableFlag (boolean): Whether the worklog should be added to the issue even if the issue is not editable. For example, because the issue is closed. Connect and Forge app users with *Administer Jira* [global permission]( can use this flag.
            author (string): Details of the user who created the worklog.
            comment (string): A comment about the worklog in [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/). Optional when creating or updating a worklog.
            created (string): The datetime on which the worklog was created.
            id_body (string): The ID of the worklog record.
            issueId (string): The ID of the issue this worklog is for.
            properties (array): Details of properties for the worklog. Optional when creating or updating a worklog.
            self_arg_body (string): The URL of the worklog item.
            started (string): The datetime on which the worklog effort was started. Required when creating a worklog. Optional when updating a worklog.
            timeSpent (string): The time spent working on the issue as days (\#d), hours (\#h), or minutes (\#m or \#). Required when creating a worklog if `timeSpentSeconds` isn't provided. Optional when updating a worklog. Cannot be provided if `timeSpentSecond` is provided.
            timeSpentSeconds (integer): The time in seconds spent working on the issue. Required when creating a worklog if `timeSpent` isn't provided. Optional when updating a worklog. Cannot be provided if `timeSpent` is provided.
            updateAuthor (string): Details of the user who last updated the worklog.
            updated (string): The datetime on which the worklog was last updated.
            visibility (string): Details about any restrictions in the visibility of the worklog. Optional when creating or updating a worklog.
                Example:
                ```json
                {
                  "comment": {
                    "content": [
                      {
                        "content": [
                          {
                            "text": "I did some work here.",
                            "type": "text"
                          }
                        ],
                        "type": "paragraph"
                      }
                    ],
                    "type": "doc",
                    "version": 1
                  },
                  "started": "2021-01-17T12:34:00.000+0000",
                  "timeSpentSeconds": 12000,
                  "visibility": {
                    "identifier": "276f955c-63d7-42c8-9520-92d01dca0625",
                    "type": "group"
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful

        Tags:
            Issue worklogs
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'author': author,
            'comment': comment,
            'created': created,
            'id': id_body,
            'issueId': issueId,
            'properties': properties,
            'self': self_arg_body,
            'started': started,
            'timeSpent': timeSpent,
            'timeSpentSeconds': timeSpentSeconds,
            'updateAuthor': updateAuthor,
            'updated': updated,
            'visibility': visibility,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{id}"
        query_params = {k: v for k, v in [('notifyUsers', notifyUsers), ('adjustEstimate', adjustEstimate), ('newEstimate', newEstimate), ('expand', expand), ('overrideEditableFlag', overrideEditableFlag)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_worklog_property_keys(self, issueIdOrKey, worklogId) -> dict[str, Any]:
        """
        Retrieves the keys of all custom properties stored against a specific worklog entry in Jira issues.

        Args:
            issueIdOrKey (string): issueIdOrKey
            worklogId (string): worklogId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklog properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if worklogId is None:
            raise ValueError("Missing required parameter 'worklogId'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_worklog_property(self, issueIdOrKey, worklogId, propertyKey) -> Any:
        """
        Deletes a specific property from a Jira issue's worklog entry.

        Args:
            issueIdOrKey (string): issueIdOrKey
            worklogId (string): worklogId
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the worklog property is removed.

        Tags:
            Issue worklog properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if worklogId is None:
            raise ValueError("Missing required parameter 'worklogId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_worklog_property(self, issueIdOrKey, worklogId, propertyKey) -> dict[str, Any]:
        """
        Retrieves the value of a specific property associated with a worklog for a given issue in Jira using the specified issue ID/key, worklog ID, and property key.

        Args:
            issueIdOrKey (string): issueIdOrKey
            worklogId (string): worklogId
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklog properties
        """
        if issueIdOrKey is None:
            raise ValueError("Missing required parameter 'issueIdOrKey'")
        if worklogId is None:
            raise ValueError("Missing required parameter 'worklogId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issue/{issueIdOrKey}/worklog/{worklogId}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def link_issues(self, inwardIssue, outwardIssue, type, comment=None) -> Any:
        """
        Creates a link between two Jira issues, allowing you to define the relationship type and optionally include a comment, using the POST method at the "/rest/api/3/issueLink" endpoint.

        Args:
            inwardIssue (object): The ID or key of a linked issue.
            outwardIssue (object): The ID or key of a linked issue.
            type (object): This object is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it defines and reports on the type of link between the issues. Find a list of issue link types with [Get issue link types](#api-rest-api-3-issueLinkType-get).
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it defines and reports on issue link types.
            comment (object): A comment.
                Example:
                ```json
                {
                  "comment": {
                    "body": {
                      "content": [
                        {
                          "content": [
                            {
                              "text": "Linked related issue!",
                              "type": "text"
                            }
                          ],
                          "type": "paragraph"
                        }
                      ],
                      "type": "doc",
                      "version": 1
                    },
                    "visibility": {
                      "identifier": "276f955c-63d7-42c8-9520-92d01dca0625",
                      "type": "group",
                      "value": "jira-software-users"
                    }
                  },
                  "inwardIssue": {
                    "key": "HSP-1"
                  },
                  "outwardIssue": {
                    "key": "MKY-1"
                  },
                  "type": {
                    "name": "Duplicate"
                  }
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue links
        """
        request_body = {
            'comment': comment,
            'inwardIssue': inwardIssue,
            'outwardIssue': outwardIssue,
            'type': type,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issueLink"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_link(self, linkId) -> Any:
        """
        Deletes a specific issue link in Jira by its link ID and returns a success status.

        Args:
            linkId (string): linkId

        Returns:
            Any: 200 response

        Tags:
            Issue links
        """
        if linkId is None:
            raise ValueError("Missing required parameter 'linkId'")
        url = f"{self.base_url}/rest/api/3/issueLink/{linkId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_link(self, linkId) -> dict[str, Any]:
        """
        Retrieves details of a specific issue link in Jira by its unique identifier using the Jira REST API.

        Args:
            linkId (string): linkId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue links
        """
        if linkId is None:
            raise ValueError("Missing required parameter 'linkId'")
        url = f"{self.base_url}/rest/api/3/issueLink/{linkId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_link_types(self) -> dict[str, Any]:
        """
        Retrieves information about an issue link type in Jira using the provided ID.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue link types
        """
        url = f"{self.base_url}/rest/api/3/issueLinkType"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_link_type(self, id=None, inward=None, name=None, outward=None, self_arg_body=None) -> dict[str, Any]:
        """
        Creates a new issue link type in Jira to define relationships between linked issues.

        Args:
            id (string): The ID of the issue link type and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is the type of issue link. Required on create when `name` isn't provided. Otherwise, read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is read only.
            inward (string): The description of the issue link type inward link and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            name (string): The name of the issue link type and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is the type of issue link. Required on create when `id` isn't provided. Otherwise, read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            outward (string): The description of the issue link type outward link and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            self_arg_body (string): The URL of the issue link type. Read only.
                Example:
                ```json
                {
                  "inward": "Duplicated by",
                  "name": "Duplicate",
                  "outward": "Duplicates"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue link types
        """
        request_body = {
            'id': id,
            'inward': inward,
            'name': name,
            'outward': outward,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issueLinkType"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_link_type(self, issueLinkTypeId) -> Any:
        """
        Deletes a specified issue link type in Jira and returns a success status upon removal.

        Args:
            issueLinkTypeId (string): issueLinkTypeId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue link types
        """
        if issueLinkTypeId is None:
            raise ValueError("Missing required parameter 'issueLinkTypeId'")
        url = f"{self.base_url}/rest/api/3/issueLinkType/{issueLinkTypeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_link_type(self, issueLinkTypeId) -> dict[str, Any]:
        """
        Retrieves a specific issue link type by its ID from Jira, including relationship descriptions for inward and outward links.

        Args:
            issueLinkTypeId (string): issueLinkTypeId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue link types
        """
        if issueLinkTypeId is None:
            raise ValueError("Missing required parameter 'issueLinkTypeId'")
        url = f"{self.base_url}/rest/api/3/issueLinkType/{issueLinkTypeId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_link_type(self, issueLinkTypeId, id=None, inward=None, name=None, outward=None, self_arg_body=None) -> dict[str, Any]:
        """
        Updates the specified issue link type (e.g., Duplicate, Blocks) by ID to modify its name and relationship descriptions.

        Args:
            issueLinkTypeId (string): issueLinkTypeId
            id (string): The ID of the issue link type and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is the type of issue link. Required on create when `name` isn't provided. Otherwise, read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is read only.
            inward (string): The description of the issue link type inward link and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            name (string): The name of the issue link type and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is the type of issue link. Required on create when `id` isn't provided. Otherwise, read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            outward (string): The description of the issue link type outward link and is used as follows:

         *  In the [ issueLink](#api-rest-api-3-issueLink-post) resource it is read only.
         *  In the [ issueLinkType](#api-rest-api-3-issueLinkType-post) resource it is required on create and optional on update. Otherwise, read only.
            self_arg_body (string): The URL of the issue link type. Read only.
                Example:
                ```json
                {
                  "inward": "Duplicated by",
                  "name": "Duplicate",
                  "outward": "Duplicates"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue link types
        """
        if issueLinkTypeId is None:
            raise ValueError("Missing required parameter 'issueLinkTypeId'")
        request_body = {
            'id': id,
            'inward': inward,
            'name': name,
            'outward': outward,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issueLinkType/{issueLinkTypeId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def export_archived_issues(self, archivedBy=None, archivedDateRange=None, issueTypes=None, projects=None, reporters=None) -> dict[str, Any]:
        """
        Exports archived issues using the Jira API, initiating a task that sends an email with a link to download a CSV file containing the issue details upon completion.

        Args:
            archivedBy (array): List archived issues archived by a specified account ID.
            archivedDateRange (object): List issues archived within a specified date range.
            issueTypes (array): List archived issues with a specified issue type ID.
            projects (array): List archived issues with a specified project key.
            reporters (array): List archived issues where the reporter is a specified account ID.
                Example:
                ```json
                {
                  "archivedBy": [
                    "uuid-rep-001",
                    "uuid-rep-002"
                  ],
                  "archivedDate": {
                    "dateAfter": "2023-01-01",
                    "dateBefore": "2023-01-12"
                  },
                  "archivedDateRange": {
                    "dateAfter": "2023-01-01",
                    "dateBefore": "2023-01-12"
                  },
                  "issueTypes": [
                    "10001",
                    "10002"
                  ],
                  "projects": [
                    "FOO",
                    "BAR"
                  ],
                  "reporters": [
                    "uuid-rep-001",
                    "uuid-rep-002"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returns the details of your export task. You can use the [get task](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-tasks/#api-rest-api-3-task-taskid-get) API to view the progress of your request.

        Tags:
            Issues
        """
        request_body = {
            'archivedBy': archivedBy,
            'archivedDateRange': archivedDateRange,
            'issueTypes': issueTypes,
            'projects': projects,
            'reporters': reporters,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issues/archive/export"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_security_schemes(self) -> dict[str, Any]:
        """
        Retrieves a list of all issue security schemes available in a Jira instance, allowing administrators to manage which users or groups can view issues.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_security_scheme(self, name, description=None, levels=None) -> dict[str, Any]:
        """
        Creates an issue security scheme in Jira Cloud using the POST method, allowing administrators to define security levels and members, and returns the ID of the newly created scheme upon success.

        Args:
            name (string): The name of the issue security scheme. Must be unique (case-insensitive).
            description (string): The description of the issue security scheme.
            levels (array): The list of scheme levels which should be added to the security scheme.
                Example:
                ```json
                {
                  "description": "Newly created issue security scheme",
                  "levels": [
                    {
                      "description": "Newly created level",
                      "isDefault": true,
                      "members": [
                        {
                          "parameter": "administrators",
                          "type": "group"
                        }
                      ],
                      "name": "New level"
                    }
                  ],
                  "name": "New security scheme"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        request_body = {
            'description': description,
            'levels': levels,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_security_levels(self, startAt=None, maxResults=None, id=None, schemeId=None, onlyDefault=None) -> dict[str, Any]:
        """
        Retrieves details of issue security levels within a scheme, including pagination support and filtering by scheme ID or default status.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of issue security scheme level IDs. To include multiple issue security levels, separate IDs with an ampersand: `id=10000&id=10001`.
            schemeId (array): The list of issue security scheme IDs. To include multiple issue security schemes, separate IDs with an ampersand: `schemeId=10000&schemeId=10001`.
            onlyDefault (boolean): When set to true, returns multiple default levels for each security scheme containing a default. If you provide scheme and level IDs not associated with the default, returns an empty page. The default value is false.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/level"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('schemeId', schemeId), ('onlyDefault', onlyDefault)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_default_levels(self, defaultValues) -> Any:
        """
        Sets default issue security levels for schemes, allowing administrators to configure which security levels are applied by default across specified issue security schemes.

        Args:
            defaultValues (array): List of objects with issue security scheme ID and new default level ID.
                Example:
                ```json
                {
                  "defaultValues": [
                    {
                      "defaultLevelId": "20000",
                      "issueSecuritySchemeId": "10000"
                    },
                    {
                      "defaultLevelId": "30000",
                      "issueSecuritySchemeId": "12000"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        request_body = {
            'defaultValues': defaultValues,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/level/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_security_level_members(self, startAt=None, maxResults=None, id=None, schemeId=None, levelId=None, expand=None) -> dict[str, Any]:
        """
        Retrieves the members of a specific issue security level using the Jira Cloud API, allowing for pagination and expansion of details by specifying parameters such as start index, maximum results, and expansion options.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of issue security level member IDs. To include multiple issue security level members separate IDs with an ampersand: `id=10000&id=10001`.
            schemeId (array): The list of issue security scheme IDs. To include multiple issue security schemes separate IDs with an ampersand: `schemeId=10000&schemeId=10001`.
            levelId (array): The list of issue security level IDs. To include multiple issue security levels separate IDs with an ampersand: `levelId=10000&levelId=10001`.
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `all` Returns all expandable information * `field` Returns information about the custom field granted the permission * `group` Returns information about the group that is granted the permission * `projectRole` Returns information about the project role granted the permission * `user` Returns information about the user who is granted the permission

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/level/member"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('schemeId', schemeId), ('levelId', levelId), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_projects_using_security_schemes(self, startAt=None, maxResults=None, issueSecuritySchemeId=None, projectId=None) -> dict[str, Any]:
        """
        Retrieves projects associated with specific issue security schemes based on scheme ID or project ID query parameters.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            issueSecuritySchemeId (array): The list of security scheme IDs to be filtered out.
            projectId (array): The list of project IDs to be filtered out.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('issueSecuritySchemeId', issueSecuritySchemeId), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def associate_schemes_to_projects(self, projectId, schemeId, oldToNewSecurityLevelMappings=None) -> Any:
        """
        Associates an issue security scheme with a project using the Jira Cloud API, allowing for the remapping of security levels for issues, with the operation being asynchronous.

        Args:
            projectId (string): The ID of the project.
            schemeId (string): The ID of the issue security scheme. Providing null will clear the association with the issue security scheme.
            oldToNewSecurityLevelMappings (array): The list of scheme levels which should be remapped to new levels of the issue security scheme.
                Example:
                ```json
                {
                  "oldToNewSecurityLevelMappings": [
                    {
                      "newLevelId": "30001",
                      "oldLevelId": "30000"
                    }
                  ],
                  "projectId": "10000",
                  "schemeId": "20000"
                }
                ```

        Returns:
            Any: API response data.

        Tags:
            Issue security schemes
        """
        request_body = {
            'oldToNewSecurityLevelMappings': oldToNewSecurityLevelMappings,
            'projectId': projectId,
            'schemeId': schemeId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_security_schemes(self, startAt=None, maxResults=None, id=None, projectId=None) -> dict[str, Any]:
        """
        Searches for and returns issue security schemes in Jira Cloud, allowing filtering by start index, maximum results, ID, or project ID.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of issue security scheme IDs. To include multiple issue security scheme IDs, separate IDs with an ampersand: `id=10000&id=10001`.
            projectId (array): The list of project IDs. To include multiple project IDs, separate IDs with an ampersand: `projectId=10000&projectId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_security_scheme(self, id) -> dict[str, Any]:
        """
        Retrieves the details of a specific issue security scheme by its ID, including associated security levels and project mappings.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_security_scheme(self, id, description=None, name=None) -> Any:
        """
        Updates an existing issue security scheme by specifying the ID in the path using the Jira Cloud API.

        Args:
            id (string): id
            description (string): The description of the security scheme scheme.
            name (string): The name of the security scheme scheme. Must be unique.
                Example:
                ```json
                {
                  "description": "My issue security scheme description",
                  "name": "My issue security scheme name"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_security_level_members(self, issueSecuritySchemeId, startAt=None, maxResults=None, issueSecurityLevelId=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of members associated with issue security levels in a specified issue security scheme using the Jira API.

        Args:
            issueSecuritySchemeId (string): issueSecuritySchemeId
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            issueSecurityLevelId (array): The list of issue security level IDs. To include multiple issue security levels separate IDs with ampersand: `issueSecurityLevelId=10000&issueSecurityLevelId=10001`.
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security level
        """
        if issueSecuritySchemeId is None:
            raise ValueError("Missing required parameter 'issueSecuritySchemeId'")
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{issueSecuritySchemeId}/members"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('issueSecurityLevelId', issueSecurityLevelId), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_security_scheme(self, schemeId) -> Any:
        """
        Deletes an issue security scheme in Jira and disassociates it from all projects.

        Args:
            schemeId (string): schemeId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_security_level(self, schemeId, levels=None) -> Any:
        """
        Updates an issue security level within a specified security scheme in Jira.

        Args:
            schemeId (string): schemeId
            levels (array): The list of scheme levels which should be added to the security scheme.
                Example:
                ```json
                {
                  "levels": [
                    {
                      "description": "First Level Description",
                      "isDefault": true,
                      "members": [
                        {
                          "type": "reporter"
                        },
                        {
                          "parameter": "jira-administrators",
                          "type": "group"
                        }
                      ],
                      "name": "First Level"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        request_body = {
            'levels': levels,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}/level"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_level(self, schemeId, levelId, replaceWith=None) -> Any:
        """
        Deletes an issue security level with the specified `levelId` from an issue security scheme identified by `schemeId`, optionally allowing replacement with another level using the `replaceWith` query parameter.

        Args:
            schemeId (string): schemeId
            levelId (string): levelId
            replaceWith (string): The ID of the issue security level that will replace the currently selected level.

        Returns:
            Any: API response data.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if levelId is None:
            raise ValueError("Missing required parameter 'levelId'")
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}"
        query_params = {k: v for k, v in [('replaceWith', replaceWith)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_security_level(self, schemeId, levelId, description=None, name=None) -> Any:
        """
        Updates an issue security level in a Jira issue security scheme by modifying its name and description using the `PUT` method.

        Args:
            schemeId (string): schemeId
            levelId (string): levelId
            description (string): The description of the issue security scheme level.
            name (string): The name of the issue security scheme level. Must be unique.
                Example:
                ```json
                {
                  "description": "New level description",
                  "name": "New level name"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if levelId is None:
            raise ValueError("Missing required parameter 'levelId'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_security_level_members(self, schemeId, levelId, members=None) -> Any:
        """
        Adds members to a specific security level within an issue security scheme in Jira.

        Args:
            schemeId (string): schemeId
            levelId (string): levelId
            members (array): The list of level members which should be added to the issue security scheme level.
                Example:
                ```json
                {
                  "members": [
                    {
                      "type": "reporter"
                    },
                    {
                      "parameter": "jira-administrators",
                      "type": "group"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if levelId is None:
            raise ValueError("Missing required parameter 'levelId'")
        request_body = {
            'members': members,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_member_from_security_level(self, schemeId, levelId, memberId) -> Any:
        """
        Removes a specified member from an issue security level within a Jira issue security scheme.

        Args:
            schemeId (string): schemeId
            levelId (string): levelId
            memberId (string): memberId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue security schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if levelId is None:
            raise ValueError("Missing required parameter 'levelId'")
        if memberId is None:
            raise ValueError("Missing required parameter 'memberId'")
        url = f"{self.base_url}/rest/api/3/issuesecurityschemes/{schemeId}/level/{levelId}/member/{memberId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_all_types(self) -> list[Any]:
        """
        Retrieves a list of all issue types available in Jira using the GET method at the "/rest/api/3/issuetype" endpoint.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        url = f"{self.base_url}/rest/api/3/issuetype"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_type(self, name, description=None, hierarchyLevel=None, type=None) -> dict[str, Any]:
        """
        Creates a new issue type in Jira and adds it to the default issue type scheme.

        Args:
            name (string): The unique name for the issue type. The maximum length is 60 characters.
            description (string): The description of the issue type.
            hierarchyLevel (integer): The hierarchy level of the issue type. Use:

         *  `-1` for Subtask.
         *  `0` for Base.

        Defaults to `0`.
            type (string): Deprecated. Use `hierarchyLevel` instead. See the [deprecation notice](https://community.developer.atlassian.com/t/deprecation-of-the-epic-link-parent-link-and-other-related-fields-in-rest-apis-and-webhooks/54048) for details.

        Whether the issue type is `subtype` or `standard`. Defaults to `standard`.
                Example:
                ```json
                {
                  "description": "description",
                  "name": "name",
                  "type": "standard"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        request_body = {
            'description': description,
            'hierarchyLevel': hierarchyLevel,
            'name': name,
            'type': type,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetype"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_types_for_project(self, projectId, level=None) -> list[Any]:
        """
        Retrieves issue types associated with a specified project in Jira using the "GET" method at the "/rest/api/3/issuetype/project" endpoint.

        Args:
            projectId (integer): The ID of the project.
            level (integer): The level of the issue type to filter by. Use: * `-1` for Subtask. * `0` for Base. * `1` for Epic.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        url = f"{self.base_url}/rest/api/3/issuetype/project"
        query_params = {k: v for k, v in [('projectId', projectId), ('level', level)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_type(self, id, alternativeIssueTypeId=None) -> Any:
        """
        Deletes the specified Jira issue type and migrates associated issues to an alternative type if provided.

        Args:
            id (string): id
            alternativeIssueTypeId (string): The ID of the replacement issue type.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue types
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issuetype/{id}"
        query_params = {k: v for k, v in [('alternativeIssueTypeId', alternativeIssueTypeId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type(self, id) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific issue type in Jira by its ID using the "GET" method.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issuetype/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_type(self, id, avatarId=None, description=None, name=None) -> dict[str, Any]:
        """
        Updates an existing Jira issue type by its ID, returning the modified issue type details or relevant error responses.

        Args:
            id (string): id
            avatarId (integer): The ID of an issue type avatar.
            description (string): The description of the issue type.
            name (string): The unique name for the issue type. The maximum length is 60 characters.
                Example:
                ```json
                {
                  "avatarId": 1,
                  "description": "description",
                  "name": "name"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'avatarId': avatarId,
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetype/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_alternative_issue_types(self, id) -> list[Any]:
        """
        Retrieves alternative issue types for a specified issue type ID using the Jira Cloud REST API.

        Args:
            id (string): id

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue types
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/issuetype/{id}/alternatives"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def get_issue_type_property_keys(self, issueTypeId) -> dict[str, Any]:
        """
        Retrieves all property keys for a specific Jira issue type using the issueTypeId path parameter.

        Args:
            issueTypeId (string): issueTypeId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type properties
        """
        if issueTypeId is None:
            raise ValueError("Missing required parameter 'issueTypeId'")
        url = f"{self.base_url}/rest/api/3/issuetype/{issueTypeId}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_type_property(self, issueTypeId, propertyKey) -> Any:
        """
        Deletes a specific property from an issue type in Jira using the specified property key and issue type ID.

        Args:
            issueTypeId (string): issueTypeId
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the issue type property is deleted.

        Tags:
            Issue type properties
        """
        if issueTypeId is None:
            raise ValueError("Missing required parameter 'issueTypeId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_property(self, issueTypeId, propertyKey) -> dict[str, Any]:
        """
        Retrieves a specific custom property associated with an issue type using its unique identifier and property key.

        Args:
            issueTypeId (string): issueTypeId
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type properties
        """
        if issueTypeId is None:
            raise ValueError("Missing required parameter 'issueTypeId'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/issuetype/{issueTypeId}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def get_all_issue_type_schemes(self, startAt=None, maxResults=None, id=None, orderBy=None, expand=None, queryString=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of issue type schemes with optional filtering by ID, ordering, and expansion of related entities.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of issue type schemes IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.
            orderBy (string): [Order](#ordering) the results by a field: * `name` Sorts by issue type scheme name. * `id` Sorts by issue type scheme ID.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `projects` For each issue type schemes, returns information about the projects the issue type scheme is assigned to. * `issueTypes` For each issue type schemes, returns information about the issueTypes the issue type scheme have.
            queryString (string): String used to perform a case-insensitive partial match with issue type scheme name.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('orderBy', orderBy), ('expand', expand), ('queryString', queryString)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_type_scheme(self, issueTypeIds, name, defaultIssueTypeId=None, description=None) -> dict[str, Any]:
        """
        Creates a new issue type scheme in Jira and returns the created resource.

        Args:
            issueTypeIds (array): The list of issue types IDs of the issue type scheme. At least one standard issue type ID is required.
            name (string): The name of the issue type scheme. The name must be unique. The maximum length is 255 characters.
            defaultIssueTypeId (string): The ID of the default issue type of the issue type scheme. This ID must be included in `issueTypeIds`.
            description (string): The description of the issue type scheme. The maximum length is 4000 characters.
                Example:
                ```json
                {
                  "defaultIssueTypeId": "10002",
                  "description": "A collection of issue types suited to use in a kanban style project.",
                  "issueTypeIds": [
                    "10001",
                    "10002",
                    "10003"
                  ],
                  "name": "Kanban Issue Type Scheme"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        request_body = {
            'defaultIssueTypeId': defaultIssueTypeId,
            'description': description,
            'issueTypeIds': issueTypeIds,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_schemes_mapping(self, startAt=None, maxResults=None, issueTypeSchemeId=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of issue type scheme mappings for classic Jira projects, filtered by scheme ID.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            issueTypeSchemeId (array): The list of issue type scheme IDs. To include multiple IDs, provide an ampersand-separated list. For example, `issueTypeSchemeId=10000&issueTypeSchemeId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescheme/mapping"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('issueTypeSchemeId', issueTypeSchemeId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_scheme_for_projects(self, projectId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of issue type schemes associated with specific Jira projects using query parameters for pagination (startAt, maxResults) and project filtering (projectId).

        Args:
            projectId (array): The list of project IDs. To include multiple project IDs, provide an ampersand-separated list. For example, `projectId=10000&projectId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescheme/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_issue_type_scheme_to_project(self, issueTypeSchemeId, projectId) -> Any:
        """
        Assigns an issue type scheme to a Jira Cloud project, requiring global Administer Jira permissions and validating all project issues use scheme types.

        Args:
            issueTypeSchemeId (string): The ID of the issue type scheme.
            projectId (string): The ID of the project.
                Example:
                ```json
                {
                  "issueTypeSchemeId": "10000",
                  "projectId": "10000"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        request_body = {
            'issueTypeSchemeId': issueTypeSchemeId,
            'projectId': projectId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescheme/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_type_scheme(self, issueTypeSchemeId) -> Any:
        """
        Deletes an issue type scheme by its ID, reassigning any associated projects to the default issue type scheme.

        Args:
            issueTypeSchemeId (string): issueTypeSchemeId

        Returns:
            Any: Returned if the issue type scheme is deleted.

        Tags:
            Issue type schemes
        """
        if issueTypeSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeSchemeId'")
        url = f"{self.base_url}/rest/api/3/issuetypescheme/{issueTypeSchemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_type_scheme(self, issueTypeSchemeId, defaultIssueTypeId=None, description=None, name=None) -> Any:
        """
        Updates an issue type scheme by modifying its configuration (such as associated issue types) for the specified scheme ID.

        Args:
            issueTypeSchemeId (string): issueTypeSchemeId
            defaultIssueTypeId (string): The ID of the default issue type of the issue type scheme.
            description (string): The description of the issue type scheme. The maximum length is 4000 characters.
            name (string): The name of the issue type scheme. The name must be unique. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "defaultIssueTypeId": "10002",
                  "description": "A collection of issue types suited to use in a kanban style project.",
                  "name": "Kanban Issue Type Scheme"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        if issueTypeSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeSchemeId'")
        request_body = {
            'defaultIssueTypeId': defaultIssueTypeId,
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescheme/{issueTypeSchemeId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_issue_types_to_issue_type_scheme(self, issueTypeSchemeId, issueTypeIds) -> Any:
        """
        Adds issue types to an existing issue type scheme in Jira Cloud, appending them to the current list and returning a success status if the operation completes without conflicts.

        Args:
            issueTypeSchemeId (string): issueTypeSchemeId
            issueTypeIds (array): The list of issue type IDs.
                Example:
                ```json
                {
                  "issueTypeIds": [
                    "10000",
                    "10002",
                    "10003"
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        if issueTypeSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeSchemeId'")
        request_body = {
            'issueTypeIds': issueTypeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def reorder_issue_types_in_issue_type_scheme(self, issueTypeSchemeId, issueTypeIds, after=None, position=None) -> Any:
        """
        Moves issue types within a specified issue type scheme in Jira and returns an empty response on success.

        Args:
            issueTypeSchemeId (string): issueTypeSchemeId
            issueTypeIds (array): A list of the issue type IDs to move. The order of the issue type IDs in the list is the order they are given after the move.
            after (string): The ID of the issue type to place the moved issue types after. Required if `position` isn't provided.
            position (string): The position the issue types should be moved to. Required if `after` isn't provided.
                Example:
                ```json
                {
                  "after": "10008",
                  "issueTypeIds": [
                    "10001",
                    "10004",
                    "10002"
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        if issueTypeSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeSchemeId'")
        request_body = {
            'after': after,
            'issueTypeIds': issueTypeIds,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/move"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_issue_type_from_issue_type_scheme(self, issueTypeSchemeId, issueTypeId) -> Any:
        """
        Deletes an issue type from an issue type scheme using the Jira Cloud API by specifying the `issueTypeSchemeId` and `issueTypeId`, allowing for removal of issue types from schemes.

        Args:
            issueTypeSchemeId (string): issueTypeSchemeId
            issueTypeId (string): issueTypeId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type schemes
        """
        if issueTypeSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeSchemeId'")
        if issueTypeId is None:
            raise ValueError("Missing required parameter 'issueTypeId'")
        url = f"{self.base_url}/rest/api/3/issuetypescheme/{issueTypeSchemeId}/issuetype/{issueTypeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_screen_schemes(self, startAt=None, maxResults=None, id=None, queryString=None, orderBy=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of issue type screen schemes in Jira with options to filter, paginate, and expand results.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of issue type screen scheme IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.
            queryString (string): String used to perform a case-insensitive partial match with issue type screen scheme name.
            orderBy (string): [Order](#ordering) the results by a field: * `name` Sorts by issue type screen scheme name. * `id` Sorts by issue type screen scheme ID.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts `projects` that, for each issue type screen schemes, returns information about the projects the issue type screen scheme is assigned to.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('queryString', queryString), ('orderBy', orderBy), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_issue_type_screen_scheme(self, issueTypeMappings, name, description=None) -> dict[str, Any]:
        """
        Creates an issue type screen scheme using the Jira Cloud API, allowing administrators to map issue types to specific screen schemes for organizing project workflows.

        Args:
            issueTypeMappings (array): The IDs of the screen schemes for the issue type IDs and *default*. A *default* entry is required to create an issue type screen scheme, it defines the mapping for all issue types without a screen scheme.
            name (string): The name of the issue type screen scheme. The name must be unique. The maximum length is 255 characters.
            description (string): The description of the issue type screen scheme. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "issueTypeMappings": [
                    {
                      "issueTypeId": "default",
                      "screenSchemeId": "10001"
                    },
                    {
                      "issueTypeId": "10001",
                      "screenSchemeId": "10002"
                    },
                    {
                      "issueTypeId": "10002",
                      "screenSchemeId": "10002"
                    }
                  ],
                  "name": "Scrum issue type screen scheme"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        request_body = {
            'description': description,
            'issueTypeMappings': issueTypeMappings,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_screen_scheme_mappings(self, startAt=None, maxResults=None, issueTypeScreenSchemeId=None) -> dict[str, Any]:
        """
        Retrieves a list of issue type to screen scheme mappings associated with a specified issue type screen scheme using the Jira Cloud API.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            issueTypeScreenSchemeId (array): The list of issue type screen scheme IDs. To include multiple issue type screen schemes, separate IDs with ampersand: `issueTypeScreenSchemeId=10000&issueTypeScreenSchemeId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/mapping"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('issueTypeScreenSchemeId', issueTypeScreenSchemeId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_type_screen_scheme_project_associations(self, projectId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of issue type screen schemes and their associated projects using the specified query parameters.

        Args:
            projectId (array): The list of project IDs. To include multiple projects, separate IDs with ampersand: `projectId=10000&projectId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_issue_type_screen_scheme_to_project(self, issueTypeScreenSchemeId=None, projectId=None) -> Any:
        """
        Assigns an issue type screen scheme to a project using the Jira API, requiring *Administer Jira* global permission to update project configurations.

        Args:
            issueTypeScreenSchemeId (string): The ID of the issue type screen scheme.
            projectId (string): The ID of the project.
                Example:
                ```json
                {
                  "issueTypeScreenSchemeId": "10001",
                  "projectId": "10002"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        request_body = {
            'issueTypeScreenSchemeId': issueTypeScreenSchemeId,
            'projectId': projectId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_issue_type_screen_scheme(self, issueTypeScreenSchemeId) -> Any:
        """
        Deletes an issue type screen scheme in Jira and returns a success status upon removal.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId

        Returns:
            Any: Returned if the issue type screen scheme is deleted.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_issue_type_screen_scheme(self, issueTypeScreenSchemeId, description=None, name=None) -> Any:
        """
        Updates the default screen scheme for unmapped issue types in the specified issue type screen scheme.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId
            description (string): The description of the issue type screen scheme. The maximum length is 255 characters.
            name (string): The name of the issue type screen scheme. The name must be unique. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "description": "Screens for scrum issue types.",
                  "name": "Scrum scheme"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def append_mappings_for_issue_type_screen_scheme(self, issueTypeScreenSchemeId, issueTypeMappings) -> Any:
        """
        Updates the mappings of an issue type screen scheme using the PUT method, specifically allowing administrators to append or modify issue type to screen scheme mappings by providing the necessary `issueTypeScreenSchemeId` in the path.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId
            issueTypeMappings (array): The list of issue type to screen scheme mappings. A *default* entry cannot be specified because a default entry is added when an issue type screen scheme is created.
                Example:
                ```json
                {
                  "issueTypeMappings": [
                    {
                      "issueTypeId": "10000",
                      "screenSchemeId": "10001"
                    },
                    {
                      "issueTypeId": "10001",
                      "screenSchemeId": "10002"
                    },
                    {
                      "issueTypeId": "10002",
                      "screenSchemeId": "10002"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        request_body = {
            'issueTypeMappings': issueTypeMappings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_default_screen_scheme(self, issueTypeScreenSchemeId, screenSchemeId) -> Any:
        """
        Updates the default screen scheme mapping for an issue type screen scheme identified by the `{issueTypeScreenSchemeId}` using the PUT method, which is used for all unmapped issue types in Jira.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId
            screenSchemeId (string): The ID of the screen scheme.
                Example:
                ```json
                {
                  "screenSchemeId": "10010"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        request_body = {
            'screenSchemeId': screenSchemeId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_mappings_from_issue_type_screen_scheme(self, issueTypeScreenSchemeId, issueTypeIds) -> Any:
        """
        Removes issue type to screen scheme mappings from an issue type screen scheme in Jira using the provided issue type IDs.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId
            issueTypeIds (array): The list of issue type IDs.
                Example:
                ```json
                {
                  "issueTypeIds": [
                    "10000",
                    "10001",
                    "10004"
                  ]
                }
                ```

        Returns:
            Any: Returned if the screen scheme mappings are removed from the issue type screen scheme.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        request_body = {
            'issueTypeIds': issueTypeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/mapping/remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_projects_for_issue_type_screen_scheme(self, issueTypeScreenSchemeId, startAt=None, maxResults=None, query=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of projects associated with a specific issue type screen scheme.

        Args:
            issueTypeScreenSchemeId (string): issueTypeScreenSchemeId
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            query (string): Filter issues by a JQL (Jira Query Language) statement to narrow down the results from the specified issue type screen scheme and project.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue type screen schemes
        """
        if issueTypeScreenSchemeId is None:
            raise ValueError("Missing required parameter 'issueTypeScreenSchemeId'")
        url = f"{self.base_url}/rest/api/3/issuetypescreenscheme/{issueTypeScreenSchemeId}/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('query', query)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_auto_complete(self) -> dict[str, Any]:
        """
        Retrieves JQL search auto-complete data including field references, operators, and suggestions to assist in programmatic query construction.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL
        """
        url = f"{self.base_url}/rest/api/3/jql/autocompletedata"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_auto_complete_post(self, includeCollapsedFields=None, projectIds=None) -> dict[str, Any]:
        """
        Provides JQL search auto-complete data and field reference information to assist in programmatic query construction or validation.

        Args:
            includeCollapsedFields (boolean): Include collapsed fields for fields that have non-unique names.
            projectIds (array): List of project IDs used to filter the visible field details returned.
                Example:
                ```json
                {
                  "includeCollapsedFields": true,
                  "projectIds": [
                    10000,
                    10001,
                    10002
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL
        """
        request_body = {
            'includeCollapsedFields': includeCollapsedFields,
            'projectIds': projectIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/autocompletedata"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_field_auto_complete_for_query_string(self, fieldName=None, fieldValue=None, predicateName=None, predicateValue=None) -> dict[str, Any]:
        """
        Retrieves JQL search autocomplete suggestions for specific fields, values, predicates, or predicate values to assist in query construction.

        Args:
            fieldName (string): The name of the field. Example: 'reporter'.
            fieldValue (string): The partial field item name entered by the user.
            predicateName (string): The name of the [ CHANGED operator predicate]( for which the suggestions are generated. The valid predicate operators are *by*, *from*, and *to*.
            predicateValue (string): The partial predicate item name entered by the user.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL
        """
        url = f"{self.base_url}/rest/api/3/jql/autocompletedata/suggestions"
        query_params = {k: v for k, v in [('fieldName', fieldName), ('fieldValue', fieldValue), ('predicateName', predicateName), ('predicateValue', predicateValue)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_precomputations(self, functionKey=None, startAt=None, maxResults=None, orderBy=None) -> dict[str, Any]:
        """
        Retrieves a list of precomputations for a specified JQL function, including when they were created, updated, and last used, allowing apps to inspect their own functions.

        Args:
            functionKey (array): The function key in format: * Forge: `ari:cloud:ecosystem::extension/[App ID]/[Environment ID]/static/[Function key from manifest]` * Connect: `[App key]__[Module key]`
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field: * `functionKey` Sorts by the functionKey. * `used` Sorts by the used timestamp. * `created` Sorts by the created timestamp. * `updated` Sorts by the updated timestamp.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL functions (apps)
        """
        url = f"{self.base_url}/rest/api/3/jql/function/computation"
        query_params = {k: v for k, v in [('functionKey', functionKey), ('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_precomputations(self, skipNotFoundPrecomputations=None, values=None) -> dict[str, Any]:
        """
        Updates precomputations (JQL fragments mapped to custom functions) and optionally skips invalid entries based on query parameters.

        Args:
            skipNotFoundPrecomputations (boolean): Specifies whether to skip precomputations when referenced entities (e.g., users, projects) are not found during JQL function processing.
            values (array): values
                Example:
                ```json
                {
                  "values": [
                    {
                      "id": "f2ef228b-367f-4c6b-bd9d-0d0e96b5bd7b",
                      "value": "issue in (TEST-1, TEST-2, TEST-3)"
                    },
                    {
                      "error": "Error message to be displayed to the user",
                      "id": "2a854f11-d0e1-4260-aea8-64a562a7062a"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: 200 response

        Tags:
            JQL functions (apps)
        """
        request_body = {
            'values': values,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/function/computation"
        query_params = {k: v for k, v in [('skipNotFoundPrecomputations', skipNotFoundPrecomputations)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_precomputations_by_id(self, orderBy=None, precomputationIDs=None) -> dict[str, Any]:
        """
        Performs a computation search using JQL functions in Jira Cloud, allowing users to specify an **orderBy** parameter and returns the results of the computation search via a POST request.

        Args:
            orderBy (string): [Order](#ordering) the results by a field: * `functionKey` Sorts by the functionKey. * `used` Sorts by the used timestamp. * `created` Sorts by the created timestamp. * `updated` Sorts by the updated timestamp.
            precomputationIDs (array): precomputationIDs
                Example:
                ```json
                {
                  "precomputationIDs": [
                    "f2ef228b-367f-4c6b-bd9d-0d0e96b5bd7b",
                    "2a854f11-d0e1-4260-aea8-64a562a7062a"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL functions (apps)
        """
        request_body = {
            'precomputationIDs': precomputationIDs,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/function/computation/search"
        query_params = {k: v for k, v in [('orderBy', orderBy)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def match_issues(self, issueIds, jqls) -> dict[str, Any]:
        """
        Checks which issues from a provided list match specified JQL queries and returns matched issues for each query.

        Args:
            issueIds (array): A list of issue IDs.
            jqls (array): A list of JQL queries.
                Example:
                ```json
                {
                  "issueIds": [
                    10001,
                    1000,
                    10042
                  ],
                  "jqls": [
                    "project = FOO",
                    "issuetype = Bug",
                    "summary ~ \"some text\" AND project in (FOO, BAR)"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        request_body = {
            'issueIds': issueIds,
            'jqls': jqls,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/match"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def parse_jql_queries(self, validation, queries) -> dict[str, Any]:
        """
        Parses a JQL query using the POST method at "/rest/api/3/jql/parse" and returns its abstract syntax tree, allowing for analysis or processing of JQL queries, with optional validation configuration.

        Args:
            validation (string): How to validate the JQL query and treat the validation results. Validation options include: * `strict` Returns all errors. If validation fails, the query structure is not returned. * `warn` Returns all errors. If validation fails but the JQL query is correctly formed, the query structure is returned. * `none` No validation is performed. If JQL query is correctly formed, the query structure is returned.
            queries (array): A list of queries to parse.
                Example:
                ```json
                {
                  "queries": [
                    "summary ~ test AND (labels in (urgent, blocker) OR lastCommentedBy = currentUser()) AND status CHANGED AFTER startOfMonth(-1M) ORDER BY updated DESC",
                    "issue.property[\"spaces here\"].value in (\"Service requests\", Incidents)",
                    "invalid query",
                    "summary = test",
                    "summary in test",
                    "project = INVALID",
                    "universe = 42"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL
        """
        request_body = {
            'queries': queries,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/parse"
        query_params = {k: v for k, v in [('validation', validation)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def migrate_queries(self, queryStrings=None) -> dict[str, Any]:
        """
        Converts JQL queries containing usernames or user keys to equivalent queries with account IDs, handling unknown users appropriately.

        Args:
            queryStrings (array): A list of queries with user identifiers. Maximum of 100 queries.
                Example:
                ```json
                {
                  "queryStrings": [
                    "assignee = mia",
                    "issuetype = Bug AND assignee in (mia) AND reporter in (alana) order by lastViewed DESC"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful. Note that the JQL queries are returned in the same order that they were passed.

        Tags:
            JQL
        """
        request_body = {
            'queryStrings': queryStrings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/pdcleaner"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def sanitise_jql_queries(self, queries) -> dict[str, Any]:
        """
        Sanitizes one or more JQL queries by converting readable details into IDs where a user lacks permission to view the entity, ensuring that unauthorized project names are replaced with project IDs.

        Args:
            queries (array): The list of JQL queries to sanitize. Must contain unique values. Maximum of 20 queries.
                Example:
                ```json
                {
                  "queries": [
                    {
                      "query": "project = 'Sample project'"
                    },
                    {
                      "accountId": "5b10ac8d82e05b22cc7d4ef5",
                      "query": "project = 'Sample project'"
                    },
                    {
                      "accountId": "cda2aa1395ac195d951b3387",
                      "query": "project = 'Sample project'"
                    },
                    {
                      "accountId": "5b10ac8d82e05b22cc7d4ef5",
                      "query": "invalid query"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            JQL
        """
        request_body = {
            'queries': queries,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/jql/sanitize"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_labels(self, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of labels starting from a specified index and limited by a maximum number of results using the Jira API.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Labels
        """
        url = f"{self.base_url}/rest/api/3/label"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_approximate_license_count(self) -> dict[str, Any]:
        """
        Retrieves the approximate user license count for a Jira instance, which may be cached for up to 7 days.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            License metrics
        """
        url = f"{self.base_url}/rest/api/3/license/approximateLicenseCount"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_approximate_application_license_count(self, applicationKey) -> dict[str, Any]:
        """
        Retrieves the approximate license count for a specific application in Jira Cloud using the provided application key.

        Args:
            applicationKey (string): applicationKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            License metrics
        """
        if applicationKey is None:
            raise ValueError("Missing required parameter 'applicationKey'")
        url = f"{self.base_url}/rest/api/3/license/approximateLicenseCount/product/{applicationKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_my_permissions(self, projectKey=None, projectId=None, issueKey=None, issueId=None, permissions=None, projectUuid=None, projectConfigurationUuid=None, commentId=None) -> dict[str, Any]:
        """
        Retrieves the current user's permissions in Jira, optionally filtered by project, issue, or specific permission keys, and indicates whether each permission is granted.

        Args:
            projectKey (string): The key of project. Ignored if `projectId` is provided.
            projectId (string): The ID of project.
            issueKey (string): The key of the issue. Ignored if `issueId` is provided.
            issueId (string): The ID of the issue.
            permissions (string): A list of permission keys. (Required) This parameter accepts a comma-separated list. To get the list of available permissions, use [Get all permissions](#api-rest-api-3-permissions-get). Example: 'BROWSE_PROJECTS,EDIT_ISSUES'.
            projectUuid (string): Specifies the UUID of the project to check permissions for.
            projectConfigurationUuid (string): A UUID identifying the specific project configuration to check permissions against.
            commentId (string): The ID of the comment.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permissions
        """
        url = f"{self.base_url}/rest/api/3/mypermissions"
        query_params = {k: v for k, v in [('projectKey', projectKey), ('projectId', projectId), ('issueKey', issueKey), ('issueId', issueId), ('permissions', permissions), ('projectUuid', projectUuid), ('projectConfigurationUuid', projectConfigurationUuid), ('commentId', commentId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_preference(self, key) -> Any:
        """
        Deletes a user's Jira preference specified by the key query parameter and returns a 204 status code on success.

        Args:
            key (string): The key of the preference.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Myself
        """
        url = f"{self.base_url}/rest/api/3/mypreferences"
        query_params = {k: v for k, v in [('key', key)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_preference(self, key) -> Any:
        """
        Retrieves the specified user preference value for the currently authenticated user using the provided key parameter.

        Args:
            key (string): The key of the preference.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Myself
        """
        url = f"{self.base_url}/rest/api/3/mypreferences"
        query_params = {k: v for k, v in [('key', key)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def delete_locale(self) -> Any:
        """
        Deletes the locale preference for a user, restoring the default locale setting, using the Jira Cloud platform REST API.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Myself
        """
        url = f"{self.base_url}/rest/api/3/mypreferences/locale"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_locale(self) -> dict[str, Any]:
        """
        Retrieves the locale preference for the currently authenticated user in Jira using the GET method.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Myself
        """
        url = f"{self.base_url}/rest/api/3/mypreferences/locale"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_locale(self, locale=None) -> Any:
        """
        Updates the user's locale preference in Jira, restoring the default if no value is specified (deprecated, use user management API instead).

        Args:
            locale (string): The locale code. The Java the locale format is used: a two character language code (ISO 639), an underscore, and two letter country code (ISO 3166). For example, en\_US represents a locale of English (United States). Required on create.
                Example:
                ```json
                {
                  "locale": "en_US"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Myself
        """
        request_body = {
            'locale': locale,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/mypreferences/locale"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_current_user(self, expand=None) -> dict[str, Any]:
        """
        Retrieves the authenticated user's profile details (with privacy-based limitations on sensitive fields) from Jira Cloud.

        Args:
            expand (string): Use [expand](#expansion) to include additional information about user in the response. This parameter accepts a comma-separated list. Expand options include: * `groups` Returns all groups, including nested groups, the user belongs to. * `applicationRoles` Returns the application roles the user is assigned to.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Myself
        """
        url = f"{self.base_url}/rest/api/3/myself"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_notification_schemes(self, startAt=None, maxResults=None, id=None, projectId=None, onlyDefault=None, expand=None) -> dict[str, Any]:
        """
        Retrieves notification schemes listing configured events and their notification recipients for Jira issues, supporting filtering by project, ID, and pagination.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of notification schemes IDs to be filtered by
            projectId (array): The list of projects IDs to be filtered by
            onlyDefault (boolean): When set to true, returns only the default notification scheme. If you provide project IDs not associated with the default, returns an empty page. The default value is false.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `all` Returns all expandable information * `field` Returns information about any custom fields assigned to receive an event * `group` Returns information about any groups assigned to receive an event * `notificationSchemeEvents` Returns a list of event associations. This list is returned for all expandable information * `projectRole` Returns information about any project roles assigned to receive an event * `user` Returns information about any users assigned to receive an event

        Returns:
            dict[str, Any]: Returned if the request is successful. Only returns notification schemes that the user has permission to access. An empty list is returned if the user lacks permission to access all notification schemes.

        Tags:
            Issue notification schemes
        """
        url = f"{self.base_url}/rest/api/3/notificationscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('projectId', projectId), ('onlyDefault', onlyDefault), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_notification_scheme(self, name, description=None, notificationSchemeEvents=None) -> dict[str, Any]:
        """
        Creates a new notification scheme using the "POST" method at the "/rest/api/3/notificationscheme" endpoint, returning a successful creation response when the operation is completed.

        Args:
            name (string): The name of the notification scheme. Must be unique (case-insensitive).
            description (string): The description of the notification scheme.
            notificationSchemeEvents (array): The list of notifications which should be added to the notification scheme.
                Example:
                ```json
                {
                  "description": "My new scheme description",
                  "name": "My new notification scheme",
                  "notificationSchemeEvents": [
                    {
                      "event": {
                        "id": "1"
                      },
                      "notifications": [
                        {
                          "notificationType": "Group",
                          "parameter": "jira-administrators"
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        request_body = {
            'description': description,
            'name': name,
            'notificationSchemeEvents': notificationSchemeEvents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/notificationscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_notification_scheme_to_project_mappings(self, startAt=None, maxResults=None, notificationSchemeId=None, projectId=None) -> dict[str, Any]:
        """
        Retrieves the association between notification schemes and projects in Jira, including scheme IDs and project IDs, based on query parameters such as notificationSchemeId and projectId.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            notificationSchemeId (array): The list of notifications scheme IDs to be filtered out
            projectId (array): The list of project IDs to be filtered out

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        url = f"{self.base_url}/rest/api/3/notificationscheme/project"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('notificationSchemeId', notificationSchemeId), ('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_notification_scheme(self, id, expand=None) -> dict[str, Any]:
        """
        Retrieves details of a specific notification scheme by its ID using the Jira API, optionally expanding the response with additional details.

        Args:
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `all` Returns all expandable information * `field` Returns information about any custom fields assigned to receive an event * `group` Returns information about any groups assigned to receive an event * `notificationSchemeEvents` Returns a list of event associations. This list is returned for all expandable information * `projectRole` Returns information about any project roles assigned to receive an event * `user` Returns information about any users assigned to receive an event

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/notificationscheme/{id}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_notification_scheme(self, id, description=None, name=None) -> Any:
        """
        Updates a notification scheme using its ID, allowing modifications to the scheme's configuration, such as events and recipients.

        Args:
            id (string): id
            description (string): The description of the notification scheme.
            name (string): The name of the notification scheme. Must be unique.
                Example:
                ```json
                {
                  "description": "My updated notification scheme description",
                  "name": "My updated notification scheme"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/notificationscheme/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_notifications(self, id, notificationSchemeEvents) -> Any:
        """
        Updates notifications for a specific notification scheme in Jira by adding or modifying event-based notification rules.

        Args:
            id (string): id
            notificationSchemeEvents (array): The list of notifications which should be added to the notification scheme.
                Example:
                ```json
                {
                  "notificationSchemeEvents": [
                    {
                      "event": {
                        "id": "1"
                      },
                      "notifications": [
                        {
                          "notificationType": "Group",
                          "parameter": "jira-administrators"
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'notificationSchemeEvents': notificationSchemeEvents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/notificationscheme/{id}/notification"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_notification_scheme(self, notificationSchemeId) -> Any:
        """
        Deletes a specific notification scheme in Jira using its ID, returning appropriate status codes for success or error conditions.

        Args:
            notificationSchemeId (string): notificationSchemeId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        if notificationSchemeId is None:
            raise ValueError("Missing required parameter 'notificationSchemeId'")
        url = f"{self.base_url}/rest/api/3/notificationscheme/{notificationSchemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_notification_from_notification_scheme(self, notificationSchemeId, notificationId) -> Any:
        """
        Deletes a specific notification from a notification scheme in Jira using the specified notification scheme and notification IDs.

        Args:
            notificationSchemeId (string): notificationSchemeId
            notificationId (string): notificationId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue notification schemes
        """
        if notificationSchemeId is None:
            raise ValueError("Missing required parameter 'notificationSchemeId'")
        if notificationId is None:
            raise ValueError("Missing required parameter 'notificationId'")
        url = f"{self.base_url}/rest/api/3/notificationscheme/{notificationSchemeId}/notification/{notificationId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_permissions(self) -> dict[str, Any]:
        """
        Retrieves details of global and project permissions granted to a user using the Jira Cloud REST API.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permissions
        """
        url = f"{self.base_url}/rest/api/3/permissions"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_bulk_permissions(self, accountId=None, globalPermissions=None, projectPermissions=None) -> dict[str, Any]:
        """
        Checks user permissions in Jira projects and returns global and project-specific permission details.

        Args:
            accountId (string): The account ID of a user.
            globalPermissions (array): Global permissions to look up.
            projectPermissions (array): Project permissions with associated projects and issues to look up.
                Example:
                ```json
                {
                  "accountId": "5b10a2844c20165700ede21g",
                  "globalPermissions": [
                    "ADMINISTER"
                  ],
                  "projectPermissions": [
                    {
                      "issues": [
                        10010,
                        10011,
                        10012,
                        10013,
                        10014
                      ],
                      "permissions": [
                        "EDIT_ISSUES"
                      ],
                      "projects": [
                        10001
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permissions
        """
        request_body = {
            'accountId': accountId,
            'globalPermissions': globalPermissions,
            'projectPermissions': projectPermissions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/permissions/check"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_permitted_projects(self, permissions) -> dict[str, Any]:
        """
        Retrieves all projects where a user has specified project permissions and returns the list of projects with granted access.

        Args:
            permissions (array): A list of permission keys.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permissions
        """
        request_body = {
            'permissions': permissions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/permissions/project"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_permission_schemes(self, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of all permission schemes in Jira Cloud, optionally expanding the response to include additional details such as groups by using the "expand" query parameter.

        Args:
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permission schemes
        """
        url = f"{self.base_url}/rest/api/3/permissionscheme"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_permission_scheme(self, name, expand=None, description=None, expand_body=None, id=None, permissions=None, scope=None, self_arg_body=None) -> dict[str, Any]:
        """
        Creates a new permission scheme in Jira using the "POST" method at the "/rest/api/3/permissionscheme" path, allowing for the definition of a permission set with various grants.

        Args:
            name (string): The name of the permission scheme. Must be unique.
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are always included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.
            description (string): A description for the permission scheme.
            expand_body (string): The expand options available for the permission scheme.
            id (integer): The ID of the permission scheme.
            permissions (array): The permission scheme to create or update. See [About permission schemes and grants](../api-group-permission-schemes/#about-permission-schemes-and-grants) for more information.
            scope (string): The scope of the permission scheme.
            self_arg_body (string): The URL of the permission scheme.
                Example:
                ```json
                {
                  "description": "description",
                  "name": "Example permission scheme",
                  "permissions": [
                    {
                      "holder": {
                        "parameter": "jira-core-users",
                        "type": "group",
                        "value": "ca85fac0-d974-40ca-a615-7af99c48d24f"
                      },
                      "permission": "ADMINISTER_PROJECTS"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the permission scheme is created.

        Tags:
            Permission schemes
        """
        request_body = {
            'description': description,
            'expand': expand_body,
            'id': id,
            'name': name,
            'permissions': permissions,
            'scope': scope,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/permissionscheme"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_permission_scheme(self, schemeId) -> Any:
        """
        Deletes a permission scheme specified by the provided `schemeId` using the Jira REST API, removing it from the system.

        Args:
            schemeId (string): schemeId

        Returns:
            Any: Returned if the permission scheme is deleted.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_permission_scheme(self, schemeId, expand=None) -> dict[str, Any]:
        """
        Retrieves a specific permission scheme in Jira, identified by its scheme ID, and optionally expands its details with certain information based on the provided expand parameter.

        Args:
            schemeId (string): schemeId
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_permission_scheme(self, schemeId, name, expand=None, description=None, expand_body=None, id=None, permissions=None, scope=None, self_arg_body=None) -> dict[str, Any]:
        """
        Updates a permission scheme identified by `{schemeId}` using the PUT method, allowing modifications to its permissions and settings.

        Args:
            schemeId (string): schemeId
            name (string): The name of the permission scheme. Must be unique.
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are always included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.
            description (string): A description for the permission scheme.
            expand_body (string): The expand options available for the permission scheme.
            id (integer): The ID of the permission scheme.
            permissions (array): The permission scheme to create or update. See [About permission schemes and grants](../api-group-permission-schemes/#about-permission-schemes-and-grants) for more information.
            scope (string): The scope of the permission scheme.
            self_arg_body (string): The URL of the permission scheme.
                Example:
                ```json
                {
                  "description": "description",
                  "name": "Example permission scheme",
                  "permissions": [
                    {
                      "holder": {
                        "parameter": "jira-core-users",
                        "type": "group",
                        "value": "ca85fac0-d974-40ca-a615-7af99c48d24f"
                      },
                      "permission": "ADMINISTER_PROJECTS"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the scheme is updated.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        request_body = {
            'description': description,
            'expand': expand_body,
            'id': id,
            'name': name,
            'permissions': permissions,
            'scope': scope,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_permission_scheme_grants(self, schemeId, expand=None) -> dict[str, Any]:
        """
        Retrieves the permissions granted by a specific permission scheme in Jira, including details about each permission grant within the scheme.

        Args:
            schemeId (string): schemeId
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are always included when you specify any value. Expand options include: * `permissions` Returns all permission grants for each permission scheme. * `user` Returns information about the user who is granted the permission. * `group` Returns information about the group that is granted the permission. * `projectRole` Returns information about the project role granted the permission. * `field` Returns information about the custom field granted the permission. * `all` Returns all expandable information.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}/permission"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_permission_grant(self, schemeId, expand=None, holder=None, id=None, permission=None, self_arg_body=None) -> dict[str, Any]:
        """
        Adds permissions to a specific permission scheme in Jira, enabling access control configuration for users, groups, or roles.

        Args:
            schemeId (string): schemeId
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are always included when you specify any value. Expand options include: * `permissions` Returns all permission grants for each permission scheme. * `user` Returns information about the user who is granted the permission. * `group` Returns information about the group that is granted the permission. * `projectRole` Returns information about the project role granted the permission. * `field` Returns information about the custom field granted the permission. * `all` Returns all expandable information.
            holder (string): The user or group being granted the permission. It consists of a `type`, a type-dependent `parameter` and a type-dependent `value`. See [Holder object](../api-group-permission-schemes/#holder-object) in *Get all permission schemes* for more information.
            id (integer): The ID of the permission granted details.
            permission (string): The permission to grant. This permission can be one of the built-in permissions or a custom permission added by an app. See [Built-in permissions](../api-group-permission-schemes/#built-in-permissions) in *Get all permission schemes* for more information about the built-in permissions. See the [project permission](https://developer.atlassian.com/cloud/jira/platform/modules/project-permission/) and [global permission](https://developer.atlassian.com/cloud/jira/platform/modules/global-permission/) module documentation for more information about custom permissions.
            self_arg_body (string): The URL of the permission granted details.
                Example:
                ```json
                {
                  "holder": {
                    "parameter": "jira-core-users",
                    "type": "group",
                    "value": "ca85fac0-d974-40ca-a615-7af99c48d24f"
                  },
                  "permission": "ADMINISTER_PROJECTS"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the scheme permission is created.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        request_body = {
            'holder': holder,
            'id': id,
            'permission': permission,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}/permission"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_permission_scheme_entity(self, schemeId, permissionId) -> Any:
        """
        Deletes a permission grant from a permission scheme in Jira using the specified `schemeId` and `permissionId`.

        Args:
            schemeId (string): schemeId
            permissionId (string): permissionId

        Returns:
            Any: Returned if the permission grant is deleted.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if permissionId is None:
            raise ValueError("Missing required parameter 'permissionId'")
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_permission_scheme_grant(self, schemeId, permissionId, expand=None) -> dict[str, Any]:
        """
        Retrieves a specific permission grant's details within a Jira permission scheme identified by the scheme ID and permission ID.

        Args:
            schemeId (string): schemeId
            permissionId (string): permissionId
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are always included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Permission schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        if permissionId is None:
            raise ValueError("Missing required parameter 'permissionId'")
        url = f"{self.base_url}/rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_plans(self, includeTrashed=None, includeArchived=None, cursor=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves plan details using pagination and optional filters for trashed or archived items.

        Args:
            includeTrashed (boolean): Whether to include trashed plans in the results.
            includeArchived (boolean): Whether to include archived plans in the results.
            cursor (string): The cursor to start from. If not provided, the first page will be returned.
            maxResults (integer): The maximum number of plans to return per page. The maximum value is 50. The default value is 50.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Plans
        """
        url = f"{self.base_url}/rest/api/3/plans/plan"
        query_params = {k: v for k, v in [('includeTrashed', includeTrashed), ('includeArchived', includeArchived), ('cursor', cursor), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_plan(self, issueSources, name, scheduling, useGroupId=None, crossProjectReleases=None, customFields=None, exclusionRules=None, leadAccountId=None, permissions=None) -> Any:
        """
        Creates a new plan resource via the specified endpoint, requiring a request body with plan details and supporting optional useGroupId query parameter for group association.

        Args:
            issueSources (array): The issue sources to include in the plan.
            name (string): The plan name.
            scheduling (string): The scheduling settings for the plan.
            useGroupId (boolean): Whether to accept group IDs instead of group names. Group names are deprecated.
            crossProjectReleases (array): The cross-project releases to include in the plan.
            customFields (array): The custom fields for the plan.
            exclusionRules (string): The exclusion rules for the plan.
            leadAccountId (string): The account ID of the plan lead.
            permissions (array): The permissions for the plan.
                Example:
                ```json
                {
                  "crossProjectReleases": [
                    {
                      "name": "AB and BC merge",
                      "releaseIds": [
                        29,
                        39
                      ]
                    }
                  ],
                  "customFields": [
                    {
                      "customFieldId": 2335,
                      "filter": true
                    }
                  ],
                  "exclusionRules": {
                    "issueIds": [
                      2,
                      3
                    ],
                    "issueTypeIds": [
                      32,
                      33
                    ],
                    "numberOfDaysToShowCompletedIssues": 50,
                    "releaseIds": [
                      42,
                      43
                    ],
                    "workStatusCategoryIds": [
                      22,
                      23
                    ],
                    "workStatusIds": [
                      12,
                      13
                    ]
                  },
                  "issueSources": [
                    {
                      "type": "Project",
                      "value": 12
                    },
                    {
                      "type": "Board",
                      "value": 462
                    }
                  ],
                  "leadAccountId": "abc-12-rbji",
                  "name": "ABC Quaterly plan",
                  "permissions": [
                    {
                      "holder": {
                        "type": "AccountId",
                        "value": "234-tgj-343"
                      },
                      "type": "Edit"
                    }
                  ],
                  "scheduling": {
                    "dependencies": "Sequential",
                    "endDate": {
                      "type": "DueDate"
                    },
                    "estimation": "Days",
                    "inferredDates": "ReleaseDates",
                    "startDate": {
                      "type": "TargetStartDate"
                    }
                  }
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Plans
        """
        request_body = {
            'crossProjectReleases': crossProjectReleases,
            'customFields': customFields,
            'exclusionRules': exclusionRules,
            'issueSources': issueSources,
            'leadAccountId': leadAccountId,
            'name': name,
            'permissions': permissions,
            'scheduling': scheduling,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/plans/plan"
        query_params = {k: v for k, v in [('useGroupId', useGroupId)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_plan(self, planId, useGroupId=None) -> dict[str, Any]:
        """
        Retrieves the details of a specific plan identified by its planId using a GET request.

        Args:
            planId (string): planId
            useGroupId (boolean): Whether to return group IDs instead of group names. Group names are deprecated.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Plans
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}"
        query_params = {k: v for k, v in [('useGroupId', useGroupId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def archive_plan(self, planId) -> Any:
        """
        Archives a specific plan in Jira using the PUT method at the "/rest/api/3/plans/plan/{planId}/archive" endpoint, identified by the planId parameter.

        Args:
            planId (string): planId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Plans
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/archive"
        query_params = {}
        response = self._put(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def duplicate_plan(self, planId, name) -> Any:
        """
        Creates a duplicate of the specified Jira plan using the provided plan ID and returns the new plan's details.

        Args:
            planId (string): planId
            name (string): The plan name.
                Example:
                ```json
                {
                  "name": "Copied Plan"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Plans
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        request_body = {
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/duplicate"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_teams(self, planId, cursor=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of teams associated with a specific plan in Jira Cloud.

        Args:
            planId (string): planId
            cursor (string): The cursor to start from. If not provided, the first page will be returned.
            maxResults (integer): The maximum number of plan teams to return per page. The maximum value is 50. The default value is 50.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team"
        query_params = {k: v for k, v in [('cursor', cursor), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_atlassian_team(self, planId, id, planningStyle, capacity=None, issueSourceId=None, sprintLength=None) -> Any:
        """
        Adds an Atlassian team to a plan using the Jira Cloud API and returns a status message, allowing for the management of team configurations within plans.

        Args:
            planId (string): planId
            id (string): The Atlassian team ID.
            planningStyle (string): The planning style for the Atlassian team. This must be "Scrum" or "Kanban".
            capacity (number): The capacity for the Atlassian team.
            issueSourceId (integer): The ID of the issue source for the Atlassian team.
            sprintLength (integer): The sprint length for the Atlassian team.
                Example:
                ```json
                {
                  "capacity": 200,
                  "id": "AtlassianTeamId",
                  "issueSourceId": 0,
                  "planningStyle": "Scrum",
                  "sprintLength": 2
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        request_body = {
            'capacity': capacity,
            'id': id,
            'issueSourceId': issueSourceId,
            'planningStyle': planningStyle,
            'sprintLength': sprintLength,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/atlassian"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_atlassian_team(self, planId, atlassianTeamId) -> Any:
        """
        Deletes an Atlassian team from a specified plan in Jira Cloud using the "DELETE" method, requiring plan ID and Atlassian team ID as path parameters.

        Args:
            planId (string): planId
            atlassianTeamId (string): atlassianTeamId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        if atlassianTeamId is None:
            raise ValueError("Missing required parameter 'atlassianTeamId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_atlassian_team(self, planId, atlassianTeamId) -> dict[str, Any]:
        """
        Retrieves planning settings for an Atlassian team within a specific plan in Jira.

        Args:
            planId (string): planId
            atlassianTeamId (string): atlassianTeamId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        if atlassianTeamId is None:
            raise ValueError("Missing required parameter 'atlassianTeamId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/atlassian/{atlassianTeamId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def create_plan_only_team(self, planId, name, planningStyle, capacity=None, issueSourceId=None, memberAccountIds=None, sprintLength=None) -> Any:
        """
        Creates a plan-only team in a Jira Cloud plan with specified planning settings and returns the configuration.

        Args:
            planId (string): planId
            name (string): The plan-only team name.
            planningStyle (string): The planning style for the plan-only team. This must be "Scrum" or "Kanban".
            capacity (number): The capacity for the plan-only team.
            issueSourceId (integer): The ID of the issue source for the plan-only team.
            memberAccountIds (array): The account IDs of the plan-only team members.
            sprintLength (integer): The sprint length for the plan-only team.
                Example:
                ```json
                {
                  "capacity": 200,
                  "issueSourceId": 0,
                  "memberAccountIds": [
                    "member1AccountId",
                    "member2AccountId"
                  ],
                  "name": "Team1",
                  "planningStyle": "Scrum",
                  "sprintLength": 2
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        request_body = {
            'capacity': capacity,
            'issueSourceId': issueSourceId,
            'memberAccountIds': memberAccountIds,
            'name': name,
            'planningStyle': planningStyle,
            'sprintLength': sprintLength,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/planonly"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_plan_only_team(self, planId, planOnlyTeamId) -> Any:
        """
        Deletes a specific team associated with a plan in a REST API (likely related to project management or issue tracking).

        Args:
            planId (string): planId
            planOnlyTeamId (string): planOnlyTeamId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        if planOnlyTeamId is None:
            raise ValueError("Missing required parameter 'planOnlyTeamId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_plan_only_team(self, planId, planOnlyTeamId) -> dict[str, Any]:
        """
        Retrieves planning settings for a specific plan-only team in a Jira plan using the Jira Cloud REST API.

        Args:
            planId (string): planId
            planOnlyTeamId (string): planOnlyTeamId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Teams in plan
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        if planOnlyTeamId is None:
            raise ValueError("Missing required parameter 'planOnlyTeamId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/team/planonly/{planOnlyTeamId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()



    def trash_plan(self, planId) -> Any:
        """
        Moves a specified plan to trash using the Jira API and returns an empty response on success.

        Args:
            planId (string): planId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Plans
        """
        if planId is None:
            raise ValueError("Missing required parameter 'planId'")
        url = f"{self.base_url}/rest/api/3/plans/plan/{planId}/trash"
        query_params = {}
        response = self._put(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_priorities(self) -> list[Any]:
        """
        Retrieves a list of all issue priorities in Jira using the "/rest/api/3/priority" endpoint with the GET method.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        url = f"{self.base_url}/rest/api/3/priority"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_priority(self, name, statusColor, avatarId=None, description=None, iconUrl=None) -> dict[str, Any]:
        """
        Creates a new priority in Jira with specified properties and returns the generated ID.

        Args:
            name (string): The name of the priority. Must be unique.
            statusColor (string): The status color of the priority in 3-digit or 6-digit hexadecimal format.
            avatarId (integer): The ID for the avatar for the priority. Either the iconUrl or avatarId must be defined, but not both. This parameter is nullable and will become mandatory once the iconUrl parameter is deprecated.
            description (string): The description of the priority.
            iconUrl (string): The URL of an icon for the priority. Accepted protocols are HTTP and HTTPS. Built in icons can also be used. Either the iconUrl or avatarId must be defined, but not both.
                Example:
                ```json
                {
                  "description": "My priority description",
                  "iconUrl": "images/icons/priorities/major.png",
                  "name": "My new priority",
                  "statusColor": "#ABCDEF"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        request_body = {
            'avatarId': avatarId,
            'description': description,
            'iconUrl': iconUrl,
            'name': name,
            'statusColor': statusColor,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priority"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_default_priority(self, id) -> Any:
        """
        Sets the default issue priority in Jira using the PUT method at the "/rest/api/3/priority/default" path.

        Args:
            id (string): The ID of the new default issue priority. Must be an existing ID or null. Setting this to null erases the default priority setting.
                Example:
                ```json
                {
                  "id": "3"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        request_body = {
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priority/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def move_priorities(self, ids, after=None, position=None) -> Any:
        """
        Reorders the priority of issues in Jira by updating their sequence using a PUT request.

        Args:
            ids (array): The list of issue IDs to be reordered. Cannot contain duplicates nor after ID.
            after (string): The ID of the priority. Required if `position` isn't provided.
            position (string): The position for issue priorities to be moved to. Required if `after` isn't provided.
                Example:
                ```json
                {
                  "after": "10003",
                  "ids": [
                    "10004",
                    "10005"
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        request_body = {
            'after': after,
            'ids': ids,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priority/move"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_priorities(self, startAt=None, maxResults=None, id=None, projectId=None, priorityName=None, onlyDefault=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of priorities from Jira using the GET method at "/rest/api/3/priority/search", allowing for customizable queries with parameters like start index, maximum results, ID, project ID, priority name, and expansion options.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of priority IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=2&id=3`.
            projectId (array): The list of projects IDs. To include multiple IDs, provide an ampersand-separated list. For example, `projectId=10010&projectId=10111`.
            priorityName (string): The name of priority to search for.
            onlyDefault (boolean): Whether only the default priority is returned.
            expand (string): Use `schemes` to return the associated priority schemes for each priority. Limited to returning first 15 priority schemes per priority.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        url = f"{self.base_url}/rest/api/3/priority/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('projectId', projectId), ('priorityName', priorityName), ('onlyDefault', onlyDefault), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_priority(self, id) -> Any:
        """
        Deletes an issue priority asynchronously by its ID using the Jira Cloud REST API, requiring administrative permissions and returning various status messages based on the outcome.

        Args:
            id (string): id

        Returns:
            Any: API response data.

        Tags:
            Issue priorities
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/priority/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_priority(self, id) -> dict[str, Any]:
        """
        Retrieves details of a specific issue priority by its ID in Jira.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/priority/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_priority(self, id, avatarId=None, description=None, iconUrl=None, name=None, statusColor=None) -> Any:
        """
        Updates an issue priority with the specified ID using the Jira Cloud API, allowing modifications to priority details such as name or icon URL.

        Args:
            id (string): id
            avatarId (integer): The ID for the avatar for the priority. This parameter is nullable and both iconUrl and avatarId cannot be defined.
            description (string): The description of the priority.
            iconUrl (string): The URL of an icon for the priority. Accepted protocols are HTTP and HTTPS. Built in icons can also be used. Both iconUrl and avatarId cannot be defined.
            name (string): The name of the priority. Must be unique.
            statusColor (string): The status color of the priority in 3-digit or 6-digit hexadecimal format.
                Example:
                ```json
                {
                  "description": "My updated priority description",
                  "iconUrl": "images/icons/priorities/minor.png",
                  "name": "My updated priority",
                  "statusColor": "#123456"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue priorities
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'avatarId': avatarId,
            'description': description,
            'iconUrl': iconUrl,
            'name': name,
            'statusColor': statusColor,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priority/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_priority_schemes(self, startAt=None, maxResults=None, priorityId=None, schemeId=None, schemeName=None, onlyDefault=None, orderBy=None, expand=None) -> dict[str, Any]:
        """
        Retrieves priority schemes and their associated priorities from a Jira instance using various filters such as priority ID, scheme ID, scheme name, and more.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            priorityId (array): A set of priority IDs to filter by. To include multiple IDs, provide an ampersand-separated list. For example, `priorityId=10000&priorityId=10001`.
            schemeId (array): A set of priority scheme IDs. To include multiple IDs, provide an ampersand-separated list. For example, `schemeId=10000&schemeId=10001`.
            schemeName (string): The name of scheme to search for.
            onlyDefault (boolean): Whether only the default priority is returned.
            orderBy (string): The ordering to return the priority schemes by.
            expand (string): A comma separated list of additional information to return. "priorities" will return priorities associated with the priority scheme. "projects" will return projects associated with the priority scheme. `expand=priorities,projects`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        url = f"{self.base_url}/rest/api/3/priorityscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('priorityId', priorityId), ('schemeId', schemeId), ('schemeName', schemeName), ('onlyDefault', onlyDefault), ('orderBy', orderBy), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_priority_scheme(self, defaultPriorityId, name, priorityIds, description=None, mappings=None, projectIds=None) -> dict[str, Any]:
        """
        Creates a new priority scheme with configurable priority mappings and project associations in Jira.

        Args:
            defaultPriorityId (integer): The ID of the default priority for the priority scheme.
            name (string): The name of the priority scheme. Must be unique.
            priorityIds (array): The IDs of priorities in the scheme.
            description (string): The description of the priority scheme.
            mappings (string): Instructions to migrate the priorities of issues.

        `in` mappings are used to migrate the priorities of issues to priorities used within the priority scheme.

        `out` mappings are used to migrate the priorities of issues to priorities not used within the priority scheme.

         *  When **priorities** are **added** to the new priority scheme, no mapping needs to be provided as the new priorities are not used by any issues.
         *  When **priorities** are **removed** from the new priority scheme, no mapping needs to be provided as the removed priorities are not used by any issues.
         *  When **projects** are **added** to the priority scheme, the priorities of issues in those projects might need to be migrated to new priorities used by the priority scheme. This can occur when the current scheme does not use all the priorities in the project(s)' priority scheme(s).
    
             *  An `in` mapping must be provided for each of these priorities.
         *  When **projects** are **removed** from the priority scheme, no mapping needs to be provided as the removed projects are not using the priorities of the new priority scheme.

        For more information on `in` and `out` mappings, see the child properties documentation for the `PriorityMapping` object below.
            projectIds (array): The IDs of projects that will use the priority scheme.
                Example:
                ```json
                {
                  "defaultPriorityId": 10001,
                  "description": "My priority scheme description",
                  "mappings": {
                    "in": {
                      "10002": 10000,
                      "10005": 10001,
                      "10006": 10001,
                      "10008": 10003
                    },
                    "out": {}
                  },
                  "name": "My new priority scheme",
                  "priorityIds": [
                    10000,
                    10001,
                    10003
                  ],
                  "projectIds": [
                    10005,
                    10006,
                    10007
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is completed.

        Tags:
            Priority schemes
        """
        request_body = {
            'defaultPriorityId': defaultPriorityId,
            'description': description,
            'mappings': mappings,
            'name': name,
            'priorityIds': priorityIds,
            'projectIds': projectIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priorityscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def suggested_priorities_for_mappings(self, maxResults=None, priorities=None, projects=None, schemeId=None, startAt=None) -> dict[str, Any]:
        """
        Submits priority mappings for a scheme and returns the updated configuration upon completion.

        Args:
            maxResults (integer): The maximum number of results that could be on the page.
            priorities (string): The priority changes in the scheme.
            projects (string): The project changes in the scheme.
            schemeId (integer): The id of the priority scheme.
            startAt (integer): The index of the first item returned on the page.
                Example:
                ```json
                {
                  "maxResults": 50,
                  "priorities": {
                    "add": [
                      10001,
                      10002
                    ],
                    "remove": [
                      10003
                    ]
                  },
                  "projects": {
                    "add": [
                      10021
                    ]
                  },
                  "schemeId": 10005,
                  "startAt": 0
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        request_body = {
            'maxResults': maxResults,
            'priorities': priorities,
            'projects': projects,
            'schemeId': schemeId,
            'startAt': startAt,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priorityscheme/mappings"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_available_priorities_by_priority_scheme(self, schemeId, startAt=None, maxResults=None, query=None, exclude=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of available priorities for a specified priority scheme or across all schemes, supporting filtering by query and exclusion criteria.

        Args:
            schemeId (string): The priority scheme ID.
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            query (string): The string to query priorities on by name.
            exclude (array): A list of priority IDs to exclude from the results.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        url = f"{self.base_url}/rest/api/3/priorityscheme/priorities/available"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('query', query), ('schemeId', schemeId), ('exclude', exclude)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_priority_scheme(self, schemeId) -> Any:
        """
        Deletes a specific priority scheme identified by its scheme ID, causing projects that were using it to default to the standard priority scheme.

        Args:
            schemeId (string): schemeId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/priorityscheme/{schemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_priority_scheme(self, schemeId, defaultPriorityId=None, description=None, mappings=None, name=None, priorities=None, projects=None) -> dict[str, Any]:
        """
        Updates a Jira priority scheme configuration with the given ID, rejecting updates if they would require issue migrations.

        Args:
            schemeId (string): schemeId
            defaultPriorityId (integer): The default priority of the scheme.
            description (string): The description of the priority scheme.
            mappings (string): Instructions to migrate the priorities of issues.

        `in` mappings are used to migrate the priorities of issues to priorities used within the priority scheme.

        `out` mappings are used to migrate the priorities of issues to priorities not used within the priority scheme.

         *  When **priorities** are **added** to the priority scheme, no mapping needs to be provided as the new priorities are not used by any issues.
         *  When **priorities** are **removed** from the priority scheme, issues that are using those priorities must be migrated to new priorities used by the priority scheme.
    
             *  An `in` mapping must be provided for each of these priorities.
         *  When **projects** are **added** to the priority scheme, the priorities of issues in those projects might need to be migrated to new priorities used by the priority scheme. This can occur when the current scheme does not use all the priorities in the project(s)' priority scheme(s).
    
             *  An `in` mapping must be provided for each of these priorities.
         *  When **projects** are **removed** from the priority scheme, the priorities of issues in those projects might need to be migrated to new priorities within the **Default Priority Scheme** that are not used by the priority scheme. This can occur when the **Default Priority Scheme** does not use all the priorities within the current scheme.
    
             *  An `out` mapping must be provided for each of these priorities.

        For more information on `in` and `out` mappings, see the child properties documentation for the `PriorityMapping` object below.
            name (string): The name of the priority scheme. Must be unique.
            priorities (string): The priorities in the scheme.
            projects (string): The projects in the scheme.
                Example:
                ```json
                {
                  "defaultPriorityId": 10001,
                  "description": "My priority scheme description",
                  "mappings": {
                    "in": {
                      "10003": 10002,
                      "10004": 10001
                    },
                    "out": {
                      "10001": 10005,
                      "10002": 10006
                    }
                  },
                  "name": "My new priority scheme",
                  "priorities": {
                    "add": {
                      "ids": [
                        10001,
                        10002
                      ]
                    },
                    "remove": {
                      "ids": [
                        10003,
                        10004
                      ]
                    }
                  },
                  "projects": {
                    "add": {
                      "ids": [
                        10101,
                        10102
                      ]
                    },
                    "remove": {
                      "ids": [
                        10103,
                        10104
                      ]
                    }
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is accepted.

        Tags:
            Priority schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        request_body = {
            'defaultPriorityId': defaultPriorityId,
            'description': description,
            'mappings': mappings,
            'name': name,
            'priorities': priorities,
            'projects': projects,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/priorityscheme/{schemeId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_priorities_by_priority_scheme(self, schemeId, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of priorities associated with a specific priority scheme in Jira, supporting startAt and maxResults parameters.

        Args:
            schemeId (string): schemeId
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/priorityscheme/{schemeId}/priorities"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_projects_by_priority_scheme(self, schemeId, startAt=None, maxResults=None, projectId=None, query=None) -> dict[str, Any]:
        """
        Retrieves a list of projects associated with a specific priority scheme in Jira.

        Args:
            schemeId (string): schemeId
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            projectId (array): The project IDs to filter by. For example, `projectId=10000&projectId=10001`.
            query (string): The string to query projects on by name.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Priority schemes
        """
        if schemeId is None:
            raise ValueError("Missing required parameter 'schemeId'")
        url = f"{self.base_url}/rest/api/3/priorityscheme/{schemeId}/projects"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('projectId', projectId), ('query', query)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_projects(self, expand=None, recent=None, properties=None) -> list[Any]:
        """
        Retrieves project details from Jira with optional parameters to expand properties, limit to recent projects, or include specific properties.

        Args:
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expanded options include: * `description` Returns the project description. * `issueTypes` Returns all issue types associated with the project. * `lead` Returns information about the project lead. * `projectKeys` Returns all project keys associated with the project.
            recent (integer): Returns the user's most recently accessed projects. You may specify the number of results to return up to a maximum of 20. If access is anonymous, then the recently accessed projects are based on the current HTTP session.
            properties (array): A list of project properties to return for the project. This parameter accepts a comma-separated list.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        url = f"{self.base_url}/rest/api/3/project"
        query_params = {k: v for k, v in [('expand', expand), ('recent', recent), ('properties', properties)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_project(self, key, name, assigneeType=None, avatarId=None, categoryId=None, description=None, fieldConfigurationScheme=None, issueSecurityScheme=None, issueTypeScheme=None, issueTypeScreenScheme=None, lead=None, leadAccountId=None, notificationScheme=None, permissionScheme=None, projectTemplateKey=None, projectTypeKey=None, url=None, workflowScheme=None) -> dict[str, Any]:
        """
        Creates a new Jira project using the REST API, allowing the specification of project details such as key, name, type, and description.

        Args:
            key (string): Project keys must be unique and start with an uppercase letter followed by one or more uppercase alphanumeric characters. The maximum length is 10 characters.
            name (string): The name of the project.
            assigneeType (string): The default assignee when creating issues for this project.
            avatarId (integer): An integer value for the project's avatar.
            categoryId (integer): The ID of the project's category. A complete list of category IDs is found using the [Get all project categories](#api-rest-api-3-projectCategory-get) operation.
            description (string): A brief description of the project.
            fieldConfigurationScheme (integer): The ID of the field configuration scheme for the project. Use the [Get all field configuration schemes](#api-rest-api-3-fieldconfigurationscheme-get) operation to get a list of field configuration scheme IDs. If you specify the field configuration scheme you cannot specify the project template key.
            issueSecurityScheme (integer): The ID of the issue security scheme for the project, which enables you to control who can and cannot view issues. Use the [Get issue security schemes](#api-rest-api-3-issuesecurityschemes-get) resource to get all issue security scheme IDs.
            issueTypeScheme (integer): The ID of the issue type scheme for the project. Use the [Get all issue type schemes](#api-rest-api-3-issuetypescheme-get) operation to get a list of issue type scheme IDs. If you specify the issue type scheme you cannot specify the project template key.
            issueTypeScreenScheme (integer): The ID of the issue type screen scheme for the project. Use the [Get all issue type screen schemes](#api-rest-api-3-issuetypescreenscheme-get) operation to get a list of issue type screen scheme IDs. If you specify the issue type screen scheme you cannot specify the project template key.
            lead (string): This parameter is deprecated because of privacy changes. Use `leadAccountId` instead. See the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details. The user name of the project lead. Either `lead` or `leadAccountId` must be set when creating a project. Cannot be provided with `leadAccountId`.
            leadAccountId (string): The account ID of the project lead. Either `lead` or `leadAccountId` must be set when creating a project. Cannot be provided with `lead`.
            notificationScheme (integer): The ID of the notification scheme for the project. Use the [Get notification schemes](#api-rest-api-3-notificationscheme-get) resource to get a list of notification scheme IDs.
            permissionScheme (integer): The ID of the permission scheme for the project. Use the [Get all permission schemes](#api-rest-api-3-permissionscheme-get) resource to see a list of all permission scheme IDs.
            projectTemplateKey (string): A predefined configuration for a project. The type of the `projectTemplateKey` must match with the type of the `projectTypeKey`.
            projectTypeKey (string): The [project type](https://confluence.atlassian.com/x/GwiiLQ#Jiraapplicationsoverview-Productfeaturesandprojecttypes), which defines the application-specific feature set. If you don't specify the project template you have to specify the project type.
            url (string): A link to information about this project, such as project documentation
            workflowScheme (integer): The ID of the workflow scheme for the project. Use the [Get all workflow schemes](#api-rest-api-3-workflowscheme-get) operation to get a list of workflow scheme IDs. If you specify the workflow scheme you cannot specify the project template key.
                Example:
                ```json
                {
                  "assigneeType": "PROJECT_LEAD",
                  "avatarId": 10200,
                  "categoryId": 10120,
                  "description": "Cloud migration initiative",
                  "issueSecurityScheme": 10001,
                  "key": "EX",
                  "leadAccountId": "5b10a0effa615349cb016cd8",
                  "name": "Example",
                  "notificationScheme": 10021,
                  "permissionScheme": 10011,
                  "projectTemplateKey": "com.atlassian.jira-core-project-templates:jira-core-simplified-process-control",
                  "projectTypeKey": "business",
                  "url": "http://atlassian.com"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the project is created.

        Tags:
            Projects
        """
        request_body = {
            'assigneeType': assigneeType,
            'avatarId': avatarId,
            'categoryId': categoryId,
            'description': description,
            'fieldConfigurationScheme': fieldConfigurationScheme,
            'issueSecurityScheme': issueSecurityScheme,
            'issueTypeScheme': issueTypeScheme,
            'issueTypeScreenScheme': issueTypeScreenScheme,
            'key': key,
            'lead': lead,
            'leadAccountId': leadAccountId,
            'name': name,
            'notificationScheme': notificationScheme,
            'permissionScheme': permissionScheme,
            'projectTemplateKey': projectTemplateKey,
            'projectTypeKey': projectTypeKey,
            'url': url,
            'workflowScheme': workflowScheme,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_project_with_custom_template(self, details=None, template=None) -> Any:
        """
        Creates a project in Jira from a specified project template and returns a redirect response to the new project.

        Args:
            details (object): Project Details
            template (object): The specific request object for creating a project with template.

        Returns:
            Any: API response data.

        Tags:
            Project templates
        """
        request_body = {
            'details': details,
            'template': template,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project-template"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_recent(self, expand=None, properties=None) -> list[Any]:
        """
        Retrieves a list of up to 20 recently viewed projects still visible to the user.

        Args:
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expanded options include: * `description` Returns the project description. * `projectKeys` Returns all project keys associated with a project. * `lead` Returns information about the project lead. * `issueTypes` Returns all issue types associated with the project. * `url` Returns the URL associated with the project. * `permissions` Returns the permissions associated with the project. * `insight` EXPERIMENTAL. Returns the insight details of total issue count and last issue update time for the project. * `*` Returns the project with all available expand options.
            properties (array): EXPERIMENTAL. A list of project properties to return for the project. This parameter accepts a comma-separated list. Invalid property names are ignored.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        url = f"{self.base_url}/rest/api/3/project/recent"
        query_params = {k: v for k, v in [('expand', expand), ('properties', properties)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_projects(self, startAt=None, maxResults=None, orderBy=None, id=None, keys=None, query=None, typeKey=None, categoryId=None, action=None, expand=None, status=None, properties=None, propertyQuery=None) -> dict[str, Any]:
        """
        Searches for Jira projects using various criteria such as project ID, keys, category, and more, returning a list of matching projects based on the specified parameters using the Jira Cloud REST API.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field. * `category` Sorts by project category. A complete list of category IDs is found using [Get all project categories](#api-rest-api-3-projectCategory-get). * `issueCount` Sorts by the total number of issues in each project. * `key` Sorts by project key. * `lastIssueUpdatedTime` Sorts by the last issue update time. * `name` Sorts by project name. * `owner` Sorts by project lead. * `archivedDate` EXPERIMENTAL. Sorts by project archived date. * `deletedDate` EXPERIMENTAL. Sorts by project deleted date.
            id (array): The project IDs to filter the results by. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`. Up to 50 project IDs can be provided.
            keys (array): The project keys to filter the results by. To include multiple keys, provide an ampersand-separated list. For example, `keys=PA&keys=PB`. Up to 50 project keys can be provided.
            query (string): Filter the results using a literal string. Projects with a matching `key` or `name` are returned (case insensitive).
            typeKey (string): Orders results by the [project type]( This parameter accepts a comma-separated list. Valid values are `business`, `service_desk`, and `software`.
            categoryId (integer): The ID of the project's category. A complete list of category IDs is found using the [Get all project categories](#api-rest-api-3-projectCategory-get) operation.
            action (string): Filter results by projects for which the user can: * `view` the project, meaning that they have one of the following permissions: * *Browse projects* [project permission]( for the project. * *Administer projects* [project permission]( for the project. * *Administer Jira* [global permission]( * `browse` the project, meaning that they have the *Browse projects* [project permission]( for the project. * `edit` the project, meaning that they have one of the following permissions: * *Administer projects* [project permission]( for the project. * *Administer Jira* [global permission]( * `create` the project, meaning that they have the *Create issues* [project permission]( for the project in which the issue is created.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expanded options include: * `description` Returns the project description. * `projectKeys` Returns all project keys associated with a project. * `lead` Returns information about the project lead. * `issueTypes` Returns all issue types associated with the project. * `url` Returns the URL associated with the project. * `insight` EXPERIMENTAL. Returns the insight details of total issue count and last issue update time for the project.
            status (array): EXPERIMENTAL. Filter results by project status: * `live` Search live projects. * `archived` Search archived projects. * `deleted` Search deleted projects, those in the recycle bin.
            properties (array): EXPERIMENTAL. A list of project properties to return for the project. This parameter accepts a comma-separated list.
            propertyQuery (string): EXPERIMENTAL. A query string used to search properties. The query string cannot be specified using a JSON object. For example, to search for the value of `nested` from `{"something":{"nested":1,"other":2}}` use `[thepropertykey].something.nested=1`. Note that the propertyQuery key is enclosed in square brackets to enable searching where the propertyQuery key includes dot (.) or equals (=) characters. Note that `thepropertykey` is only returned when included in `properties`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        url = f"{self.base_url}/rest/api/3/project/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy), ('id', id), ('keys', keys), ('query', query), ('typeKey', typeKey), ('categoryId', categoryId), ('action', action), ('expand', expand), ('status', status), ('properties', properties), ('propertyQuery', propertyQuery)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_project_types(self) -> list[Any]:
        """
        Retrieves all project types available in Jira Cloud, including those without valid licenses, and can be accessed anonymously without permissions.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project types
        """
        url = f"{self.base_url}/rest/api/3/project/type"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_accessible_project_types(self) -> list[Any]:
        """
        Retrieves a list of project types accessible to the calling user via the Jira Cloud REST API.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project types
        """
        url = f"{self.base_url}/rest/api/3/project/type/accessible"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_type_by_key(self, projectTypeKey) -> dict[str, Any]:
        """
        Retrieves the project type details for a specified project type key using the "GET" method.

        Args:
            projectTypeKey (string): projectTypeKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project types
        """
        if projectTypeKey is None:
            raise ValueError("Missing required parameter 'projectTypeKey'")
        url = f"{self.base_url}/rest/api/3/project/type/{projectTypeKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_accessible_project_type_by_key(self, projectTypeKey) -> dict[str, Any]:
        """
        Retrieves details of a specific project type accessible to the user in Jira Cloud based on the provided project type key.

        Args:
            projectTypeKey (string): projectTypeKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project types
        """
        if projectTypeKey is None:
            raise ValueError("Missing required parameter 'projectTypeKey'")
        url = f"{self.base_url}/rest/api/3/project/type/{projectTypeKey}/accessible"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project(self, projectIdOrKey, enableUndo=None) -> Any:
        """
        Deletes a Jira project identified by its ID or key, with an optional undo capability via query parameter.

        Args:
            projectIdOrKey (string): projectIdOrKey
            enableUndo (boolean): Whether this project is placed in the Jira recycle bin where it will be available for restoration.

        Returns:
            Any: Returned if the project is deleted.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}"
        query_params = {k: v for k, v in [('enableUndo', enableUndo)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project(self, projectIdOrKey, expand=None, properties=None) -> dict[str, Any]:
        """
        Retrieves details about a specific Jira project by its ID or key, allowing optional expansion of additional details and properties, using the Jira REST API.

        Args:
            projectIdOrKey (string): projectIdOrKey
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Note that the project description, issue types, and project lead are included in all responses by default. Expand options include: * `description` The project description. * `issueTypes` The issue types associated with the project. * `lead` The project lead. * `projectKeys` All project keys associated with the project. * `issueTypeHierarchy` The project issue type hierarchy.
            properties (array): A list of project properties to return for the project. This parameter accepts a comma-separated list.

        Returns:
            dict[str, Any]: Returned if successful.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}"
        query_params = {k: v for k, v in [('expand', expand), ('properties', properties)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_project(self, projectIdOrKey, expand=None, assigneeType=None, avatarId=None, categoryId=None, description=None, issueSecurityScheme=None, key=None, lead=None, leadAccountId=None, name=None, notificationScheme=None, permissionScheme=None, releasedProjectKeys=None, url=None) -> dict[str, Any]:
        """
        Updates or replaces a Jira project identified by the projectIdOrKey and returns the modified project.

        Args:
            projectIdOrKey (string): projectIdOrKey
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Note that the project description, issue types, and project lead are included in all responses by default. Expand options include: * `description` The project description. * `issueTypes` The issue types associated with the project. * `lead` The project lead. * `projectKeys` All project keys associated with the project.
            assigneeType (string): The default assignee when creating issues for this project.
            avatarId (integer): An integer value for the project's avatar.
            categoryId (integer): The ID of the project's category. A complete list of category IDs is found using the [Get all project categories](#api-rest-api-3-projectCategory-get) operation. To remove the project category from the project, set the value to `-1.`
            description (string): A brief description of the project.
            issueSecurityScheme (integer): The ID of the issue security scheme for the project, which enables you to control who can and cannot view issues. Use the [Get issue security schemes](#api-rest-api-3-issuesecurityschemes-get) resource to get all issue security scheme IDs.
            key (string): Project keys must be unique and start with an uppercase letter followed by one or more uppercase alphanumeric characters. The maximum length is 10 characters.
            lead (string): This parameter is deprecated because of privacy changes. Use `leadAccountId` instead. See the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details. The user name of the project lead. Cannot be provided with `leadAccountId`.
            leadAccountId (string): The account ID of the project lead. Cannot be provided with `lead`.
            name (string): The name of the project.
            notificationScheme (integer): The ID of the notification scheme for the project. Use the [Get notification schemes](#api-rest-api-3-notificationscheme-get) resource to get a list of notification scheme IDs.
            permissionScheme (integer): The ID of the permission scheme for the project. Use the [Get all permission schemes](#api-rest-api-3-permissionscheme-get) resource to see a list of all permission scheme IDs.
            releasedProjectKeys (array): Previous project keys to be released from the current project. Released keys must belong to the current project and not contain the current project key
            url (string): A link to information about this project, such as project documentation
                Example:
                ```json
                {
                  "assigneeType": "PROJECT_LEAD",
                  "avatarId": 10200,
                  "categoryId": 10120,
                  "description": "Cloud migration initiative",
                  "issueSecurityScheme": 10001,
                  "key": "EX",
                  "leadAccountId": "5b10a0effa615349cb016cd8",
                  "name": "Example",
                  "notificationScheme": 10021,
                  "permissionScheme": 10011,
                  "url": "http://atlassian.com"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the project is updated.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        request_body = {
            'assigneeType': assigneeType,
            'avatarId': avatarId,
            'categoryId': categoryId,
            'description': description,
            'issueSecurityScheme': issueSecurityScheme,
            'key': key,
            'lead': lead,
            'leadAccountId': leadAccountId,
            'name': name,
            'notificationScheme': notificationScheme,
            'permissionScheme': permissionScheme,
            'releasedProjectKeys': releasedProjectKeys,
            'url': url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def archive_project(self, projectIdOrKey) -> Any:
        """
        Archives a Jira project using the "POST" method by specifying the project ID or key in the path "/rest/api/3/project/{projectIdOrKey}/archive".

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/archive"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_project_avatar(self, projectIdOrKey, id, fileName=None, isDeletable=None, isSelected=None, isSystemAvatar=None, owner=None, urls=None) -> Any:
        """
        Sets the displayed avatar for a Jira project using the specified project ID or key.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): The ID of the avatar.
            fileName (string): The file name of the avatar icon. Returned for system avatars.
            isDeletable (boolean): Whether the avatar can be deleted.
            isSelected (boolean): Whether the avatar is used in Jira. For example, shown as a project's avatar.
            isSystemAvatar (boolean): Whether the avatar is a system avatar.
            owner (string): The owner of the avatar. For a system avatar the owner is null (and nothing is returned). For non-system avatars this is the appropriate identifier, such as the ID for a project or the account ID for a user.
            urls (object): The list of avatar icon URLs.
                Example:
                ```json
                {
                  "id": "10010"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project avatars
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        request_body = {
            'fileName': fileName,
            'id': id,
            'isDeletable': isDeletable,
            'isSelected': isSelected,
            'isSystemAvatar': isSystemAvatar,
            'owner': owner,
            'urls': urls,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/avatar"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project_avatar(self, projectIdOrKey, id) -> Any:
        """
        Deletes a custom project avatar (system avatars cannot be deleted) using the Jira REST API.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project avatars
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/avatar/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

 
    def get_all_project_avatars(self, projectIdOrKey) -> dict[str, Any]:
        """
        Retrieves the list of avatars associated with a specified Jira project, including system and custom avatars.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            dict[str, Any]: Returned if request is successful.

        Tags:
            Project avatars
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/avatars"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_default_project_classification(self, projectIdOrKey) -> Any:
        """
        Removes the default data classification level from a Jira project using the Jira Cloud API, returning a status code indicating success or failure.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project classification levels
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/classification-level/default"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_default_project_classification(self, projectIdOrKey) -> Any:
        """
        Retrieves the default data classification level configured for a specified Jira project.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project classification levels
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/classification-level/default"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_default_project_classification(self, projectIdOrKey, id) -> Any:
        """
        Updates the default data classification level for a Jira project.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): The ID of the project classification.
                Example:
                ```json
                {
                  "id": "ari:cloud:platform::classification-tag/dec24c48-5073-4c25-8fef-9d81a992c30c"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project classification levels
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        request_body = {
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/classification-level/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_components_paginated(self, projectIdOrKey, startAt=None, maxResults=None, orderBy=None, componentSource=None, query=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of components associated with a specified Jira project, optionally filtered and ordered by query parameters.

        Args:
            projectIdOrKey (string): projectIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field: * `description` Sorts by the component description. * `issueCount` Sorts by the count of issues associated with the component. * `lead` Sorts by the user key of the component's project lead. * `name` Sorts by component name.
            componentSource (string): The source of the components to return. Can be `jira` (default), `compass` or `auto`. When `auto` is specified, the API will return connected Compass components if the project is opted into Compass, otherwise it will return Jira components. Defaults to `jira`.
            query (string): Filter the results using a literal string. Components with a matching `name` or `description` are returned (case insensitive).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/component"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy), ('componentSource', componentSource), ('query', query)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_components(self, projectIdOrKey, componentSource=None) -> list[Any]:
        """
        Retrieves a list of components for a specified Jira project using its ID or key, with optional filtering by component source.

        Args:
            projectIdOrKey (string): projectIdOrKey
            componentSource (string): The source of the components to return. Can be `jira` (default), `compass` or `auto`. When `auto` is specified, the API will return connected Compass components if the project is opted into Compass, otherwise it will return Jira components. Defaults to `jira`.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project components
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/components"
        query_params = {k: v for k, v in [('componentSource', componentSource)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project_asynchronously(self, projectIdOrKey) -> Any:
        """
        Deletes a Jira project specified by its ID or key via a POST request and returns relevant status codes.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            Any: API response data.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/delete"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_features_for_project(self, projectIdOrKey) -> dict[str, Any]:
        """
        Retrieves the list of features for a specified Jira project using the project ID or key.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project features
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/features"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def toggle_feature_for_project(self, projectIdOrKey, featureKey, state=None) -> dict[str, Any]:
        """
        Updates the configuration of a specific feature for a Jira project using the project identifier and feature key.

        Args:
            projectIdOrKey (string): projectIdOrKey
            featureKey (string): featureKey
            state (string): The feature state.
                Example:
                ```json
                {
                  "state": "ENABLED"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project features
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if featureKey is None:
            raise ValueError("Missing required parameter 'featureKey'")
        request_body = {
            'state': state,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/features/{featureKey}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_property_keys(self, projectIdOrKey) -> dict[str, Any]:
        """
        Retrieves a list of project property keys for a specified project in Jira Cloud using the provided project ID or key.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project properties
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project_property(self, projectIdOrKey, propertyKey) -> Any:
        """
        Deletes a specific project property from a Jira project using the project ID or key and property key, requiring administrative permissions.

        Args:
            projectIdOrKey (string): projectIdOrKey
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the project property is deleted.

        Tags:
            Project properties
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_property(self, projectIdOrKey, propertyKey) -> dict[str, Any]:
        """
        Retrieves the value of a specific project property using the Jira Cloud API and returns it based on the provided project ID or key and property key.

        Args:
            projectIdOrKey (string): projectIdOrKey
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project properties
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

 
    def restore(self, projectIdOrKey) -> dict[str, Any]:
        """
        Restores a deleted or archived Jira project identified by its project ID or key.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/restore"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_roles(self, projectIdOrKey) -> dict[str, Any]:
        """
        Retrieves a list of project roles (including names, IDs, and self URLs) for a specific Jira project using its ID or key.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/role"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_actor(self, projectIdOrKey, id, user=None, group=None, groupId=None) -> Any:
        """
        Deletes a user or group from a specific project role in Jira, returning a success status if removed.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): id
            user (string): The user account ID of the user to remove from the project role. Example: '5b10ac8d82e05b22cc7d4ef5'.
            group (string): The name of the group to remove from the project role. This parameter cannot be used with the `groupId` parameter. As a group's name can change, use of `groupId` is recommended.
            groupId (string): The ID of the group to remove from the project role. This parameter cannot be used with the `group` parameter.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project role actors
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/role/{id}"
        query_params = {k: v for k, v in [('user', user), ('group', group), ('groupId', groupId)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_role(self, projectIdOrKey, id, excludeInactiveUsers=None) -> dict[str, Any]:
        """
        Retrieves a specific project role's details and associated actors for a Jira project using the provided project identifier and role ID.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): id
            excludeInactiveUsers (boolean): Exclude inactive users.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/role/{id}"
        query_params = {k: v for k, v in [('excludeInactiveUsers', excludeInactiveUsers)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_actor_users(self, projectIdOrKey, id, group=None, groupId=None, user=None) -> dict[str, Any]:
        """
        Partially updates a project role's name or description using the Jira REST API.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): id
            group (array): The name of the group to add. This parameter cannot be used with the `groupId` parameter. As a group's name can change, use of `groupId` is recommended.
            groupId (array): The ID of the group to add. This parameter cannot be used with the `group` parameter.
            user (array): The user account ID of the user to add.
                Example:
                ```json
                {
                  "groupId": [
                    "952d12c3-5b5b-4d04-bb32-44d383afc4b2"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful. The complete list of actors for the project is returned.

        For example, the cURL request above adds a group, *jira-developers*. For the response below to be returned as a result of that request, the user *Mia Krystof* would have previously been added as a `user` actor for this project.

        Tags:
            Project role actors
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'group': group,
            'groupId': groupId,
            'user': user,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/role/{id}"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_actors(self, projectIdOrKey, id, categorisedActors=None, id_body=None) -> dict[str, Any]:
        """
        Fully updates a project role by ID for a specified Jira project using the provided parameters.

        Args:
            projectIdOrKey (string): projectIdOrKey
            id (string): id
            categorisedActors (object): The actors to add to the project role.

        Add groups using:

         *  `atlassian-group-role-actor` and a list of group names.
         *  `atlassian-group-role-actor-id` and a list of group IDs.

        As a group's name can change, use of `atlassian-group-role-actor-id` is recommended. For example, `"atlassian-group-role-actor-id":["eef79f81-0b89-4fca-a736-4be531a10869","77f6ab39-e755-4570-a6ae-2d7a8df0bcb8"]`.

        Add users using `atlassian-user-role-actor` and a list of account IDs. For example, `"atlassian-user-role-actor":["12345678-9abc-def1-2345-6789abcdef12", "abcdef12-3456-789a-bcde-f123456789ab"]`.
            id_body (integer): The ID of the project role. Use [Get all project roles](#api-rest-api-3-role-get) to get a list of project role IDs.
                Example:
                ```json
                {
                  "categorisedActors": {
                    "atlassian-group-role-actor-id": [
                      "952d12c3-5b5b-4d04-bb32-44d383afc4b2"
                    ],
                    "atlassian-user-role-actor": [
                      "12345678-9abc-def1-2345-6789abcdef12"
                    ]
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful. The complete list of actors for the project is returned.

        Tags:
            Project role actors
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'categorisedActors': categorisedActors,
            'id': id_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/role/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_role_details(self, projectIdOrKey, currentMember=None, excludeConnectAddons=None) -> list[Any]:
        """
        Retrieves role details for a specified project, including information about project roles and their associated members, using a GET request.

        Args:
            projectIdOrKey (string): projectIdOrKey
            currentMember (boolean): Whether the roles should be filtered to include only those the user is assigned to.
            excludeConnectAddons (boolean): Excludes Connect add-ons from the role details response when set to true.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/roledetails"
        query_params = {k: v for k, v in [('currentMember', currentMember), ('excludeConnectAddons', excludeConnectAddons)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_statuses(self, projectIdOrKey) -> list[Any]:
        """
        Retrieves a list of statuses available for a specific Jira project, identified by its ID or key, using the GET method.

        Args:
            projectIdOrKey (string): projectIdOrKey

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/statuses"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_versions_paginated(self, projectIdOrKey, startAt=None, maxResults=None, orderBy=None, query=None, status=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a list of versions for a specified Jira project, allowing for pagination, filtering, and expansion of details using various query parameters.

        Args:
            projectIdOrKey (string): projectIdOrKey
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            orderBy (string): [Order](#ordering) the results by a field: * `description` Sorts by version description. * `name` Sorts by version name. * `releaseDate` Sorts by release date, starting with the oldest date. Versions with no release date are listed last. * `sequence` Sorts by the order of appearance in the user interface. * `startDate` Sorts by start date, starting with the oldest date. Versions with no start date are listed last.
            query (string): Filter the results using a literal string. Versions with matching `name` or `description` are returned (case insensitive).
            status (string): A list of status values used to filter the results by version status. This parameter accepts a comma-separated list. The status values are `released`, `unreleased`, and `archived`.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `issuesstatus` Returns the number of issues in each status category for each version. * `operations` Returns actions that can be performed on the specified version. * `driver` Returns the Atlassian account ID of the version driver. * `approvers` Returns a list containing the approvers for this version.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/version"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('orderBy', orderBy), ('query', query), ('status', status), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_versions(self, projectIdOrKey, expand=None) -> list[Any]:
        """
        Retrieves all versions of a specified Jira project, including version details like names, descriptions, and issue status counts.

        Args:
            projectIdOrKey (string): projectIdOrKey
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts `operations`, which returns actions that can be performed on the version.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if projectIdOrKey is None:
            raise ValueError("Missing required parameter 'projectIdOrKey'")
        url = f"{self.base_url}/rest/api/3/project/{projectIdOrKey}/versions"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_email(self, projectId) -> dict[str, Any]:
        """
        Retrieves email-related information for a specified project using its unique identifier.

        Args:
            projectId (string): projectId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project email
        """
        if projectId is None:
            raise ValueError("Missing required parameter 'projectId'")
        url = f"{self.base_url}/rest/api/3/project/{projectId}/email"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_project_email(self, projectId, emailAddress=None, emailAddressStatus=None) -> Any:
        """
        Updates the sender email address for a specific project's notifications and returns a success status upon completion.

        Args:
            projectId (string): projectId
            emailAddress (string): The email address.
            emailAddressStatus (array): When using a custom domain, the status of the email address.
                Example:
                ```json
                {
                  "emailAddress": "jira@example.atlassian.net"
                }
                ```

        Returns:
            Any: Returned if the project's sender email address is successfully set.

        Tags:
            Project email
        """
        if projectId is None:
            raise ValueError("Missing required parameter 'projectId'")
        request_body = {
            'emailAddress': emailAddress,
            'emailAddressStatus': emailAddressStatus,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectId}/email"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_hierarchy(self, projectId) -> dict[str, Any]:
        """
        Retrieves the hierarchy details for a specific project using the `GET` method at path "/rest/api/3/project/{projectId}/hierarchy".

        Args:
            projectId (string): projectId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        if projectId is None:
            raise ValueError("Missing required parameter 'projectId'")
        url = f"{self.base_url}/rest/api/3/project/{projectId}/hierarchy"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_issue_security_scheme(self, projectKeyOrId) -> dict[str, Any]:
        """
        Retrieves the issue security level scheme associated with a specified project in Jira.

        Args:
            projectKeyOrId (string): projectKeyOrId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project permission schemes
        """
        if projectKeyOrId is None:
            raise ValueError("Missing required parameter 'projectKeyOrId'")
        url = f"{self.base_url}/rest/api/3/project/{projectKeyOrId}/issuesecuritylevelscheme"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_notification_scheme_for_project(self, projectKeyOrId, expand=None) -> dict[str, Any]:
        """
        Retrieves the notification scheme associated with a specific project in Jira, including event configurations and recipient details.

        Args:
            projectKeyOrId (string): projectKeyOrId
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `all` Returns all expandable information * `field` Returns information about any custom fields assigned to receive an event * `group` Returns information about any groups assigned to receive an event * `notificationSchemeEvents` Returns a list of event associations. This list is returned for all expandable information * `projectRole` Returns information about any project roles assigned to receive an event * `user` Returns information about any users assigned to receive an event

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Projects
        """
        if projectKeyOrId is None:
            raise ValueError("Missing required parameter 'projectKeyOrId'")
        url = f"{self.base_url}/rest/api/3/project/{projectKeyOrId}/notificationscheme"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_assigned_permission_scheme(self, projectKeyOrId, expand=None) -> dict[str, Any]:
        """
        Retrieves the permission scheme associated with a specified Jira project by its key or ID, allowing optional expansion of certain details.

        Args:
            projectKeyOrId (string): projectKeyOrId
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project permission schemes
        """
        if projectKeyOrId is None:
            raise ValueError("Missing required parameter 'projectKeyOrId'")
        url = f"{self.base_url}/rest/api/3/project/{projectKeyOrId}/permissionscheme"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_permission_scheme(self, projectKeyOrId, id, expand=None) -> dict[str, Any]:
        """
        Assigns a permission scheme to a project using the Jira Cloud API, allowing administrators to manage project permissions by associating a specific permission scheme with a given project.

        Args:
            projectKeyOrId (string): projectKeyOrId
            id (integer): The ID of the permission scheme to associate with the project. Use the [Get all permission schemes](#api-rest-api-3-permissionscheme-get) resource to get a list of permission scheme IDs.
                Example:
                ```json
                {
                  "id": 10000
                }
                ```
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Note that permissions are included when you specify any value. Expand options include: * `all` Returns all expandable information. * `field` Returns information about the custom field granted the permission. * `group` Returns information about the group that is granted the permission. * `permissions` Returns all permission grants for each permission scheme. * `projectRole` Returns information about the project role granted the permission. * `user` Returns information about the user who is granted the permission.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project permission schemes
        """
        if projectKeyOrId is None:
            raise ValueError("Missing required parameter 'projectKeyOrId'")
        request_body = {
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/project/{projectKeyOrId}/permissionscheme"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_security_levels_for_project(self, projectKeyOrId) -> dict[str, Any]:
        """
        Retrieves issue security levels for a specified project using the provided project key or ID, returning details about the security levels associated with the project.

        Args:
            projectKeyOrId (string): projectKeyOrId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project permission schemes
        """
        if projectKeyOrId is None:
            raise ValueError("Missing required parameter 'projectKeyOrId'")
        url = f"{self.base_url}/rest/api/3/project/{projectKeyOrId}/securitylevel"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_project_categories(self) -> list[Any]:
        """
        Retrieves a project category from Jira using its ID and returns the category details.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project categories
        """
        url = f"{self.base_url}/rest/api/3/projectCategory"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_project_category(self, description=None, id=None, name=None, self_arg_body=None) -> dict[str, Any]:
        """
        Creates a new project category in Jira and returns the created category details.

        Args:
            description (string): The description of the project category.
            id (string): The ID of the project category.
            name (string): The name of the project category. Required on create, optional on update.
            self_arg_body (string): The URL of the project category.
                Example:
                ```json
                {
                  "description": "Created Project Category",
                  "name": "CREATED"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project categories
        """
        request_body = {
            'description': description,
            'id': id,
            'name': name,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/projectCategory"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_project_category(self, id) -> Any:
        """
        Deletes a project category by its ID using the Jira Cloud API, requiring admin permissions and returning a successful response without content if the operation is completed.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project categories
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/projectCategory/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_category_by_id(self, id) -> dict[str, Any]:
        """
        Retrieves a specific project category by ID from Jira using the REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project categories
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/projectCategory/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_project_category(self, id, description=None, id_body=None, name=None, self_arg_body=None) -> dict[str, Any]:
        """
        Updates a specific project category by ID in Jira using the PUT method, allowing modifications to the category details such as name and description.

        Args:
            id (string): id
            description (string): The description of the project category.
            id_body (string): The ID of the project category.
            name (string): The name of the project category. Required on create, optional on update.
            self_arg_body (string): The URL of the project category.
                Example:
                ```json
                {
                  "description": "Updated Project Category",
                  "name": "UPDATED"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project categories
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'id': id_body,
            'name': name,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/projectCategory/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def validate_project_key(self, key=None) -> dict[str, Any]:
        """
        Validates a project key by confirming the key's validity and checking for existing usage in Jira Cloud.

        Args:
            key (string): The project key. Example: 'HSP'.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project key and name validation
        """
        url = f"{self.base_url}/rest/api/3/projectvalidate/key"
        query_params = {k: v for k, v in [('key', key)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_valid_project_key(self, key=None) -> Any:
        """
        Validates a project key by confirming it is a valid string and not in use, returning success or error messages using the Jira Cloud REST API.

        Args:
            key (string): The project key. Example: 'HSP'.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project key and name validation
        """
        url = f"{self.base_url}/rest/api/3/projectvalidate/validProjectKey"
        query_params = {k: v for k, v in [('key', key)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_valid_project_name(self, name) -> Any:
        """
        Validates a project name's availability, returning the original name if available or generating a new valid name if unavailable.

        Args:
            name (string): The project name.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project key and name validation
        """
        url = f"{self.base_url}/rest/api/3/projectvalidate/validProjectName"
        query_params = {k: v for k, v in [('name', name)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_resolutions(self) -> list[Any]:
        """
        Retrieves a list of available resolution statuses for Jira issues.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        url = f"{self.base_url}/rest/api/3/resolution"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_resolution(self, name, description=None) -> dict[str, Any]:
        """
        Creates a new issue resolution in Jira using the REST API and returns the created resolution details.

        Args:
            name (string): The name of the resolution. Must be unique (case-insensitive).
            description (string): The description of the resolution.
                Example:
                ```json
                {
                  "description": "My resolution description",
                  "name": "My new resolution"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/resolution"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_default_resolution(self, id) -> Any:
        """
        Sets the default issue resolution in Jira using the REST API, requiring administrative permissions.

        Args:
            id (string): The ID of the new default issue resolution. Must be an existing ID or null. Setting this to null erases the default resolution setting.
                Example:
                ```json
                {
                  "id": "3"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        request_body = {
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/resolution/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def move_resolutions(self, ids, after=None, position=None) -> Any:
        """
        Moves issue resolutions using the Jira Cloud API with a PUT request to the "/rest/api/3/resolution/move" endpoint.

        Args:
            ids (array): The list of resolution IDs to be reordered. Cannot contain duplicates nor after ID.
            after (string): The ID of the resolution. Required if `position` isn't provided.
            position (string): The position for issue resolutions to be moved to. Required if `after` isn't provided.
                Example:
                ```json
                {
                  "after": "10002",
                  "ids": [
                    "10000",
                    "10001"
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        request_body = {
            'after': after,
            'ids': ids,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/resolution/move"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_resolutions(self, startAt=None, maxResults=None, id=None, onlyDefault=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of Jira issue resolutions using the GET method at the "/rest/api/3/resolution/search" path, allowing for filtering by parameters such as start position, maximum results, resolution ID, and default-only options.

        Args:
            startAt (string): The index of the first item to return in a page of results (page offset).
            maxResults (string): The maximum number of items to return per page.
            id (array): The list of resolutions IDs to be filtered out
            onlyDefault (boolean): When set to true, return default only, when IDs provided, if none of them is default, return empty page. Default value is false

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        url = f"{self.base_url}/rest/api/3/resolution/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('onlyDefault', onlyDefault)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_resolution(self, id, replaceWith) -> Any:
        """
        Deletes an issue resolution by ID using the Jira API and optionally replaces it with another resolution if specified.

        Args:
            id (string): id
            replaceWith (string): The ID of the issue resolution that will replace the currently selected resolution.

        Returns:
            Any: API response data.

        Tags:
            Issue resolutions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/resolution/{id}"
        query_params = {k: v for k, v in [('replaceWith', replaceWith)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_resolution(self, id) -> dict[str, Any]:
        """
        Retrieves the details of a specific resolution by its ID using the Jira Cloud Platform REST API and returns the resolution information.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/resolution/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_resolution(self, id, name, description=None) -> Any:
        """
        Updates the specified resolution's details in Jira using the provided ID, returning a success status upon completion.

        Args:
            id (string): id
            name (string): The name of the resolution. Must be unique.
            description (string): The description of the resolution.
                Example:
                ```json
                {
                  "description": "My updated resolution description",
                  "name": "My updated resolution"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Issue resolutions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/resolution/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_project_roles(self) -> list[Any]:
        """
        Retrieves role details in Jira projects using the specified REST API endpoint.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        url = f"{self.base_url}/rest/api/3/role"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_project_role(self, description=None, name=None) -> dict[str, Any]:
        """
        Creates a new role using the Jira API and returns a status message, handling responses for various HTTP status codes including successful creation, bad requests, unauthorized access, forbidden actions, and conflicts.

        Args:
            description (string): A description of the project role. Required when fully updating a project role. Optional when creating or partially updating a project role.
            name (string): The name of the project role. Must be unique. Cannot begin or end with whitespace. The maximum length is 255 characters. Required when creating a project role. Optional when partially updating a project role.
                Example:
                ```json
                {
                  "description": "A project role that represents developers in a project",
                  "name": "Developers"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/role"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project_role(self, id, swap=None) -> Any:
        """
        Deletes a role by its ID using the REST API.

        Args:
            id (string): id
            swap (integer): The ID of the project role that will replace the one being deleted. The swap will attempt to swap the role in schemes (notifications, permissions, issue security), workflows, worklogs and comments.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Project roles
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/role/{id}"
        query_params = {k: v for k, v in [('swap', swap)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_role_by_id(self, id) -> dict[str, Any]:
        """
        Retrieves a specific role in Jira by its ID using the GET method and returns the role details.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/role/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def partial_update_project_role(self, id, description=None, name=None) -> dict[str, Any]:
        """
        Updates a specific project role's configuration and returns the modified role details.

        Args:
            id (string): id
            description (string): A description of the project role. Required when fully updating a project role. Optional when creating or partially updating a project role.
            name (string): The name of the project role. Must be unique. Cannot begin or end with whitespace. The maximum length is 255 characters. Required when creating a project role. Optional when partially updating a project role.
                Example:
                ```json
                {
                  "description": "A project role that represents developers in a project",
                  "name": "Developers"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/role/{id}"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def fully_update_project_role(self, id, description=None, name=None) -> dict[str, Any]:
        """
        Updates or replaces an existing role's configuration via specified ID and returns the operation status.

        Args:
            id (string): id
            description (string): A description of the project role. Required when fully updating a project role. Optional when creating or partially updating a project role.
            name (string): The name of the project role. Must be unique. Cannot begin or end with whitespace. The maximum length is 255 characters. Required when creating a project role. Optional when partially updating a project role.
                Example:
                ```json
                {
                  "description": "A project role that represents developers in a project",
                  "name": "Developers"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project roles
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/role/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_project_role_actors_from_role(self, id, user=None, groupId=None, group=None) -> dict[str, Any]:
        """
        Deletes actors from a role using the "DELETE" method with options to specify a user or group ID, and returns corresponding status codes based on the success or failure of the operation.

        Args:
            id (string): id
            user (string): The user account ID of the user to remove as a default actor. Example: '5b10ac8d82e05b22cc7d4ef5'.
            groupId (string): The group ID of the group to be removed as a default actor. This parameter cannot be used with the `group` parameter.
            group (string): The group name of the group to be removed as a default actor.This parameter cannot be used with the `groupId` parameter. As a group's name can change, use of `groupId` is recommended.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project role actors
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/role/{id}/actors"
        query_params = {k: v for k, v in [('user', user), ('groupId', groupId), ('group', group)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_role_actors_for_role(self, id) -> dict[str, Any]:
        """
        Retrieves a list of actors associated with a specified role ID using the Jira REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project role actors
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/role/{id}/actors"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_project_role_actors_to_role(self, id, group=None, groupId=None, user=None) -> dict[str, Any]:
        """
        Adds or modifies actors (users/groups) for a specific project role ID and returns the updated role details.

        Args:
            id (string): id
            group (array): The name of the group to add as a default actor. This parameter cannot be used with the `groupId` parameter. As a group's name can change,use of `groupId` is recommended. This parameter accepts a comma-separated list. For example, `"group":["project-admin", "jira-developers"]`.
            groupId (array): The ID of the group to add as a default actor. This parameter cannot be used with the `group` parameter This parameter accepts a comma-separated list. For example, `"groupId":["77f6ab39-e755-4570-a6ae-2d7a8df0bcb8", "0c011f85-69ed-49c4-a801-3b18d0f771bc"]`.
            user (array): The account IDs of the users to add as default actors. This parameter accepts a comma-separated list. For example, `"user":["5b10a2844c20165700ede21g", "5b109f2e9729b51b54dc274d"]`.
                Example:
                ```json
                {
                  "user": [
                    "admin"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project role actors
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'group': group,
            'groupId': groupId,
            'user': user,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/role/{id}/actors"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_screens(self, startAt=None, maxResults=None, id=None, queryString=None, scope=None, orderBy=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of all screens or specified screens by ID in Jira, allowing for optional filtering by query parameters such as start position, maximum results, and query string.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of screen IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.
            queryString (string): String used to perform a case-insensitive partial match with screen name.
            scope (array): The scope filter string. To filter by multiple scope, provide an ampersand-separated list. For example, `scope=GLOBAL&scope=PROJECT`.
            orderBy (string): [Order](#ordering) the results by a field: * `id` Sorts by screen ID. * `name` Sorts by screen name.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screens
        """
        url = f"{self.base_url}/rest/api/3/screens"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('queryString', queryString), ('scope', scope), ('orderBy', orderBy)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_screen(self, name, description=None) -> dict[str, Any]:
        """
        Creates a new screen in Jira using the REST API and returns a successful response if the operation is completed without errors.

        Args:
            name (string): The name of the screen. The name must be unique. The maximum length is 255 characters.
            description (string): The description of the screen. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "description": "Enables changes to resolution and linked issues.",
                  "name": "Resolve Security Issue Screen"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screens
        """
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_field_to_default_screen(self, fieldId) -> Any:
        """
        Adds a custom field to the default tab of the default screen using the Jira Cloud REST API.

        Args:
            fieldId (string): fieldId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screens
        """
        if fieldId is None:
            raise ValueError("Missing required parameter 'fieldId'")
        url = f"{self.base_url}/rest/api/3/screens/addToDefault/{fieldId}"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_bulk_screen_tabs(self, screenId=None, tabId=None, startAt=None, maxResult=None) -> Any:
        """
        Retrieves the list of tabs for a specified screen in Jira Cloud, including pagination support through startAt and maxResult parameters.

        Args:
            screenId (array): The list of screen IDs. To include multiple screen IDs, provide an ampersand-separated list. For example, `screenId=10000&screenId=10001`.
            tabId (array): The list of tab IDs. To include multiple tab IDs, provide an ampersand-separated list. For example, `tabId=10000&tabId=10001`.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResult (integer): The maximum number of items to return per page. The maximum number is 100,

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        url = f"{self.base_url}/rest/api/3/screens/tabs"
        query_params = {k: v for k, v in [('screenId', screenId), ('tabId', tabId), ('startAt', startAt), ('maxResult', maxResult)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_screen(self, screenId) -> Any:
        """
        Deletes a specified screen in Jira if not used in screen schemes, workflows, or workflow drafts, returning success if the operation completes.

        Args:
            screenId (string): screenId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screens
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_screen(self, screenId, description=None, name=None) -> dict[str, Any]:
        """
        Updates or replaces a screen resource identified by the specified `screenId` using the PUT method.

        Args:
            screenId (string): screenId
            description (string): The description of the screen. The maximum length is 255 characters.
            name (string): The name of the screen. The name must be unique. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "description": "Enables changes to resolution and linked issues for accessibility related issues.",
                  "name": "Resolve Accessibility Issue Screen"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screens
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        request_body = {
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens/{screenId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_available_screen_fields(self, screenId) -> list[Any]:
        """
        Retrieves available fields for a specified screen in Jira, including both system and custom fields.

        Args:
            screenId (string): screenId

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Screens
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/availableFields"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_screen_tabs(self, screenId, projectKey=None) -> list[Any]:
        """
        Retrieves the list of tabs configured for a specific screen in Jira using the provided screen ID.

        Args:
            screenId (string): screenId
            projectKey (string): The key of the project.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs"
        query_params = {k: v for k, v in [('projectKey', projectKey)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_screen_tab(self, screenId, name, id=None) -> dict[str, Any]:
        """
        Creates a new tab in a Jira screen using the specified screen ID and returns the created screen tab.

        Args:
            screenId (string): screenId
            name (string): The name of the screen tab. The maximum length is 255 characters.
            id (integer): The ID of the screen tab.
                Example:
                ```json
                {
                  "name": "Fields Tab"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        request_body = {
            'id': id,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_screen_tab(self, screenId, tabId) -> Any:
        """
        Deletes a specified screen tab from a Jira screen and returns a success status upon completion.

        Args:
            screenId (string): screenId
            tabId (string): tabId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def rename_screen_tab(self, screenId, tabId, name, id=None) -> dict[str, Any]:
        """
        Updates the details of a specific screen tab identified by `screenId` and `tabId` using the Jira API, returning a status message upon successful modification.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            name (string): The name of the screen tab. The maximum length is 255 characters.
            id (integer): The ID of the screen tab.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        request_body = {
            'id': id,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_screen_tab_fields(self, screenId, tabId, projectKey=None) -> list[Any]:
        """
        Retrieves all fields associated with a specific screen tab in Jira Cloud.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            projectKey (string): The key of the project.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Screen tab fields
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}/fields"
        query_params = {k: v for k, v in [('projectKey', projectKey)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def add_screen_tab_field(self, screenId, tabId, fieldId) -> dict[str, Any]:
        """
        Adds a field to a specified screen tab in Jira and returns the field configuration upon success.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            fieldId (string): The ID of the field to add.
                Example:
                ```json
                {
                  "fieldId": "summary"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screen tab fields
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        request_body = {
            'fieldId': fieldId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}/fields"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_screen_tab_field(self, screenId, tabId, id) -> Any:
        """
        Removes a field from a specific screen tab in Jira and returns an empty response upon success.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen tab fields
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def move_screen_tab_field(self, screenId, tabId, id, after=None, position=None) -> Any:
        """
        Moves a screen tab field to a new position using the Jira Cloud platform REST API, allowing for reorganization of issue details fields on a specific screen tab.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            id (string): id
            after (string): The ID of the screen tab field after which to place the moved screen tab field. Required if `position` isn't provided.
            position (string): The named position to which the screen tab field should be moved. Required if `after` isn't provided.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen tab fields
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'after': after,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}/fields/{id}/move"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def move_screen_tab(self, screenId, tabId, pos) -> Any:
        """
        Moves a tab to a specified position within a screen using the "POST" method.

        Args:
            screenId (string): screenId
            tabId (string): tabId
            pos (string): pos

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen tabs
        """
        if screenId is None:
            raise ValueError("Missing required parameter 'screenId'")
        if tabId is None:
            raise ValueError("Missing required parameter 'tabId'")
        if pos is None:
            raise ValueError("Missing required parameter 'pos'")
        url = f"{self.base_url}/rest/api/3/screens/{screenId}/tabs/{tabId}/move/{pos}"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_screen_schemes(self, startAt=None, maxResults=None, id=None, expand=None, queryString=None, orderBy=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of screen schemes used in classic projects in Jira Cloud using the GET method, allowing for optional filtering by query parameters such as startAt, maxResults, id, expand, queryString, and orderBy.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            id (array): The list of screen scheme IDs. To include multiple IDs, provide an ampersand-separated list. For example, `id=10000&id=10001`.
            expand (string): Use [expand](#expansion) include additional information in the response. This parameter accepts `issueTypeScreenSchemes` that, for each screen schemes, returns information about the issue type screen scheme the screen scheme is assigned to.
            queryString (string): String used to perform a case-insensitive partial match with screen scheme name.
            orderBy (string): [Order](#ordering) the results by a field: * `id` Sorts by screen scheme ID. * `name` Sorts by screen scheme name.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screen schemes
        """
        url = f"{self.base_url}/rest/api/3/screenscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('id', id), ('expand', expand), ('queryString', queryString), ('orderBy', orderBy)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_screen_scheme(self, name, screens, description=None) -> dict[str, Any]:
        """
        Creates a new screen scheme in Jira for defining screen configurations associated with workflows and returns the created resource upon success.

        Args:
            name (string): The name of the screen scheme. The name must be unique. The maximum length is 255 characters.
            screens (string): The IDs of the screens for the screen types of the screen scheme. Only screens used in classic projects are accepted.
            description (string): The description of the screen scheme. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "description": "Manage employee data",
                  "name": "Employee screen scheme",
                  "screens": {
                    "default": 10017,
                    "edit": 10019,
                    "view": 10020
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Screen schemes
        """
        request_body = {
            'description': description,
            'name': name,
            'screens': screens,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screenscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_screen_scheme(self, screenSchemeId) -> Any:
        """
        Deletes a screen scheme in Jira using the `DELETE` method, provided it is not used in an issue type screen scheme and is associated with a classic project.

        Args:
            screenSchemeId (string): screenSchemeId

        Returns:
            Any: Returned if the screen scheme is deleted.

        Tags:
            Screen schemes
        """
        if screenSchemeId is None:
            raise ValueError("Missing required parameter 'screenSchemeId'")
        url = f"{self.base_url}/rest/api/3/screenscheme/{screenSchemeId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_screen_scheme(self, screenSchemeId, description=None, name=None, screens=None) -> Any:
        """
        Updates a specific screen scheme, identified by its ID, in Jira Cloud's classic projects, allowing modifications to its details and settings.

        Args:
            screenSchemeId (string): screenSchemeId
            description (string): The description of the screen scheme. The maximum length is 255 characters.
            name (string): The name of the screen scheme. The name must be unique. The maximum length is 255 characters.
            screens (string): The IDs of the screens for the screen types of the screen scheme. Only screens used in classic projects are accepted.
                Example:
                ```json
                {
                  "name": "Employee screen scheme v2",
                  "screens": {
                    "create": "10019",
                    "default": "10018"
                  }
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Screen schemes
        """
        if screenSchemeId is None:
            raise ValueError("Missing required parameter 'screenSchemeId'")
        request_body = {
            'description': description,
            'name': name,
            'screens': screens,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/screenscheme/{screenSchemeId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_for_issues_using_jql(self, jql=None, startAt=None, maxResults=None, validateQuery=None, fields=None, expand=None, properties=None, fieldsByKeys=None, failFast=None) -> dict[str, Any]:
        """
        Searches for Jira issues using JQL queries and returns paginated results with specified fields and expansion options.

        Args:
            jql (string): The [JQL]( that defines the search. Note: * If no JQL expression is provided, all issues are returned. * `username` and `userkey` cannot be used as search terms due to privacy reasons. Use `accountId` instead. * If a user has hidden their email address in their user profile, partial matches of the email address will not find the user. An exact match is required. Example: 'project = HSP'.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page. To manage page size, Jira may return fewer items per page where a large number of fields or properties are requested. The greatest number of items returned per page is achieved when requesting `id` or `key` only.
            validateQuery (string): Determines how to validate the JQL query and treat the validation results. Supported values are: * `strict` Returns a 400 response code if any errors are found, along with a list of all errors (and warnings). * `warn` Returns all errors as warnings. * `none` No validation is performed. * `true` *Deprecated* A legacy synonym for `strict`. * `false` *Deprecated* A legacy synonym for `warn`. Note: If the JQL is not correctly formed a 400 response code is returned, regardless of the `validateQuery` value.
            fields (array): A list of fields to return for each issue, use it to retrieve a subset of fields. This parameter accepts a comma-separated list. Expand options include: * `*all` Returns all fields. * `*navigable` Returns navigable fields. * Any issue field, prefixed with a minus to exclude. Examples: * `summary,comment` Returns only the summary and comments fields. * `-description` Returns all navigable (default) fields except description. * `*all,-comment` Returns all fields except comments. This parameter may be specified multiple times. For example, `fields=field1,field2&fields=field3`. Note: All navigable fields are returned by default. This differs from [GET issue](#api-rest-api-3-issue-issueIdOrKey-get) where the default is all fields.
            expand (string): Use [expand](#expansion) to include additional information about issues in the response. This parameter accepts a comma-separated list. Expand options include: * `renderedFields` Returns field values rendered in HTML format. * `names` Returns the display name of each field. * `schema` Returns the schema describing a field type. * `transitions` Returns all possible transitions for the issue. * `operations` Returns all possible operations for the issue. * `editmeta` Returns information about how each field can be edited. * `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent. * `versionedRepresentations` Instead of `fields`, returns `versionedRepresentations` a JSON array containing each version of a field's value, with the highest numbered item representing the most recent version.
            properties (array): A list of issue property keys for issue properties to include in the results. This parameter accepts a comma-separated list. Multiple properties can also be provided using an ampersand separated list. For example, `properties=prop1,prop2&properties=prop3`. A maximum of 5 issue property keys can be specified.
            fieldsByKeys (boolean): Reference fields by their key (rather than ID).
            failFast (boolean): Whether to fail the request quickly in case of an error while loading fields for an issue. For `failFast=true`, if one field fails, the entire operation fails. For `failFast=false`, the operation will continue even if a field fails. It will return a valid response, but without values for the failed field(s).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        url = f"{self.base_url}/rest/api/3/search"
        query_params = {k: v for k, v in [('jql', jql), ('startAt', startAt), ('maxResults', maxResults), ('validateQuery', validateQuery), ('fields', fields), ('expand', expand), ('properties', properties), ('fieldsByKeys', fieldsByKeys), ('failFast', failFast)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_for_issues_using_jql_post(self, expand=None, fields=None, fieldsByKeys=None, jql=None, maxResults=None, properties=None, startAt=None, validateQuery=None) -> dict[str, Any]:
        """
        Searches Jira issues using JQL queries and returns paginated results.

        Args:
            expand (array): Use [expand](#expansion) to include additional information about issues in the response. Note that, unlike the majority of instances where `expand` is specified, `expand` is defined as a list of values. The expand options are:

         *  `renderedFields` Returns field values rendered in HTML format.
         *  `names` Returns the display name of each field.
         *  `schema` Returns the schema describing a field type.
         *  `transitions` Returns all possible transitions for the issue.
         *  `operations` Returns all possible operations for the issue.
         *  `editmeta` Returns information about how each field can be edited.
         *  `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent.
         *  `versionedRepresentations` Instead of `fields`, returns `versionedRepresentations` a JSON array containing each version of a field's value, with the highest numbered item representing the most recent version.
            fields (array): A list of fields to return for each issue, use it to retrieve a subset of fields. This parameter accepts a comma-separated list. Expand options include:

         *  `*all` Returns all fields.
         *  `*navigable` Returns navigable fields.
         *  Any issue field, prefixed with a minus to exclude.

        The default is `*navigable`.

        Examples:

         *  `summary,comment` Returns the summary and comments fields only.
         *  `-description` Returns all navigable (default) fields except description.
         *  `*all,-comment` Returns all fields except comments.

        Multiple `fields` parameters can be included in a request.

        Note: All navigable fields are returned by default. This differs from [GET issue](#api-rest-api-3-issue-issueIdOrKey-get) where the default is all fields.
            fieldsByKeys (boolean): Reference fields by their key (rather than ID). The default is `false`.
            jql (string): A [JQL](https://confluence.atlassian.com/x/egORLQ) expression.
            maxResults (integer): The maximum number of items to return per page.
            properties (array): A list of up to 5 issue properties to include in the results. This parameter accepts a comma-separated list.
            startAt (integer): The index of the first item to return in the page of results (page offset). The base index is `0`.
            validateQuery (string): Determines how to validate the JQL query and treat the validation results. Supported values:

         *  `strict` Returns a 400 response code if any errors are found, along with a list of all errors (and warnings).
         *  `warn` Returns all errors as warnings.
         *  `none` No validation is performed.
         *  `true` *Deprecated* A legacy synonym for `strict`.
         *  `false` *Deprecated* A legacy synonym for `warn`.

        The default is `strict`.

        Note: If the JQL is not correctly formed a 400 response code is returned, regardless of the `validateQuery` value.
                Example:
                ```json
                {
                  "expand": [
                    "names",
                    "schema",
                    "operations"
                  ],
                  "fields": [
                    "summary",
                    "status",
                    "assignee"
                  ],
                  "fieldsByKeys": false,
                  "jql": "project = HSP",
                  "maxResults": 15,
                  "startAt": 0
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        request_body = {
            'expand': expand,
            'fields': fields,
            'fieldsByKeys': fieldsByKeys,
            'jql': jql,
            'maxResults': maxResults,
            'properties': properties,
            'startAt': startAt,
            'validateQuery': validateQuery,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/search"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def count_issues(self, jql=None) -> dict[str, Any]:
        """
        Retrieves an approximate count of Jira issues matching a specified JQL query using the POST method at the "/rest/api/3/search/approximate-count" endpoint.

        Args:
            jql (string): A [JQL](https://confluence.atlassian.com/x/egORLQ) expression. For performance reasons, this parameter requires a bounded query. A bounded query is a query with a search restriction.
                Example:
                ```json
                {
                  "jql": "project = HSP"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        request_body = {
            'jql': jql,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/search/approximate-count"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_for_issues_ids(self, jql=None, maxResults=None, nextPageToken=None) -> dict[str, Any]:
        """
        Searches for Jira issues using JQL (Jira Query Language) and returns a list of matching issue IDs, along with a token for fetching additional results if needed, using the `POST` method at the path "/rest/api/3/search/id".

        Args:
            jql (string): A [JQL](https://confluence.atlassian.com/x/egORLQ) expression. Order by clauses are not allowed.
            maxResults (integer): The maximum number of items to return per page.
            nextPageToken (string): The continuation token to fetch the next page. This token is provided by the response of this endpoint.
                Example:
                ```json
                {
                  "jql": "project = HSP",
                  "maxResults": 1000,
                  "nextPageToken": "EgQIlMIC"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        request_body = {
            'jql': jql,
            'maxResults': maxResults,
            'nextPageToken': nextPageToken,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/search/id"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_and_reconsile_issues_using_jql(self, jql=None, nextPageToken=None, maxResults=None, fields=None, expand=None, properties=None, fieldsByKeys=None, failFast=None, reconcileIssues=None) -> dict[str, Any]:
        """
        Retrieves a list of Jira issues matching a JQL query with pagination support, customizable field selection, and result optimization options.

        Args:
            jql (string): A [JQL]( expression. For performance reasons, this parameter requires a bounded query. A bounded query is a query with a search restriction. * Example of an unbounded query: `order by key desc`. * Example of a bounded query: `assignee = currentUser() order by key`. Additionally, `orderBy` clause can contain a maximum of 7 fields. Example: 'project = HSP'.
            nextPageToken (string): The token for a page to fetch that is not the first page. The first page has a `nextPageToken` of `null`. Use the `nextPageToken` to fetch the next page of issues. Note: The `nextPageToken` field is **not included** in the response for the last page, indicating there is no next page. Example: '<string>'.
            maxResults (integer): The maximum number of items to return per page. To manage page size, API may return fewer items per page where a large number of fields or properties are requested. The greatest number of items returned per page is achieved when requesting `id` or `key` only. It returns max 5000 issues. Example: '114'.
            fields (array): A list of fields to return for each issue, use it to retrieve a subset of fields. This parameter accepts a comma-separated list. Expand options include: * `*all` Returns all fields. * `*navigable` Returns navigable fields. * `id` Returns only issue IDs. * Any issue field, prefixed with a minus to exclude. The default is `id`. Examples: * `summary,comment` Returns only the summary and comments fields only. * `-description` Returns all navigable (default) fields except description. * `*all,-comment` Returns all fields except comments. Multiple `fields` parameters can be included in a request. Note: By default, this resource returns IDs only. This differs from [GET issue](#api-rest-api-3-issue-issueIdOrKey-get) where the default is all fields.
            expand (string): Use [expand](#expansion) to include additional information about issues in the response. Note that, unlike the majority of instances where `expand` is specified, `expand` is defined as a comma-delimited string of values. The expand options are: * `renderedFields` Returns field values rendered in HTML format. * `names` Returns the display name of each field. * `schema` Returns the schema describing a field type. * `transitions` Returns all possible transitions for the issue. * `operations` Returns all possible operations for the issue. * `editmeta` Returns information about how each field can be edited. * `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent. * `versionedRepresentations` Instead of `fields`, returns `versionedRepresentations` a JSON array containing each version of a field's value, with the highest numbered item representing the most recent version. Examples: `"names,changelog"` Returns the display name of each field as well as a list of recent updates to an issue. Example: '<string>'.
            properties (array): A list of up to 5 issue properties to include in the results. This parameter accepts a comma-separated list.
            fieldsByKeys (boolean): Reference fields by their key (rather than ID). The default is `false`.
            failFast (boolean): Fail this request early if we can't retrieve all field data.
            reconcileIssues (array): Strong consistency issue ids to be reconciled with search results. Accepts max 50 ids

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        url = f"{self.base_url}/rest/api/3/search/jql"
        query_params = {k: v for k, v in [('jql', jql), ('nextPageToken', nextPageToken), ('maxResults', maxResults), ('fields', fields), ('expand', expand), ('properties', properties), ('fieldsByKeys', fieldsByKeys), ('failFast', failFast), ('reconcileIssues', reconcileIssues)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_and_reconsile_issues_using_jql_post(self, expand=None, fields=None, fieldsByKeys=None, jql=None, maxResults=None, nextPageToken=None, properties=None, reconcileIssues=None) -> dict[str, Any]:
        """
        Executes a JQL query to search for issues, returning matching results and pagination tokens.

        Args:
            expand (string): Use [expand](#expansion) to include additional information about issues in the response. Note that, unlike the majority of instances where `expand` is specified, `expand` is defined as a comma-delimited string of values. The expand options are:

         *  `renderedFields` Returns field values rendered in HTML format.
         *  `names` Returns the display name of each field.
         *  `schema` Returns the schema describing a field type.
         *  `transitions` Returns all possible transitions for the issue.
         *  `operations` Returns all possible operations for the issue.
         *  `editmeta` Returns information about how each field can be edited.
         *  `changelog` Returns a list of recent updates to an issue, sorted by date, starting from the most recent.
         *  `versionedRepresentations` Instead of `fields`, returns `versionedRepresentations` a JSON array containing each version of a field's value, with the highest numbered item representing the most recent version.

        Examples: `"names,changelog"` Returns the display name of each field as well as a list of recent updates to an issue.
            fields (array): A list of fields to return for each issue. Use it to retrieve a subset of fields. This parameter accepts a comma-separated list. Expand options include:

         *  `*all` Returns all fields.
         *  `*navigable` Returns navigable fields.
         *  `id` Returns only issue IDs.
         *  Any issue field, prefixed with a dash to exclude.

        The default is `id`.

        Examples:

         *  `summary,comment` Returns the summary and comments fields only.
         *  `*all,-comment` Returns all fields except comments.

        Multiple `fields` parameters can be included in a request.

        Note: By default, this resource returns IDs only. This differs from [GET issue](#api-rest-api-3-issue-issueIdOrKey-get) where the default is all fields.
            fieldsByKeys (boolean): Reference fields by their key (rather than ID). The default is `false`.
            jql (string): A [JQL](https://confluence.atlassian.com/x/egORLQ) expression. For performance reasons, this parameter requires a bounded query. A bounded query is a query with a search restriction.

         *  Example of an unbounded query: `order by key desc`.
         *  Example of a bounded query: `assignee = currentUser() order by key`.

        Additionally, `orderBy` clause can contain a maximum of 7 fields.
            maxResults (integer): The maximum number of items to return per page. To manage page size, API may return fewer items per page where a large number of fields are requested. The greatest number of items returned per page is achieved when requesting `id` or `key` only. It returns max 5000 issues.
            nextPageToken (string): The token for a page to fetch that is not the first page. The first page has a `nextPageToken` of `null`. Use the `nextPageToken` to fetch the next page of issues.
            properties (array): A list of up to 5 issue properties to include in the results. This parameter accepts a comma-separated list.
            reconcileIssues (array): Strong consistency issue ids to be reconciled with search results. Accepts max 50 ids

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue search
        """
        request_body = {
            'expand': expand,
            'fields': fields,
            'fieldsByKeys': fieldsByKeys,
            'jql': jql,
            'maxResults': maxResults,
            'nextPageToken': nextPageToken,
            'properties': properties,
            'reconcileIssues': reconcileIssues,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/search/jql"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_security_level(self, id) -> dict[str, Any]:
        """
        Retrieves details of a specific issue security level by its ID in Jira.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue security level
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/securitylevel/{id}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_server_info(self) -> dict[str, Any]:
        """
        Retrieves information about the Jira instance using the "GET" method at the "/rest/api/3/serverInfo" endpoint.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Server info
        """
        url = f"{self.base_url}/rest/api/3/serverInfo"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_issue_navigator_default_columns(self) -> list[Any]:
        """
        Retrieves settings for columns using the Jira API and returns relevant data.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue navigator settings
        """
        url = f"{self.base_url}/rest/api/3/settings/columns"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def get_statuses(self) -> list[Any]:
        """
        Retrieves the operational status and readiness of the Jira instance via a lightweight endpoint for monitoring.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Workflow statuses
        """
        url = f"{self.base_url}/rest/api/3/status"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_status(self, idOrName) -> dict[str, Any]:
        """
        Retrieves a specific status by its ID or name from Jira using the Jira REST API.

        Args:
            idOrName (string): idOrName

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow statuses
        """
        if idOrName is None:
            raise ValueError("Missing required parameter 'idOrName'")
        url = f"{self.base_url}/rest/api/3/status/{idOrName}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_status_categories(self) -> list[Any]:
        """
        Retrieves a list of all visible Jira issue status categories in JSON format.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Workflow status categories
        """
        url = f"{self.base_url}/rest/api/3/statuscategory"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_status_category(self, idOrKey) -> dict[str, Any]:
        """
        Retrieves a specific Jira issue status category by its ID or key using the GET method.

        Args:
            idOrKey (string): idOrKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow status categories
        """
        if idOrKey is None:
            raise ValueError("Missing required parameter 'idOrKey'")
        url = f"{self.base_url}/rest/api/3/statuscategory/{idOrKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_statuses_by_id(self, id) -> Any:
        """
        Deletes a specific status entry identified by its ID using the provided parameters and returns a success or error code.

        Args:
            id (array): The list of status IDs. To include multiple IDs, provide an ampersand-separated list. For example, id=10000&id=10001. Min items `1`, Max items `50`

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Status
        """
        url = f"{self.base_url}/rest/api/3/statuses"
        query_params = {k: v for k, v in [('id', id)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_statuses_by_id(self, id, expand=None) -> list[Any]:
        """
        Retrieves a list of statuses in Jira using the "/rest/api/3/statuses" endpoint, allowing you to fetch details of statuses based on query parameters like expansion and ID, though specific details about what statuses are returned are not provided.

        Args:
            id (array): The list of status IDs. To include multiple IDs, provide an ampersand-separated list. For example, id=10000&id=10001. Min items `1`, Max items `50`
            expand (string): Deprecated. See the [deprecation notice]( for details. Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `usages` Returns the project and issue types that use the status in their workflow. * `workflowUsages` Returns the workflows that use the status.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Status
        """
        url = f"{self.base_url}/rest/api/3/statuses"
        query_params = {k: v for k, v in [('expand', expand), ('id', id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_statuses(self, scope, statuses) -> list[Any]:
        """
        Creates commit statuses (error, failure, pending, success) with optional descriptions and target URLs via the GitHub API.

        Args:
            scope (object): The scope of the status.
            statuses (array): Details of the statuses being created.
                Example:
                ```json
                {
                  "scope": {
                    "project": {
                      "id": "1"
                    },
                    "type": "PROJECT"
                  },
                  "statuses": [
                    {
                      "description": "The issue is resolved",
                      "name": "Finished",
                      "statusCategory": "DONE"
                    }
                  ]
                }
                ```

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Status
        """
        request_body = {
            'scope': scope,
            'statuses': statuses,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/statuses"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_statuses(self, statuses) -> Any:
        """
        Updates the statuses in Jira using the PUT method at the "/rest/api/3/statuses" endpoint and returns a status message.

        Args:
            statuses (array): The list of statuses that will be updated.
                Example:
                ```json
                {
                  "statuses": [
                    {
                      "description": "The issue is resolved",
                      "id": "1000",
                      "name": "Finished",
                      "statusCategory": "DONE"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Status
        """
        request_body = {
            'statuses': statuses,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/statuses"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search(self, expand=None, projectId=None, startAt=None, maxResults=None, searchString=None, statusCategory=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of Jira statuses with optional filtering by project, search string, or status category.

        Args:
            expand (string): Deprecated. See the [deprecation notice]( for details. Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `usages` Returns the project and issue types that use the status in their workflow. * `workflowUsages` Returns the workflows that use the status.
            projectId (string): The project the status is part of or null for global statuses.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            searchString (string): Term to match status names against or null to search for all statuses in the search scope.
            statusCategory (string): Category of the status to filter by. The supported values are: `TODO`, `IN_PROGRESS`, and `DONE`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Status
        """
        url = f"{self.base_url}/rest/api/3/statuses/search"
        query_params = {k: v for k, v in [('expand', expand), ('projectId', projectId), ('startAt', startAt), ('maxResults', maxResults), ('searchString', searchString), ('statusCategory', statusCategory)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_issue_type_usages_for_status(self, statusId, projectId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of issue types associated with a specific project and status, including pagination controls via `nextPageToken` and `maxResults`.

        Args:
            statusId (string): statusId
            projectId (string): projectId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Status
        """
        if statusId is None:
            raise ValueError("Missing required parameter 'statusId'")
        if projectId is None:
            raise ValueError("Missing required parameter 'projectId'")
        url = f"{self.base_url}/rest/api/3/statuses/{statusId}/project/{projectId}/issueTypeUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_usages_for_status(self, statusId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves project usage information for a specific status identified by the status ID, supporting pagination through optional parameters for the next page token and maximum results.

        Args:
            statusId (string): statusId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Status
        """
        if statusId is None:
            raise ValueError("Missing required parameter 'statusId'")
        url = f"{self.base_url}/rest/api/3/statuses/{statusId}/projectUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_usages_for_status(self, statusId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves the workflows associated with a specific status ID and returns their usage details.

        Args:
            statusId (string): statusId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Status
        """
        if statusId is None:
            raise ValueError("Missing required parameter 'statusId'")
        url = f"{self.base_url}/rest/api/3/statuses/{statusId}/workflowUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_task(self, taskId) -> dict[str, Any]:
        """
        Retrieves details for a specific task by ID using a REST API GET request.

        Args:
            taskId (string): taskId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Tasks
        """
        if taskId is None:
            raise ValueError("Missing required parameter 'taskId'")
        url = f"{self.base_url}/rest/api/3/task/{taskId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def cancel_task(self, taskId) -> Any:
        """
        Cancels a specific task by its ID using the POST method at the "/rest/api/3/task/{taskId}/cancel" path.

        Args:
            taskId (string): taskId

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Tasks
        """
        if taskId is None:
            raise ValueError("Missing required parameter 'taskId'")
        url = f"{self.base_url}/rest/api/3/task/{taskId}/cancel"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_ui_modifications(self, startAt=None, maxResults=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of UI modifications (including project, issue type, and view contexts) from Jira's REST API.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            expand (string): Use expand to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `data` Returns UI modification data. * `contexts` Returns UI modification contexts.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            UI modifications (apps)
        """
        url = f"{self.base_url}/rest/api/3/uiModifications"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_ui_modification(self, name, contexts=None, data=None, description=None) -> dict[str, Any]:
        """
        Applies modifications to the user interface using the REST API at the "/rest/api/3/uiModifications" endpoint, returning status codes to indicate success or failure.

        Args:
            name (string): The name of the UI modification. The maximum length is 255 characters.
            contexts (array): List of contexts of the UI modification. The maximum number of contexts is 1000.
            data (string): The data of the UI modification. The maximum size of the data is 50000 characters.
            description (string): The description of the UI modification. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "contexts": [
                    {
                      "issueTypeId": "10000",
                      "projectId": "10000",
                      "viewType": "GIC"
                    },
                    {
                      "issueTypeId": "10001",
                      "projectId": "10000",
                      "viewType": "IssueView"
                    },
                    {
                      "issueTypeId": "10002",
                      "projectId": "10000",
                      "viewType": "IssueTransition"
                    },
                    {
                      "issueTypeId": "10003",
                      "projectId": "10000",
                      "viewType": null
                    }
                  ],
                  "data": "{field: 'Story Points', config: {hidden: false}}",
                  "description": "Reveals Story Points field when any Sprint is selected.",
                  "name": "Reveal Story Points"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the UI modification is created.

        Tags:
            UI modifications (apps)
        """
        request_body = {
            'contexts': contexts,
            'data': data,
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/uiModifications"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_ui_modification(self, uiModificationId) -> Any:
        """
        Deletes a UI modification with the specified ID from the system using the DELETE HTTP method.

        Args:
            uiModificationId (string): uiModificationId

        Returns:
            Any: Returned if the UI modification is deleted.

        Tags:
            UI modifications (apps)
        """
        if uiModificationId is None:
            raise ValueError("Missing required parameter 'uiModificationId'")
        url = f"{self.base_url}/rest/api/3/uiModifications/{uiModificationId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_ui_modification(self, uiModificationId, contexts=None, data=None, description=None, name=None) -> Any:
        """
        Updates a UI modification identified by `uiModificationId` using the PUT method.

        Args:
            uiModificationId (string): uiModificationId
            contexts (array): List of contexts of the UI modification. The maximum number of contexts is 1000. If provided, replaces all existing contexts.
            data (string): The data of the UI modification. The maximum size of the data is 50000 characters.
            description (string): The description of the UI modification. The maximum length is 255 characters.
            name (string): The name of the UI modification. The maximum length is 255 characters.
                Example:
                ```json
                {
                  "contexts": [
                    {
                      "issueTypeId": "10000",
                      "projectId": "10000",
                      "viewType": "GIC"
                    },
                    {
                      "issueTypeId": "10001",
                      "projectId": "10000",
                      "viewType": "IssueView"
                    },
                    {
                      "issueTypeId": "10002",
                      "projectId": "10000",
                      "viewType": "IssueTransition"
                    }
                  ],
                  "data": "{field: 'Story Points', config: {hidden: true}}",
                  "name": "Updated Reveal Story Points"
                }
                ```

        Returns:
            Any: Returned if the UI modification is updated.

        Tags:
            UI modifications (apps)
        """
        if uiModificationId is None:
            raise ValueError("Missing required parameter 'uiModificationId'")
        request_body = {
            'contexts': contexts,
            'data': data,
            'description': description,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/uiModifications/{uiModificationId}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_avatars(self, type, entityId) -> dict[str, Any]:
        """
        Retrieves details about a universal avatar by its type and owner entity ID using the Jira API.

        Args:
            type (string): type
            entityId (string): entityId

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        if entityId is None:
            raise ValueError("Missing required parameter 'entityId'")
        url = f"{self.base_url}/rest/api/3/universal_avatar/type/{type}/owner/{entityId}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def delete_avatar(self, type, owningObjectId, id) -> Any:
        """
        Deletes a specified avatar associated with a resource type and owner using the Jira API.

        Args:
            type (string): type
            owningObjectId (string): owningObjectId
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        if owningObjectId is None:
            raise ValueError("Missing required parameter 'owningObjectId'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_avatar_image_by_type(self, type, size=None, format=None) -> dict[str, Any]:
        """
        Retrieves a Jira avatar image by type using the "GET" method, allowing specification of size and format for customization.

        Args:
            type (string): type
            size (string): The size of the avatar image. If not provided the default size is returned.
            format (string): The format to return the avatar image in. If not provided the original content format is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        url = f"{self.base_url}/rest/api/3/universal_avatar/view/type/{type}"
        query_params = {k: v for k, v in [('size', size), ('format', format)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_avatar_image_by_id(self, type, id, size=None, format=None) -> dict[str, Any]:
        """
        Retrieves a specific avatar by type and ID using the Jira Universal Avatar API, allowing customization and display in various formats and sizes.

        Args:
            type (string): type
            id (string): id
            size (string): The size of the avatar image. If not provided the default size is returned.
            format (string): The format to return the avatar image in. If not provided the original content format is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/universal_avatar/view/type/{type}/avatar/{id}"
        query_params = {k: v for k, v in [('size', size), ('format', format)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_avatar_image_by_owner(self, type, entityId, size=None, format=None) -> dict[str, Any]:
        """
        Retrieves an avatar image for a specified owner entity (like user, project, or issue type) by type and ID, allowing optional size and format customization.

        Args:
            type (string): type
            entityId (string): entityId
            size (string): The size of the avatar image. If not provided the default size is returned.
            format (string): The format to return the avatar image in. If not provided the original content format is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Avatars
        """
        if type is None:
            raise ValueError("Missing required parameter 'type'")
        if entityId is None:
            raise ValueError("Missing required parameter 'entityId'")
        url = f"{self.base_url}/rest/api/3/universal_avatar/view/type/{type}/owner/{entityId}"
        query_params = {k: v for k, v in [('size', size), ('format', format)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def remove_user(self, accountId, username=None, key=None) -> Any:
        """
        Deletes a user from the system using the provided query parameters such as account ID, username, or key, and returns a status code indicating success or failure.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            key (string): This parameter is no longer available. See the [deprecation notice]( for details.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user"
        query_params = {k: v for k, v in [('accountId', accountId), ('username', username), ('key', key)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user(self, accountId=None, username=None, key=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a specific Jira user's details using the provided account ID, username, or user key via the Jira REST API.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Required. Example: '5b10ac8d82e05b22cc7d4ef5'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            key (string): This parameter is no longer available. See the [deprecation notice]( for details.
            expand (string): Use [expand](#expansion) to include additional information about users in the response. This parameter accepts a comma-separated list. Expand options include: * `groups` includes all groups and nested groups to which the user belongs. * `applicationRoles` includes details of all the applications to which the user has access.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user"
        query_params = {k: v for k, v in [('accountId', accountId), ('username', username), ('key', key), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_user(self, emailAddress, products, applicationKeys=None, displayName=None, key=None, name=None, password=None, self_arg_body=None) -> dict[str, Any]:
        """
        Creates a new user in Jira and returns the created user resource upon success.

        Args:
            emailAddress (string): The email address for the user.
            products (array): Products the new user has access to. Valid products are: jira-core, jira-servicedesk, jira-product-discovery, jira-software. To create a user without product access, set this field to be an empty array.
            applicationKeys (array): Deprecated, do not use.
            displayName (string): This property is no longer available. If the user has an Atlassian account, their display name is not changed. If the user does not have an Atlassian account, they are sent an email asking them set up an account.
            key (string): This property is no longer available. See the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            name (string): This property is no longer available. See the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/) for details.
            password (string): This property is no longer available. If the user has an Atlassian account, their password is not changed. If the user does not have an Atlassian account, they are sent an email asking them set up an account.
            self_arg_body (string): The URL of the user.
                Example:
                ```json
                {
                  "emailAddress": "mia@atlassian.com"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Users
        """
        request_body = {
            'applicationKeys': applicationKeys,
            'displayName': displayName,
            'emailAddress': emailAddress,
            'key': key,
            'name': name,
            'password': password,
            'products': products,
            'self': self_arg_body,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/user"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_bulk_assignable_users(self, projectKeys, query=None, username=None, accountId=None, startAt=None, maxResults=None) -> list[Any]:
        """
        Retrieves a list of users who can be assigned issues in one or more specified projects, allowing filtering by various user attributes such as name or account ID.

        Args:
            projectKeys (string): A list of project keys (case sensitive). This parameter accepts a comma-separated list.
            query (string): A query string that is matched against user attributes, such as `displayName` and `emailAddress`, to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*. Required, unless `accountId` is specified. Example: 'query'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            accountId (string): A query string that is matched exactly against user `accountId`. Required, unless `query` is specified.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/assignable/multiProjectSearch"
        query_params = {k: v for k, v in [('query', query), ('username', username), ('accountId', accountId), ('projectKeys', projectKeys), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_assignable_users(self, query=None, sessionId=None, username=None, accountId=None, project=None, issueKey=None, issueId=None, startAt=None, maxResults=None, actionDescriptorId=None, recommend=None) -> list[Any]:
        """
        Searches for users who can be assigned to issues in Jira, allowing filtering by query, session ID, username, account ID, project, issue key, issue ID, and other parameters, returning a list of assignable users.

        Args:
            query (string): A query string that is matched against user attributes, such as `displayName`, and `emailAddress`, to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*. Required, unless `username` or `accountId` is specified. Example: 'query'.
            sessionId (string): The sessionId of this request. SessionId is the same until the assignee is set.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            accountId (string): A query string that is matched exactly against user `accountId`. Required, unless `query` is specified.
            project (string): The project ID or project key (case sensitive). Required, unless `issueKey` or `issueId` is specified.
            issueKey (string): The key of the issue. Required, unless `issueId` or `project` is specified.
            issueId (string): The ID of the issue. Required, unless `issueKey` or `project` is specified.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return. This operation may return less than the maximum number of items even if more are available. The operation fetches users up to the maximum and then, from the fetched users, returns only the users that can be assigned to the issue.
            actionDescriptorId (integer): The ID of the transition.
            recommend (boolean): The `recommend` parameter is used to influence the recommendation of users when searching for assignable users, potentially providing suggestions based on user activity or other relevant factors.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/assignable/search"
        query_params = {k: v for k, v in [('query', query), ('sessionId', sessionId), ('username', username), ('accountId', accountId), ('project', project), ('issueKey', issueKey), ('issueId', issueId), ('startAt', startAt), ('maxResults', maxResults), ('actionDescriptorId', actionDescriptorId), ('recommend', recommend)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_get_users(self, accountId, startAt=None, maxResults=None, username=None, key=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of user details for specified account IDs using the Jira REST API.

        Args:
            accountId (array): The account ID of a user. To specify multiple users, pass multiple `accountId` parameters. For example, `accountId=5b10a2844c20165700ede21g&accountId=5b10ac8d82e05b22cc7d4ef5`. Example: '5b10ac8d82e05b22cc7d4ef5'.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            username (array): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.
            key (array): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/bulk"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('username', username), ('key', key), ('accountId', accountId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def bulk_get_users_migration(self, startAt=None, maxResults=None, username=None, key=None) -> list[Any]:
        """
        Retrieves user migration information in bulk for Jira using the GET method, allowing filtering by username, key, and pagination via startAt and maxResults parameters.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            username (array): Username of a user. To specify multiple users, pass multiple copies of this parameter. For example, `username=fred&username=barney`. Required if `key` isn't provided. Cannot be provided if `key` is present.
            key (array): Key of a user. To specify multiple users, pass multiple copies of this parameter. For example, `key=fred&key=barney`. Required if `username` isn't provided. Cannot be provided if `username` is present.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/bulk/migration"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('username', username), ('key', key)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def reset_user_columns(self, accountId=None, username=None) -> Any:
        """
        Deletes a user's saved column configuration in Jira based on either their account ID or username.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/columns"
        query_params = {k: v for k, v in [('accountId', accountId), ('username', username)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_default_columns(self, accountId=None, username=None) -> list[Any]:
        """
        Retrieves the default issue table columns for a Jira user, specified by either an accountId or the calling user if no accountId is provided, using the Jira Cloud Platform REST API.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            username (string): This parameter is no longer available See the [deprecation notice]( for details.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/columns"
        query_params = {k: v for k, v in [('accountId', accountId), ('username', username)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_email(self, accountId) -> dict[str, Any]:
        """
        Retrieves a user's email address for the specified Atlassian account ID using the Jira Cloud API.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, `5b10ac8d82e05b22cc7d4ef5`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/email"
        query_params = {k: v for k, v in [('accountId', accountId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_email_bulk(self, accountId) -> dict[str, Any]:
        """
        Retrieves email addresses for multiple Jira users by their account IDs in a single request, bypassing profile visibility restrictions.

        Args:
            accountId (array): The account IDs of the users for which emails are required. An `accountId` is an identifier that uniquely identifies the user across all Atlassian products. For example, `5b10ac8d82e05b22cc7d4ef5`. Note, this should be treated as an opaque identifier (that is, do not assume any structure in the value).

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/email/bulk"
        query_params = {k: v for k, v in [('accountId', accountId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_groups(self, accountId, username=None, key=None) -> list[Any]:
        """
        Retrieves a list of groups associated with a specified Jira user account using their accountId, username, or key.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            key (string): This parameter is no longer available. See the [deprecation notice]( for details.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/user/groups"
        query_params = {k: v for k, v in [('accountId', accountId), ('username', username), ('key', key)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_nav_property(self, propertyKey, accountId=None) -> dict[str, Any]:
        """
        Retrieves the value associated with a specified property key for a given account using the GET method.

        Args:
            propertyKey (string): propertyKey
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            usernavproperties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/user/nav4-opt-property/{propertyKey}"
        query_params = {k: v for k, v in [('accountId', accountId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_with_all_permissions(self, permissions, query=None, username=None, accountId=None, issueKey=None, projectKey=None, startAt=None, maxResults=None) -> list[Any]:
        """
        Retrieves users with specified global or project permissions, filtered by query, account ID, or project/issue context, including pagination support.

        Args:
            permissions (string): A comma separated list of permissions. Permissions can be specified as any: * permission returned by [Get all permissions](#api-rest-api-3-permissions-get). * custom project permission added by Connect apps. * (deprecated) one of the following: * ASSIGNABLE\_USER * ASSIGN\_ISSUE * ATTACHMENT\_DELETE\_ALL * ATTACHMENT\_DELETE\_OWN * BROWSE * CLOSE\_ISSUE * COMMENT\_DELETE\_ALL * COMMENT\_DELETE\_OWN * COMMENT\_EDIT\_ALL * COMMENT\_EDIT\_OWN * COMMENT\_ISSUE * CREATE\_ATTACHMENT * CREATE\_ISSUE * DELETE\_ISSUE * EDIT\_ISSUE * LINK\_ISSUE * MANAGE\_WATCHER\_LIST * MODIFY\_REPORTER * MOVE\_ISSUE * PROJECT\_ADMIN * RESOLVE\_ISSUE * SCHEDULE\_ISSUE * SET\_ISSUE\_SECURITY * TRANSITION\_ISSUE * VIEW\_VERSION\_CONTROL * VIEW\_VOTERS\_AND\_WATCHERS * VIEW\_WORKFLOW\_READONLY * WORKLOG\_DELETE\_ALL * WORKLOG\_DELETE\_OWN * WORKLOG\_EDIT\_ALL * WORKLOG\_EDIT\_OWN * WORK\_ISSUE
            query (string): A query string that is matched against user attributes, such as `displayName` and `emailAddress`, to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*. Required, unless `accountId` is specified. Example: 'query'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            accountId (string): A query string that is matched exactly against user `accountId`. Required, unless `query` is specified.
            issueKey (string): The issue key for the issue.
            projectKey (string): The project key for the project (case sensitive).
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/permission/search"
        query_params = {k: v for k, v in [('query', query), ('username', username), ('accountId', accountId), ('permissions', permissions), ('issueKey', issueKey), ('projectKey', projectKey), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_for_picker(self, query, maxResults=None, showAvatar=None, exclude=None, excludeAccountIds=None, avatarSize=None, excludeConnectUsers=None) -> dict[str, Any]:
        """
        Retrieves a list of users and groups for a picker field, allowing filtering by query, exclusion parameters, and pagination, to populate user or group suggestion lists in Jira applications.

        Args:
            query (string): A query string that is matched against user attributes, such as `displayName`, and `emailAddress`, to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*.
            maxResults (integer): The maximum number of items to return. The total number of matched users is returned in `total`.
            showAvatar (boolean): Include the URI to the user's avatar.
            exclude (array): This parameter is no longer available. See the [deprecation notice]( for details.
            excludeAccountIds (array): A list of account IDs to exclude from the search results. This parameter accepts a comma-separated list. Multiple account IDs can also be provided using an ampersand-separated list. For example, `excludeAccountIds=5b10a2844c20165700ede21g,5b10a0effa615349cb016cd8&excludeAccountIds=5b10ac8d82e05b22cc7d4ef5`. Cannot be provided with `exclude`.
            avatarSize (string): Specifies the size of the avatar to be returned in the response, typically in pixels (e.g., 16x16, 24x24, 32x32, or 48x48).
            excludeConnectUsers (boolean): A boolean parameter to exclude JSM customer accounts from the search results when set to true.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/picker"
        query_params = {k: v for k, v in [('query', query), ('maxResults', maxResults), ('showAvatar', showAvatar), ('exclude', exclude), ('excludeAccountIds', excludeAccountIds), ('avatarSize', avatarSize), ('excludeConnectUsers', excludeConnectUsers)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_property_keys(self, accountId=None, userKey=None, username=None) -> dict[str, Any]:
        """
        Retrieves the keys of all properties for a user using the Jira Cloud REST API.

        Args:
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            userKey (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.
            username (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            User properties
        """
        url = f"{self.base_url}/rest/api/3/user/properties"
        query_params = {k: v for k, v in [('accountId', accountId), ('userKey', userKey), ('username', username)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_user_property(self, propertyKey, accountId=None, userKey=None, username=None) -> Any:
        """
        Deletes a user property identified by a specific property key using the Jira Cloud platform REST API, requiring permissions to manage user properties.

        Args:
            propertyKey (string): propertyKey
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            userKey (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.
            username (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.

        Returns:
            Any: Returned if the user property is deleted.

        Tags:
            User properties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/user/properties/{propertyKey}"
        query_params = {k: v for k, v in [('accountId', accountId), ('userKey', userKey), ('username', username)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_property(self, propertyKey, accountId=None, userKey=None, username=None) -> dict[str, Any]:
        """
        Retrieves the value of a specified user property using the Jira Cloud API, returning the custom data associated with a user for a given property key.

        Args:
            propertyKey (string): propertyKey
            accountId (string): The account ID of the user, which uniquely identifies the user across all Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Example: '5b10ac8d82e05b22cc7d4ef5'.
            userKey (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.
            username (string): This parameter is no longer available and will be removed from the documentation soon. See the [deprecation notice]( for details.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            User properties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/api/3/user/properties/{propertyKey}"
        query_params = {k: v for k, v in [('accountId', accountId), ('userKey', userKey), ('username', username)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def find_users(self, query=None, username=None, accountId=None, startAt=None, maxResults=None, property=None) -> list[Any]:
        """
        Searches for Jira users by matching a query against display names and email addresses, supporting pagination and specific property filters.

        Args:
            query (string): A query string that is matched against user attributes ( `displayName`, and `emailAddress`) to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*. Required, unless `accountId` or `property` is specified. Example: 'query'.
            username (string): The "username" parameter is not explicitly documented in the `/rest/api/3/user/search` endpoint. Instead, the "query" parameter is used, which matches against user attributes like `displayName` and `emailAddress`. However, if "username" were to be considered, it would presumably involve searching for users based on their username or similar attributes, though this is not the standard behavior of the current API.
            accountId (string): A query string that is matched exactly against a user `accountId`. Required, unless `query` or `property` is specified.
            startAt (integer): The index of the first item to return in a page of filtered results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            property (string): A query string used to search properties. Property keys are specified by path, so property keys containing dot (.) or equals (=) characters cannot be used. The query string cannot be specified using a JSON object. Example: To search for the value of `nested` from `{"something":{"nested":1,"other":2}}` use `thepropertykey.something.nested=1`. Required, unless `accountId` or `query` is specified.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/search"
        query_params = {k: v for k, v in [('query', query), ('username', username), ('accountId', accountId), ('startAt', startAt), ('maxResults', maxResults), ('property', property)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_by_query(self, query, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Searches for users in Jira based on query parameters, returning paginated results.

        Args:
            query (string): The search query.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/search/query"
        query_params = {k: v for k, v in [('query', query), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_user_keys_by_query(self, query, startAt=None, maxResult=None) -> dict[str, Any]:
        """
        Searches for users based on a specified query, returning a list of matching users, with options to control the result set size and starting point.

        Args:
            query (string): The search query.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResult (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/search/query/key"
        query_params = {k: v for k, v in [('query', query), ('startAt', startAt), ('maxResult', maxResult)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_with_browse_permission(self, query=None, username=None, accountId=None, issueKey=None, projectKey=None, startAt=None, maxResults=None) -> list[Any]:
        """
        Searches for Jira issues based on specified parameters such as query, username, account ID, issue key, project key, and returns a list of matching issues with pagination options.

        Args:
            query (string): A query string that is matched against user attributes, such as `displayName` and `emailAddress`, to find relevant users. The string can match the prefix of the attribute's value. For example, *query=john* matches a user with a `displayName` of *John Smith* and a user with an `emailAddress` of *johnson@example.com*. Required, unless `accountId` is specified. Example: 'query'.
            username (string): This parameter is no longer available. See the [deprecation notice]( for details.
            accountId (string): A query string that is matched exactly against user `accountId`. Required, unless `query` is specified.
            issueKey (string): The issue key for the issue. Required, unless `projectKey` is specified.
            projectKey (string): The project key for the project (case sensitive). Required, unless `issueKey` is specified.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            User search
        """
        url = f"{self.base_url}/rest/api/3/user/viewissue/search"
        query_params = {k: v for k, v in [('query', query), ('username', username), ('accountId', accountId), ('issueKey', issueKey), ('projectKey', projectKey), ('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_users_default(self, startAt=None, maxResults=None) -> list[Any]:
        """
        Retrieves a list of Jira users, supporting pagination via the `startAt` and `maxResults` parameters, using the GET method at the `/rest/api/3/users` endpoint.

        Args:
            startAt (integer): The index of the first item to return.
            maxResults (integer): The maximum number of items to return.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/users"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_users(self, startAt=None, maxResults=None) -> list[Any]:
        """
        Searches for Jira users matching query criteria and returns paginated results.

        Args:
            startAt (integer): The index of the first item to return.
            maxResults (integer): The maximum number of items to return.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Users
        """
        url = f"{self.base_url}/rest/api/3/users/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_version(self, approvers=None, archived=None, description=None, driver=None, expand=None, id=None, issuesStatusForFixVersion=None, moveUnfixedIssuesTo=None, name=None, operations=None, overdue=None, project=None, projectId=None, releaseDate=None, released=None, self_arg_body=None, startDate=None, userReleaseDate=None, userStartDate=None) -> dict[str, Any]:
        """
        Creates a new project version in Jira and returns the details of the created version.

        Args:
            approvers (array): If the expand option `approvers` is used, returns a list containing the approvers for this version.
            archived (boolean): Indicates that the version is archived. Optional when creating or updating a version.
            description (string): The description of the version. Optional when creating or updating a version. The maximum size is 16,384 bytes.
            driver (string): If the expand option `driver` is used, returns the Atlassian account ID of the driver.
            expand (string): Use [expand](em>#expansion) to include additional information about version in the response. This parameter accepts a comma-separated list. Expand options include:

         *  `operations` Returns the list of operations available for this version.
         *  `issuesstatus` Returns the count of issues in this version for each of the status categories *to do*, *in progress*, *done*, and *unmapped*. The *unmapped* property contains a count of issues with a status other than *to do*, *in progress*, and *done*.
         *  `driver` Returns the Atlassian account ID of the version driver.
         *  `approvers` Returns a list containing approvers for this version.

        Optional for create and update.
            id (string): The ID of the version.
            issuesStatusForFixVersion (string): If the expand option `issuesstatus` is used, returns the count of issues in this version for each of the status categories *to do*, *in progress*, *done*, and *unmapped*. The *unmapped* property contains a count of issues with a status other than *to do*, *in progress*, and *done*.
            moveUnfixedIssuesTo (string): The URL of the self link to the version to which all unfixed issues are moved when a version is released. Not applicable when creating a version. Optional when updating a version.
            name (string): The unique name of the version. Required when creating a version. Optional when updating a version. The maximum length is 255 characters.
            operations (array): If the expand option `operations` is used, returns the list of operations available for this version.
            overdue (boolean): Indicates that the version is overdue.
            project (string): Deprecated. Use `projectId`.
            projectId (integer): The ID of the project to which this version is attached. Required when creating a version. Not applicable when updating a version.
            releaseDate (string): The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating or updating a version.
            released (boolean): Indicates that the version is released. If the version is released a request to release again is ignored. Not applicable when creating a version. Optional when updating a version.
            self_arg_body (string): The URL of the version.
            startDate (string): The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating or updating a version.
            userReleaseDate (string): The date on which work on this version is expected to finish, expressed in the instance's *Day/Month/Year Format* date format.
            userStartDate (string): The date on which work on this version is expected to start, expressed in the instance's *Day/Month/Year Format* date format.
                Example:
                ```json
                {
                  "archived": false,
                  "description": "An excellent version",
                  "name": "New Version 1",
                  "projectId": 10000,
                  "releaseDate": "2010-07-06",
                  "released": true
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        request_body = {
            'approvers': approvers,
            'archived': archived,
            'description': description,
            'driver': driver,
            'expand': expand,
            'id': id,
            'issuesStatusForFixVersion': issuesStatusForFixVersion,
            'moveUnfixedIssuesTo': moveUnfixedIssuesTo,
            'name': name,
            'operations': operations,
            'overdue': overdue,
            'project': project,
            'projectId': projectId,
            'releaseDate': releaseDate,
            'released': released,
            'self': self_arg_body,
            'startDate': startDate,
            'userReleaseDate': userReleaseDate,
            'userStartDate': userStartDate,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_version(self, id, moveFixIssuesTo=None, moveAffectedIssuesTo=None) -> Any:
        """
        Deletes a Jira project version using the DELETE method, optionally allowing issues to be moved to alternative versions by specifying replacement versions for `fixVersion` and `affectedVersion` fields.

        Args:
            id (string): id
            moveFixIssuesTo (string): The ID of the version to update `fixVersion` to when the field contains the deleted version. The replacement version must be in the same project as the version being deleted and cannot be the version being deleted.
            moveAffectedIssuesTo (string): The ID of the version to update `affectedVersion` to when the field contains the deleted version. The replacement version must be in the same project as the version being deleted and cannot be the version being deleted.

        Returns:
            Any: Returned if the version is deleted.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/version/{id}"
        query_params = {k: v for k, v in [('moveFixIssuesTo', moveFixIssuesTo), ('moveAffectedIssuesTo', moveAffectedIssuesTo)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_version(self, id, expand=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific Jira version using the Jira REST API, with options to expand additional fields.

        Args:
            id (string): id
            expand (string): Use [expand](#expansion) to include additional information about version in the response. This parameter accepts a comma-separated list. Expand options include: * `operations` Returns the list of operations available for this version. * `issuesstatus` Returns the count of issues in this version for each of the status categories *to do*, *in progress*, *done*, and *unmapped*. The *unmapped* property represents the number of issues with a status other than *to do*, *in progress*, and *done*. * `driver` Returns the Atlassian account ID of the version driver. * `approvers` Returns a list containing the Atlassian account IDs of approvers for this version.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/version/{id}"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_version(self, id, approvers=None, archived=None, description=None, driver=None, expand=None, id_body=None, issuesStatusForFixVersion=None, moveUnfixedIssuesTo=None, name=None, operations=None, overdue=None, project=None, projectId=None, releaseDate=None, released=None, self_arg_body=None, startDate=None, userReleaseDate=None, userStartDate=None) -> dict[str, Any]:
        """
        Updates an existing version's details (e.g., name, description, release status) in Jira using the specified version ID.

        Args:
            id (string): id
            approvers (array): If the expand option `approvers` is used, returns a list containing the approvers for this version.
            archived (boolean): Indicates that the version is archived. Optional when creating or updating a version.
            description (string): The description of the version. Optional when creating or updating a version. The maximum size is 16,384 bytes.
            driver (string): If the expand option `driver` is used, returns the Atlassian account ID of the driver.
            expand (string): Use [expand](em>#expansion) to include additional information about version in the response. This parameter accepts a comma-separated list. Expand options include:

         *  `operations` Returns the list of operations available for this version.
         *  `issuesstatus` Returns the count of issues in this version for each of the status categories *to do*, *in progress*, *done*, and *unmapped*. The *unmapped* property contains a count of issues with a status other than *to do*, *in progress*, and *done*.
         *  `driver` Returns the Atlassian account ID of the version driver.
         *  `approvers` Returns a list containing approvers for this version.

        Optional for create and update.
            id_body (string): The ID of the version.
            issuesStatusForFixVersion (string): If the expand option `issuesstatus` is used, returns the count of issues in this version for each of the status categories *to do*, *in progress*, *done*, and *unmapped*. The *unmapped* property contains a count of issues with a status other than *to do*, *in progress*, and *done*.
            moveUnfixedIssuesTo (string): The URL of the self link to the version to which all unfixed issues are moved when a version is released. Not applicable when creating a version. Optional when updating a version.
            name (string): The unique name of the version. Required when creating a version. Optional when updating a version. The maximum length is 255 characters.
            operations (array): If the expand option `operations` is used, returns the list of operations available for this version.
            overdue (boolean): Indicates that the version is overdue.
            project (string): Deprecated. Use `projectId`.
            projectId (integer): The ID of the project to which this version is attached. Required when creating a version. Not applicable when updating a version.
            releaseDate (string): The release date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating or updating a version.
            released (boolean): Indicates that the version is released. If the version is released a request to release again is ignored. Not applicable when creating a version. Optional when updating a version.
            self_arg_body (string): The URL of the version.
            startDate (string): The start date of the version. Expressed in ISO 8601 format (yyyy-mm-dd). Optional when creating or updating a version.
            userReleaseDate (string): The date on which work on this version is expected to finish, expressed in the instance's *Day/Month/Year Format* date format.
            userStartDate (string): The date on which work on this version is expected to start, expressed in the instance's *Day/Month/Year Format* date format.
                Example:
                ```json
                {
                  "archived": false,
                  "description": "An excellent version",
                  "id": "10000",
                  "name": "New Version 1",
                  "overdue": true,
                  "projectId": 10000,
                  "releaseDate": "2010-07-06",
                  "released": true,
                  "self": "https://your-domain.atlassian.net/rest/api/~ver~/version/10000",
                  "userReleaseDate": "6/Jul/2010"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'approvers': approvers,
            'archived': archived,
            'description': description,
            'driver': driver,
            'expand': expand,
            'id': id_body,
            'issuesStatusForFixVersion': issuesStatusForFixVersion,
            'moveUnfixedIssuesTo': moveUnfixedIssuesTo,
            'name': name,
            'operations': operations,
            'overdue': overdue,
            'project': project,
            'projectId': projectId,
            'releaseDate': releaseDate,
            'released': released,
            'self': self_arg_body,
            'startDate': startDate,
            'userReleaseDate': userReleaseDate,
            'userStartDate': userStartDate,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def merge_versions(self, id, moveIssuesTo) -> Any:
        """
        Merges a Jira version with another specified version and optionally moves associated issues to the target version.

        Args:
            id (string): id
            moveIssuesTo (string): moveIssuesTo

        Returns:
            Any: Returned if the version is deleted.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if moveIssuesTo is None:
            raise ValueError("Missing required parameter 'moveIssuesTo'")
        url = f"{self.base_url}/rest/api/3/version/{id}/mergeto/{moveIssuesTo}"
        query_params = {}
        response = self._put(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def move_version(self, id, after=None, position=None) -> dict[str, Any]:
        """
        Moves a project version to a new position within the ordered version list by specifying its ID and returns a status message indicating the success or failure of the operation.

        Args:
            id (string): id
            after (string): The URL (self link) of the version after which to place the moved version. Cannot be used with `position`.
            position (string): An absolute position in which to place the moved version. Cannot be used with `after`.
                Example:
                ```json
                {
                  "after": "https://your-domain.atlassian.net/rest/api/~ver~/version/10000"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'after': after,
            'position': position,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version/{id}/move"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_version_related_issues(self, id) -> dict[str, Any]:
        """
        Retrieves counts of issues related to a specific Jira version, such as those with the version set as the fix version or affected version, using the "GET" method.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/version/{id}/relatedIssueCounts"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_related_work(self, id) -> list[Any]:
        """
        Retrieves related work items associated with a specific version ID in Jira.

        Args:
            id (string): id

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/version/{id}/relatedwork"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_related_work(self, id, category, issueId=None, relatedWorkId=None, title=None, url=None) -> dict[str, Any]:
        """
        Associates external related work (e.g., design files, communication links) with a Jira project version via a POST request.

        Args:
            id (string): id
            category (string): The category of the related work
            issueId (integer): The ID of the issue associated with the related work (if there is one). Cannot be updated via the Rest API.
            relatedWorkId (string): The id of the related work. For the native release note related work item, this will be null, and Rest API does not support updating it.
            title (string): The title of the related work
            url (string): The URL of the related work. Will be null for the native release note related work item, but is otherwise required.
                Example:
                ```json
                {
                  "category": "Design",
                  "title": "Design link",
                  "url": "https://www.atlassian.com"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'category': category,
            'issueId': issueId,
            'relatedWorkId': relatedWorkId,
            'title': title,
            'url': url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version/{id}/relatedwork"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_related_work(self, id, category, issueId=None, relatedWorkId=None, title=None, url=None) -> dict[str, Any]:
        """
        Updates a version's related work links in Jira using the PUT method at the "/rest/api/3/version/{id}/relatedwork" endpoint.

        Args:
            id (string): id
            category (string): The category of the related work
            issueId (integer): The ID of the issue associated with the related work (if there is one). Cannot be updated via the Rest API.
            relatedWorkId (string): The id of the related work. For the native release note related work item, this will be null, and Rest API does not support updating it.
            title (string): The title of the related work
            url (string): The URL of the related work. Will be null for the native release note related work item, but is otherwise required.
                Example:
                ```json
                {
                  "category": "Design",
                  "relatedWorkId": "fabcdef6-7878-1234-beaf-43211234abcd",
                  "title": "Design link",
                  "url": "https://www.atlassian.com"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful together with updated related work.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'category': category,
            'issueId': issueId,
            'relatedWorkId': relatedWorkId,
            'title': title,
            'url': url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version/{id}/relatedwork"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_and_replace_version(self, id, customFieldReplacementList=None, moveAffectedIssuesTo=None, moveFixIssuesTo=None) -> Any:
        """
        Deletes a project version by ID and swaps it with another version in fixVersion and affectedVersion fields using a POST request.

        Args:
            id (string): id
            customFieldReplacementList (array): An array of custom field IDs (`customFieldId`) and version IDs (`moveTo`) to update when the fields contain the deleted version.
            moveAffectedIssuesTo (integer): The ID of the version to update `affectedVersion` to when the field contains the deleted version.
            moveFixIssuesTo (integer): The ID of the version to update `fixVersion` to when the field contains the deleted version.

        Returns:
            Any: Returned if the version is deleted.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'customFieldReplacementList': customFieldReplacementList,
            'moveAffectedIssuesTo': moveAffectedIssuesTo,
            'moveFixIssuesTo': moveFixIssuesTo,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/version/{id}/removeAndSwap"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_version_unresolved_issues(self, id) -> dict[str, Any]:
        """
        Retrieves the count of unresolved issues associated with a specific version ID in Jira using the REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Project versions
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/version/{id}/unresolvedIssueCount"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_related_work(self, versionId, relatedWorkId) -> Any:
        """
        Deletes a related work item identified by the specified `relatedWorkId` within a version specified by `versionId`, returning a 204 status code upon successful deletion.

        Args:
            versionId (string): versionId
            relatedWorkId (string): relatedWorkId

        Returns:
            Any: Returned if the related work is deleted.

        Tags:
            Project versions
        """
        if versionId is None:
            raise ValueError("Missing required parameter 'versionId'")
        if relatedWorkId is None:
            raise ValueError("Missing required parameter 'relatedWorkId'")
        url = f"{self.base_url}/rest/api/3/version/{versionId}/relatedwork/{relatedWorkId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_webhook_by_id(self, webhookIds) -> Any:
        """
        Deletes a Jira webhook by ID using the "DELETE" method at the "/rest/api/3/webhook" endpoint, removing a previously registered webhook.

        Args:
            webhookIds (array): A list of webhook IDs.
                Example:
                ```json
                {
                  "webhookIds": [
                    10000,
                    10001,
                    10042
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Webhooks
        """
        request_body = {
            'webhookIds': webhookIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/webhook"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dynamic_webhooks_for_app(self, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of webhooks from Jira, allowing for pagination through parameters `startAt` and `maxResults`.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Webhooks
        """
        url = f"{self.base_url}/rest/api/3/webhook"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def register_dynamic_webhooks(self, url, webhooks) -> dict[str, Any]:
        """
        Registers a new webhook in Jira to trigger HTTP callbacks for specified events.

        Args:
            url (string): The URL that specifies where to send the webhooks. This URL must use the same base URL as the Connect app. Only a single URL per app is allowed to be registered.
            webhooks (array): A list of webhooks.
                Example:
                ```json
                {
                  "url": "https://your-app.example.com/webhook-received",
                  "webhooks": [
                    {
                      "events": [
                        "jira:issue_created",
                        "jira:issue_updated"
                      ],
                      "fieldIdsFilter": [
                        "summary",
                        "customfield_10029"
                      ],
                      "jqlFilter": "project = PROJ"
                    },
                    {
                      "events": [
                        "jira:issue_deleted"
                      ],
                      "jqlFilter": "project IN (PROJ, EXP) AND status = done"
                    },
                    {
                      "events": [
                        "issue_property_set"
                      ],
                      "issuePropertyKeysFilter": [
                        "my-issue-property-key"
                      ],
                      "jqlFilter": "project = PROJ"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Webhooks
        """
        request_body = {
            'url': url,
            'webhooks': webhooks,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/webhook"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_failed_webhooks(self, maxResults=None, after=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of failed webhook delivery attempts, supporting pagination via maxResults and after parameters.

        Args:
            maxResults (integer): The maximum number of webhooks to return per page. If obeying the maxResults directive would result in records with the same failure time being split across pages, the directive is ignored and all records with the same failure time included on the page.
            after (integer): The time after which any webhook failure must have occurred for the record to be returned, expressed as milliseconds since the UNIX epoch.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Webhooks
        """
        url = f"{self.base_url}/rest/api/3/webhook/failed"
        query_params = {k: v for k, v in [('maxResults', maxResults), ('after', after)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def refresh_webhooks(self, webhookIds) -> dict[str, Any]:
        """
        Refreshes Jira webhooks created via Connect Apps to extend their expiration dates using a PUT request.

        Args:
            webhookIds (array): A list of webhook IDs.
                Example:
                ```json
                {
                  "webhookIds": [
                    10000,
                    10001,
                    10042
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Webhooks
        """
        request_body = {
            'webhookIds': webhookIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/webhook/refresh"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_workflows(self, workflowName=None) -> list[Any]:
        """
        Retrieves a list of all workflows in Jira or a specific workflow by name, depending on whether the `workflowName` parameter is provided, using the Jira Cloud REST API.

        Args:
            workflowName (string): The name of the workflow to be returned. Only one workflow can be specified.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        url = f"{self.base_url}/rest/api/3/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_workflow(self, name, statuses, transitions, description=None) -> dict[str, Any]:
        """
        Creates a new workflow configuration in Jira Cloud using the REST API by sending a POST request to the "/rest/api/3/workflow" endpoint.

        Args:
            name (string): The name of the workflow. The name must be unique. The maximum length is 255 characters. Characters can be separated by a whitespace but the name cannot start or end with a whitespace.
            statuses (array): The statuses of the workflow. Any status that does not include a transition is added to the workflow without a transition.
            transitions (array): The transitions of the workflow. For the request to be valid, these transitions must:

         *  include one *initial* transition.
         *  not use the same name for a *global* and *directed* transition.
         *  have a unique name for each *global* transition.
         *  have a unique 'to' status for each *global* transition.
         *  have unique names for each transition from a status.
         *  not have a 'from' status on *initial* and *global* transitions.
         *  have a 'from' status on *directed* transitions.

        All the transition statuses must be included in `statuses`.
            description (string): The description of the workflow. The maximum length is 1000 characters.
                Example:
                ```json
                {
                  "description": "This is a workflow used for Stories and Tasks",
                  "name": "Workflow 1",
                  "statuses": [
                    {
                      "id": "1",
                      "properties": {
                        "jira.issue.editable": "false"
                      }
                    },
                    {
                      "id": "2"
                    },
                    {
                      "id": "3"
                    }
                  ],
                  "transitions": [
                    {
                      "from": [],
                      "name": "Created",
                      "to": "1",
                      "type": "initial"
                    },
                    {
                      "from": [
                        "1"
                      ],
                      "name": "In progress",
                      "properties": {
                        "custom-property": "custom-value"
                      },
                      "rules": {
                        "conditions": {
                          "conditions": [
                            {
                              "type": "RemoteOnlyCondition"
                            },
                            {
                              "configuration": {
                                "groups": [
                                  "developers",
                                  "qa-testers"
                                ]
                              },
                              "type": "UserInAnyGroupCondition"
                            }
                          ],
                          "operator": "AND"
                        },
                        "postFunctions": [
                          {
                            "type": "AssignToCurrentUserFunction"
                          }
                        ]
                      },
                      "screen": {
                        "id": "10001"
                      },
                      "to": "2",
                      "type": "directed"
                    },
                    {
                      "name": "Completed",
                      "rules": {
                        "postFunctions": [
                          {
                            "configuration": {
                              "fieldId": "assignee"
                            },
                            "type": "ClearFieldValuePostFunction"
                          }
                        ],
                        "validators": [
                          {
                            "configuration": {
                              "parentStatuses": [
                                {
                                  "id": "3"
                                }
                              ]
                            },
                            "type": "ParentStatusValidator"
                          },
                          {
                            "configuration": {
                              "permissionKey": "ADMINISTER_PROJECTS"
                            },
                            "type": "PermissionValidator"
                          }
                        ]
                      },
                      "to": "3",
                      "type": "global"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the workflow is created.

        Tags:
            Workflows
        """
        request_body = {
            'description': description,
            'name': name,
            'statuses': statuses,
            'transitions': transitions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflow"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_transition_rule_configurations(self, types, startAt=None, maxResults=None, keys=None, workflowNames=None, withTags=None, draft=None, expand=None) -> dict[str, Any]:
        """
        Retrieves and configures workflow rule configurations in Jira using the GET method, allowing filtering by various parameters such as workflow names and types.

        Args:
            types (array): The types of the transition rules to return.
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            keys (array): The transition rule class keys, as defined in the Connect or the Forge app descriptor, of the transition rules to return.
            workflowNames (array): The list of workflow names to filter by.
            withTags (array): The list of `tags` to filter by.
            draft (boolean): Whether draft or published workflows are returned. If not provided, both workflow types are returned.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts `transition`, which, for each rule, returns information about the transition the rule is assigned to.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow transition rules
        """
        url = f"{self.base_url}/rest/api/3/workflow/rule/config"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('types', types), ('keys', keys), ('workflowNames', workflowNames), ('withTags', withTags), ('draft', draft), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_transition_rule_configurations(self, workflows) -> dict[str, Any]:
        """
        Updates the configuration of a workflow transition rule using the Jira API, allowing customization of conditions under which a transition can occur.

        Args:
            workflows (array): The list of workflows with transition rules to update.
                Example:
                ```json
                {
                  "workflows": [
                    {
                      "conditions": [
                        {
                          "configuration": {
                            "disabled": false,
                            "tag": "Another tag",
                            "value": "{ \"size\": \"medium\" }"
                          },
                          "id": "d663bd873d93-59f5-11e9-8647-b4d6cbdc"
                        }
                      ],
                      "postFunctions": [
                        {
                          "configuration": {
                            "disabled": false,
                            "tag": "Sample tag",
                            "value": "{ \"color\": \"red\" }"
                          },
                          "id": "b4d6cbdc-59f5-11e9-8647-d663bd873d93"
                        }
                      ],
                      "validators": [
                        {
                          "configuration": {
                            "disabled": false,
                            "value": "{ \"shape\": \"square\" }"
                          },
                          "id": "11e9-59f5-b4d6cbdc-8647-d663bd873d93"
                        }
                      ],
                      "workflowId": {
                        "draft": false,
                        "name": "My Workflow name"
                      }
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow transition rules
        """
        request_body = {
            'workflows': workflows,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflow/rule/config"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_transition_rule_configurations(self, workflows) -> dict[str, Any]:
        """
        Deletes workflow transition rule configurations from Jira workflows using the "PUT" method.

        Args:
            workflows (array): The list of workflows with transition rules to delete.
                Example:
                ```json
                {
                  "workflows": [
                    {
                      "workflowId": {
                        "draft": false,
                        "name": "Internal support workflow"
                      },
                      "workflowRuleIds": [
                        "b4d6cbdc-59f5-11e9-8647-d663bd873d93",
                        "d663bd873d93-59f5-11e9-8647-b4d6cbdc",
                        "11e9-59f5-b4d6cbdc-8647-d663bd873d93"
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow transition rules
        """
        request_body = {
            'workflows': workflows,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflow/rule/config/delete"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflows_paginated(self, startAt=None, maxResults=None, workflowName=None, expand=None, queryString=None, orderBy=None, isActive=None) -> dict[str, Any]:
        """
        Retrieves a list of workflows in Jira using pagination, allowing filtering by parameters such as workflow name, query string, and active status, and optionally expanding details like statuses.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            workflowName (array): The name of a workflow to return. To include multiple workflows, provide an ampersand-separated list. For example, `workflowName=name1&workflowName=name2`.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `transitions` For each workflow, returns information about the transitions inside the workflow. * `transitions.rules` For each workflow transition, returns information about its rules. Transitions are included automatically if this expand is requested. * `transitions.properties` For each workflow transition, returns information about its properties. Transitions are included automatically if this expand is requested. * `statuses` For each workflow, returns information about the statuses inside the workflow. * `statuses.properties` For each workflow status, returns information about its properties. Statuses are included automatically if this expand is requested. * `default` For each workflow, returns information about whether this is the default workflow. * `schemes` For each workflow, returns information about the workflow schemes the workflow is assigned to. * `projects` For each workflow, returns information about the projects the workflow is assigned to, through workflow schemes. * `hasDraftWorkflow` For each workflow, returns information about whether the workflow has a draft version. * `operations` For each workflow, returns information about the actions that can be undertaken on the workflow.
            queryString (string): String used to perform a case-insensitive partial match with workflow name.
            orderBy (string): [Order](#ordering) the results by a field: * `name` Sorts by workflow name. * `created` Sorts by create time. * `updated` Sorts by update time.
            isActive (boolean): Filters active and inactive workflows.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        url = f"{self.base_url}/rest/api/3/workflow/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('workflowName', workflowName), ('expand', expand), ('queryString', queryString), ('orderBy', orderBy), ('isActive', isActive)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_transition_property(self, transitionId, key, workflowName, workflowMode=None) -> Any:
        """
        Deletes a specified property from a workflow transition in Jira using the "DELETE" method, allowing changes to the behavior of transitions by removing custom properties.

        Args:
            transitionId (string): transitionId
            key (string): The name of the transition property to delete, also known as the name of the property.
            workflowName (string): The name of the workflow that the transition belongs to.
            workflowMode (string): The workflow status. Set to `live` for inactive workflows or `draft` for draft workflows. Active workflows cannot be edited.

        Returns:
            Any: 200 response

        Tags:
            Workflow transition properties
        """
        if transitionId is None:
            raise ValueError("Missing required parameter 'transitionId'")
        url = f"{self.base_url}/rest/api/3/workflow/transitions/{transitionId}/properties"
        query_params = {k: v for k, v in [('key', key), ('workflowName', workflowName), ('workflowMode', workflowMode)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_transition_properties(self, transitionId, workflowName, includeReservedKeys=None, key=None, workflowMode=None) -> dict[str, Any]:
        """
        Retrieves workflow transition properties for a specified transition ID using query parameters to filter results by keys and workflow details.

        Args:
            transitionId (string): transitionId
            workflowName (string): The name of the workflow that the transition belongs to.
            includeReservedKeys (boolean): Some properties with keys that have the *jira.* prefix are reserved, which means they are not editable. To include these properties in the results, set this parameter to *true*.
            key (string): The key of the property being returned, also known as the name of the property. If this parameter is not specified, all properties on the transition are returned.
            workflowMode (string): The workflow status. Set to *live* for active and inactive workflows, or *draft* for draft workflows.

        Returns:
            dict[str, Any]: 200 response

        Tags:
            Workflow transition properties
        """
        if transitionId is None:
            raise ValueError("Missing required parameter 'transitionId'")
        url = f"{self.base_url}/rest/api/3/workflow/transitions/{transitionId}/properties"
        query_params = {k: v for k, v in [('includeReservedKeys', includeReservedKeys), ('key', key), ('workflowName', workflowName), ('workflowMode', workflowMode)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_workflow_transition_property(self, transitionId, key, workflowName, value, workflowMode=None, id=None, key_body=None) -> dict[str, Any]:
        """
        Creates a workflow transition property using the Jira Cloud API by sending a POST request to the specified endpoint, allowing users to store custom data against a workflow transition and modify its behavior.

        Args:
            transitionId (string): transitionId
            key (string): The key of the property being added, also known as the name of the property. Set this to the same value as the `key` defined in the request body.
            workflowName (string): The name of the workflow that the transition belongs to.
            value (string): The value of the transition property.
            workflowMode (string): The workflow status. Set to *live* for inactive workflows or *draft* for draft workflows. Active workflows cannot be edited.
            id (string): The ID of the transition property.
            key_body (string): The key of the transition property. Also known as the name of the transition property.
                Example:
                ```json
                {
                  "value": "createissue"
                }
                ```

        Returns:
            dict[str, Any]: 200 response

        Tags:
            Workflow transition properties
        """
        if transitionId is None:
            raise ValueError("Missing required parameter 'transitionId'")
        request_body = {
            'id': id,
            'key': key_body,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflow/transitions/{transitionId}/properties"
        query_params = {k: v for k, v in [('key', key), ('workflowName', workflowName), ('workflowMode', workflowMode)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_transition_property(self, transitionId, key, workflowName, value, workflowMode=None, id=None, key_body=None) -> dict[str, Any]:
        """
        Updates a workflow transition property (or creates it if nonexistent) in Jira Cloud using the transition ID, workflow name, and key.

        Args:
            transitionId (string): transitionId
            key (string): The key of the property being updated, also known as the name of the property. Set this to the same value as the `key` defined in the request body.
            workflowName (string): The name of the workflow that the transition belongs to.
            value (string): The value of the transition property.
            workflowMode (string): The workflow status. Set to `live` for inactive workflows or `draft` for draft workflows. Active workflows cannot be edited.
            id (string): The ID of the transition property.
            key_body (string): The key of the transition property. Also known as the name of the transition property.
                Example:
                ```json
                {
                  "value": "createissue"
                }
                ```

        Returns:
            dict[str, Any]: 200 response

        Tags:
            Workflow transition properties
        """
        if transitionId is None:
            raise ValueError("Missing required parameter 'transitionId'")
        request_body = {
            'id': id,
            'key': key_body,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflow/transitions/{transitionId}/properties"
        query_params = {k: v for k, v in [('key', key), ('workflowName', workflowName), ('workflowMode', workflowMode)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_inactive_workflow(self, entityId) -> Any:
        """
        Deletes a specified workflow by its entity ID using the Jira API and returns an empty response on success.

        Args:
            entityId (string): entityId

        Returns:
            Any: Returned if the workflow is deleted.

        Tags:
            Workflows
        """
        if entityId is None:
            raise ValueError("Missing required parameter 'entityId'")
        url = f"{self.base_url}/rest/api/3/workflow/{entityId}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_project_issue_type_usages(self, workflowId, projectId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves issue type usage for a specific workflow within a project using the Jira API, returning data on how issue types are used in that workflow.

        Args:
            workflowId (string): workflowId
            projectId (string): projectId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        if workflowId is None:
            raise ValueError("Missing required parameter 'workflowId'")
        if projectId is None:
            raise ValueError("Missing required parameter 'projectId'")
        url = f"{self.base_url}/rest/api/3/workflow/{workflowId}/project/{projectId}/issueTypeUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_usages_for_workflow(self, workflowId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves the list of projects that use a specified workflow in Jira, supporting pagination with optional parameters for next page token and maximum results.

        Args:
            workflowId (string): workflowId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        if workflowId is None:
            raise ValueError("Missing required parameter 'workflowId'")
        url = f"{self.base_url}/rest/api/3/workflow/{workflowId}/projectUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme_usages_for_workflow(self, workflowId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of workflow schemes associated with a specific workflow ID, allowing pagination through query parameters like nextPageToken and maxResults.

        Args:
            workflowId (string): workflowId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        if workflowId is None:
            raise ValueError("Missing required parameter 'workflowId'")
        url = f"{self.base_url}/rest/api/3/workflow/{workflowId}/workflowSchemes"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def read_workflows(self, expand=None, useApprovalConfiguration=None, projectAndIssueTypes=None, workflowIds=None, workflowNames=None) -> dict[str, Any]:
        """
        Creates new workflows in Jira Cloud using the REST API with the specified parameters and returns a response indicating the outcome.

        Args:
            expand (string): Deprecated. See the [deprecation notice]( for details. Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `workflows.usages` Returns the project and issue types that each workflow is associated with. * `statuses.usages` Returns the project and issue types that each status is associated with.
            useApprovalConfiguration (boolean): Return the new field `approvalConfiguration` instead of the deprecated status properties for approval configuration.
            projectAndIssueTypes (array): The list of projects and issue types to query.
            workflowIds (array): The list of workflow IDs to query.
            workflowNames (array): The list of workflow names to query.
                Example:
                ```json
                {
                  "projectAndIssueTypes": [],
                  "workflowIds": [],
                  "workflowNames": [
                    "Workflow 1",
                    "Workflow 2"
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        request_body = {
            'projectAndIssueTypes': projectAndIssueTypes,
            'workflowIds': workflowIds,
            'workflowNames': workflowNames,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflows"
        query_params = {k: v for k, v in [('expand', expand), ('useApprovalConfiguration', useApprovalConfiguration)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def workflow_capabilities(self, workflowId=None, projectId=None, issueTypeId=None) -> dict[str, Any]:
        """
        Retrieves workflow capabilities (e.g., transitions, statuses) based on specified workflow, project, or issue type identifiers.

        Args:
            workflowId (string): Specifies the unique identifier of the workflow to retrieve capabilities information for.
            projectId (string): The `projectId` parameter filters workflow capabilities by a specific project ID, allowing users to retrieve capabilities relevant to that project.
            issueTypeId (string): The "issueTypeId" parameter is used to specify the ID of the issue type to filter or retrieve capabilities for in a workflow.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        url = f"{self.base_url}/rest/api/3/workflows/capabilities"
        query_params = {k: v for k, v in [('workflowId', workflowId), ('projectId', projectId), ('issueTypeId', issueTypeId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_workflows(self, scope=None, statuses=None, workflows=None) -> dict[str, Any]:
        """
        Creates a Jira workflow via REST API and returns success/failure status codes.

        Args:
            scope (object): The scope of the workflow.
            statuses (array): The statuses to associate with the workflows.
            workflows (array): The details of the workflows to create.
                Example:
                ```json
                {
                  "scope": {
                    "type": "GLOBAL"
                  },
                  "statuses": [
                    {
                      "description": "",
                      "name": "To Do",
                      "statusCategory": "TODO",
                      "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                    },
                    {
                      "description": "",
                      "name": "In Progress",
                      "statusCategory": "IN_PROGRESS",
                      "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                    },
                    {
                      "description": "",
                      "name": "Done",
                      "statusCategory": "DONE",
                      "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                    }
                  ],
                  "workflows": [
                    {
                      "description": "",
                      "name": "Software workflow 1",
                      "startPointLayout": {
                        "x": -100.00030899047852,
                        "y": -153.00020599365234
                      },
                      "statuses": [
                        {
                          "layout": {
                            "x": 114.99993896484375,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                        },
                        {
                          "layout": {
                            "x": 317.0000915527344,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                        },
                        {
                          "layout": {
                            "x": 508.000244140625,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                        }
                      ],
                      "transitions": [
                        {
                          "actions": [],
                          "description": "",
                          "id": "1",
                          "links": [],
                          "name": "Create",
                          "properties": {},
                          "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                          "triggers": [],
                          "type": "INITIAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "",
                          "id": "11",
                          "links": [],
                          "name": "To Do",
                          "properties": {},
                          "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                          "triggers": [],
                          "type": "GLOBAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "",
                          "id": "21",
                          "links": [],
                          "name": "In Progress",
                          "properties": {},
                          "toStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                          "triggers": [],
                          "type": "GLOBAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "Move a work item from in progress to done",
                          "id": "31",
                          "links": [
                            {
                              "fromPort": 0,
                              "fromStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                              "toPort": 1
                            }
                          ],
                          "name": "Done",
                          "properties": {},
                          "toStatusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849",
                          "triggers": [],
                          "type": "DIRECTED",
                          "validators": []
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        request_body = {
            'scope': scope,
            'statuses': statuses,
            'workflows': workflows,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflows/create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def validate_create_workflows(self, payload, validationOptions=None) -> dict[str, Any]:
        """
        Validates the creation of a new workflow using the Jira API and returns a response based on the validation outcome.

        Args:
            payload (object): The create workflows payload.
            validationOptions (object): The level of validation to return from the API. If no values are provided, the default would return `WARNING` and `ERROR` level validation results.
                Example:
                ```json
                {
                  "payload": {
                    "scope": {
                      "type": "GLOBAL"
                    },
                    "statuses": [
                      {
                        "description": "",
                        "name": "To Do",
                        "statusCategory": "TODO",
                        "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                      },
                      {
                        "description": "",
                        "name": "In Progress",
                        "statusCategory": "IN_PROGRESS",
                        "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                      },
                      {
                        "description": "",
                        "name": "Done",
                        "statusCategory": "DONE",
                        "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                      }
                    ],
                    "workflows": [
                      {
                        "description": "",
                        "name": "Software workflow 1",
                        "startPointLayout": {
                          "x": -100.00030899047852,
                          "y": -153.00020599365234
                        },
                        "statuses": [
                          {
                            "layout": {
                              "x": 114.99993896484375,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                          },
                          {
                            "layout": {
                              "x": 317.0000915527344,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                          },
                          {
                            "layout": {
                              "x": 508.000244140625,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                          }
                        ],
                        "transitions": [
                          {
                            "actions": [],
                            "description": "",
                            "id": "1",
                            "links": [],
                            "name": "Create",
                            "properties": {},
                            "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                            "triggers": [],
                            "type": "INITIAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "",
                            "id": "11",
                            "links": [],
                            "name": "To Do",
                            "properties": {},
                            "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                            "triggers": [],
                            "type": "GLOBAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "",
                            "id": "21",
                            "links": [],
                            "name": "In Progress",
                            "properties": {},
                            "toStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                            "triggers": [],
                            "type": "GLOBAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "Move a work item from in progress to done",
                            "id": "31",
                            "links": [
                              {
                                "fromPort": 0,
                                "fromStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                                "toPort": 1
                              }
                            ],
                            "name": "Done",
                            "properties": {},
                            "toStatusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849",
                            "triggers": [],
                            "type": "DIRECTED",
                            "validators": []
                          }
                        ]
                      }
                    ]
                  },
                  "validationOptions": {
                    "levels": [
                      "ERROR",
                      "WARNING"
                    ]
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        request_body = {
            'payload': payload,
            'validationOptions': validationOptions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflows/create/validation"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_workflows(self, startAt=None, maxResults=None, expand=None, queryString=None, orderBy=None, scope=None, isActive=None) -> dict[str, Any]:
        """
        Searches for and retrieves workflows in Jira using specified query parameters, allowing for pagination, expansion of details, and filtering by active status.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `values.transitions` Returns the transitions that each workflow is associated with.
            queryString (string): String used to perform a case-insensitive partial match with workflow name.
            orderBy (string): [Order](#ordering) the results by a field: * `name` Sorts by workflow name. * `created` Sorts by create time. * `updated` Sorts by update time.
            scope (string): The scope of the workflow. Global for company-managed projects and Project for team-managed projects.
            isActive (boolean): Filters active and inactive workflows.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        url = f"{self.base_url}/rest/api/3/workflows/search"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults), ('expand', expand), ('queryString', queryString), ('orderBy', orderBy), ('scope', scope), ('isActive', isActive)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflows(self, expand=None, statuses=None, workflows=None) -> dict[str, Any]:
        """
        Updates a workflow using the specified parameters via the POST method at the "/rest/api/3/workflows/update" endpoint, potentially allowing expansion details based on the query parameter "expand".

        Args:
            expand (string): Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `workflows.usages` Returns the project and issue types that each workflow is associated with. * `statuses.usages` Returns the project and issue types that each status is associated with.
            statuses (array): The statuses to associate with the workflows.
            workflows (array): The details of the workflows to update.
                Example:
                ```json
                {
                  "statuses": [
                    {
                      "description": "",
                      "name": "To Do",
                      "statusCategory": "TODO",
                      "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                    },
                    {
                      "description": "",
                      "name": "In Progress",
                      "statusCategory": "IN_PROGRESS",
                      "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                    },
                    {
                      "description": "",
                      "name": "Done",
                      "statusCategory": "DONE",
                      "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                    }
                  ],
                  "workflows": [
                    {
                      "defaultStatusMappings": [
                        {
                          "newStatusReference": "10011",
                          "oldStatusReference": "10010"
                        }
                      ],
                      "description": "",
                      "id": "10001",
                      "startPointLayout": {
                        "x": -100.00030899047852,
                        "y": -153.00020599365234
                      },
                      "statusMappings": [
                        {
                          "issueTypeId": "10002",
                          "projectId": "10003",
                          "statusMigrations": [
                            {
                              "newStatusReference": "10011",
                              "oldStatusReference": "10010"
                            }
                          ]
                        }
                      ],
                      "statuses": [
                        {
                          "layout": {
                            "x": 114.99993896484375,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                        },
                        {
                          "layout": {
                            "x": 317.0000915527344,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                        },
                        {
                          "layout": {
                            "x": 508.000244140625,
                            "y": -16
                          },
                          "properties": {},
                          "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                        }
                      ],
                      "transitions": [
                        {
                          "actions": [],
                          "description": "",
                          "id": "1",
                          "links": [],
                          "name": "Create",
                          "properties": {},
                          "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                          "triggers": [],
                          "type": "INITIAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "",
                          "id": "11",
                          "links": [],
                          "name": "To Do",
                          "properties": {},
                          "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                          "triggers": [],
                          "type": "GLOBAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "",
                          "id": "21",
                          "links": [],
                          "name": "In Progress",
                          "properties": {},
                          "toStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                          "triggers": [],
                          "type": "GLOBAL",
                          "validators": []
                        },
                        {
                          "actions": [],
                          "description": "Move a work item from in progress to done",
                          "id": "31",
                          "links": [
                            {
                              "fromPort": 0,
                              "fromStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                              "toPort": 1
                            }
                          ],
                          "name": "Done",
                          "properties": {},
                          "toStatusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849",
                          "triggers": [],
                          "type": "DIRECTED",
                          "validators": []
                        }
                      ],
                      "version": {
                        "id": "6f6c988b-2590-4358-90c2-5f7960265592",
                        "versionNumber": 1
                      }
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        request_body = {
            'statuses': statuses,
            'workflows': workflows,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflows/update"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def validate_update_workflows(self, payload, validationOptions=None) -> dict[str, Any]:
        """
        Validates workflow updates for Jira Cloud using specified criteria and returns validation results.

        Args:
            payload (object): The update workflows payload.
            validationOptions (object): The level of validation to return from the API. If no values are provided, the default would return `WARNING` and `ERROR` level validation results.
                Example:
                ```json
                {
                  "payload": {
                    "statuses": [
                      {
                        "description": "",
                        "name": "To Do",
                        "statusCategory": "TODO",
                        "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                      },
                      {
                        "description": "",
                        "name": "In Progress",
                        "statusCategory": "IN_PROGRESS",
                        "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                      },
                      {
                        "description": "",
                        "name": "Done",
                        "statusCategory": "DONE",
                        "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                      }
                    ],
                    "workflows": [
                      {
                        "defaultStatusMappings": [
                          {
                            "newStatusReference": "10011",
                            "oldStatusReference": "10010"
                          }
                        ],
                        "description": "",
                        "id": "10001",
                        "startPointLayout": {
                          "x": -100.00030899047852,
                          "y": -153.00020599365234
                        },
                        "statusMappings": [
                          {
                            "issueTypeId": "10002",
                            "projectId": "10003",
                            "statusMigrations": [
                              {
                                "newStatusReference": "10011",
                                "oldStatusReference": "10010"
                              }
                            ]
                          }
                        ],
                        "statuses": [
                          {
                            "layout": {
                              "x": 114.99993896484375,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0"
                          },
                          {
                            "layout": {
                              "x": 317.0000915527344,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8"
                          },
                          {
                            "layout": {
                              "x": 508.000244140625,
                              "y": -16
                            },
                            "properties": {},
                            "statusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849"
                          }
                        ],
                        "transitions": [
                          {
                            "actions": [],
                            "description": "",
                            "id": "1",
                            "links": [],
                            "name": "Create",
                            "properties": {},
                            "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                            "triggers": [],
                            "type": "INITIAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "",
                            "id": "11",
                            "links": [],
                            "name": "To Do",
                            "properties": {},
                            "toStatusReference": "f0b24de5-25e7-4fab-ab94-63d81db6c0c0",
                            "triggers": [],
                            "type": "GLOBAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "",
                            "id": "21",
                            "links": [],
                            "name": "In Progress",
                            "properties": {},
                            "toStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                            "triggers": [],
                            "type": "GLOBAL",
                            "validators": []
                          },
                          {
                            "actions": [],
                            "description": "Move a work item from in progress to done",
                            "id": "31",
                            "links": [
                              {
                                "fromPort": 0,
                                "fromStatusReference": "c7a35bf0-c127-4aa6-869f-4033730c61d8",
                                "toPort": 1
                              }
                            ],
                            "name": "Done",
                            "properties": {},
                            "toStatusReference": "6b3fc04d-3316-46c5-a257-65751aeb8849",
                            "triggers": [],
                            "type": "DIRECTED",
                            "validators": []
                          }
                        ],
                        "version": {
                          "id": "6f6c988b-2590-4358-90c2-5f7960265592",
                          "versionNumber": 1
                        }
                      }
                    ]
                  },
                  "validationOptions": {
                    "levels": [
                      "ERROR",
                      "WARNING"
                    ]
                  }
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflows
        """
        request_body = {
            'payload': payload,
            'validationOptions': validationOptions,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflows/update/validation"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_all_workflow_schemes(self, startAt=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves a list of workflow schemes in Jira Cloud, allowing for pagination by specifying a start index and maximum number of results, using the Atlassian Jira Cloud REST API.

        Args:
            startAt (integer): The index of the first item to return in a page of results (page offset).
            maxResults (integer): The maximum number of items to return per page.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        url = f"{self.base_url}/rest/api/3/workflowscheme"
        query_params = {k: v for k, v in [('startAt', startAt), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_workflow_scheme(self, defaultWorkflow=None, description=None, draft=None, id=None, issueTypeMappings=None, issueTypes=None, lastModified=None, lastModifiedUser=None, name=None, originalDefaultWorkflow=None, originalIssueTypeMappings=None, self_arg_body=None, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Creates a new workflow scheme in Jira Cloud with specified configurations like default workflow and issue type mappings.

        Args:
            defaultWorkflow (string): The name of the default workflow for the workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira. If `defaultWorkflow` is not specified when creating a workflow scheme, it is set to *Jira Workflow (jira)*.
            description (string): The description of the workflow scheme.
            draft (boolean): Whether the workflow scheme is a draft or not.
            id (integer): The ID of the workflow scheme.
            issueTypeMappings (object): The issue type to workflow mappings, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            issueTypes (object): The issue types available in Jira.
            lastModified (string): The date-time that the draft workflow scheme was last modified. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            lastModifiedUser (string): The user that last modified the draft workflow scheme. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            name (string): The name of the workflow scheme. The name must be unique. The maximum length is 255 characters. Required when creating a workflow scheme.
            originalDefaultWorkflow (string): For draft workflow schemes, this property is the name of the default workflow for the original workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira.
            originalIssueTypeMappings (object): For draft workflow schemes, this property is the issue type to workflow mappings for the original workflow scheme, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            self_arg_body (string): self
            updateDraftIfNeeded (boolean): Whether to create or update a draft workflow scheme when updating an active workflow scheme. An active workflow scheme is a workflow scheme that is used by at least one project. The following examples show how this property works:

         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `true`: If a draft workflow scheme exists, it is updated. Otherwise, a draft workflow scheme is created.
         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `false`: An error is returned, as active workflow schemes cannot be updated.
         *  Update an inactive workflow scheme with `updateDraftIfNeeded` set to `true`: The workflow scheme is updated, as inactive workflow schemes do not require drafts to update.

        Defaults to `false`.
                Example:
                ```json
                {
                  "defaultWorkflow": "jira",
                  "description": "The description of the example workflow scheme.",
                  "issueTypeMappings": {
                    "10000": "scrum workflow",
                    "10001": "builds workflow"
                  },
                  "name": "Example workflow scheme"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        request_body = {
            'defaultWorkflow': defaultWorkflow,
            'description': description,
            'draft': draft,
            'id': id,
            'issueTypeMappings': issueTypeMappings,
            'issueTypes': issueTypes,
            'lastModified': lastModified,
            'lastModifiedUser': lastModifiedUser,
            'name': name,
            'originalDefaultWorkflow': originalDefaultWorkflow,
            'originalIssueTypeMappings': originalIssueTypeMappings,
            'self': self_arg_body,
            'updateDraftIfNeeded': updateDraftIfNeeded,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme_project_associations(self, projectId) -> dict[str, Any]:
        """
        Retrieves the workflow scheme project associations for a specified project using the provided `projectId` in the query parameters.

        Args:
            projectId (array): The ID of a project to return the workflow schemes for. To include multiple projects, provide an ampersand-Jim: oneseparated list. For example, `projectId=10000&projectId=10001`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme project associations
        """
        url = f"{self.base_url}/rest/api/3/workflowscheme/project"
        query_params = {k: v for k, v in [('projectId', projectId)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def assign_scheme_to_project(self, projectId, workflowSchemeId=None) -> Any:
        """
        Associates a workflow scheme with a Jira project using the specified scheme ID.

        Args:
            projectId (string): The ID of the project.
            workflowSchemeId (string): The ID of the workflow scheme. If the workflow scheme ID is `null`, the operation assigns the default workflow scheme.
                Example:
                ```json
                {
                  "projectId": "10001",
                  "workflowSchemeId": "10032"
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Workflow scheme project associations
        """
        request_body = {
            'projectId': projectId,
            'workflowSchemeId': workflowSchemeId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/project"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def read_workflow_schemes(self, expand=None, projectIds=None, workflowSchemeIds=None) -> list[Any]:
        """
        Retrieves a list of workflow schemes using provided workflow scheme IDs or project IDs via the Jira Cloud REST API.

        Args:
            expand (string): Deprecated. See the [deprecation notice]( for details. Use [expand](#expansion) to include additional information in the response. This parameter accepts a comma-separated list. Expand options include: * `workflows.usages` Returns the project and issue types that each workflow in the workflow scheme is associated with.
            projectIds (array): The list of project IDs to query.
            workflowSchemeIds (array): The list of workflow scheme IDs to query.
                Example:
                ```json
                {
                  "projectIds": [
                    "10047",
                    "10048"
                  ],
                  "workflowSchemeIds": [
                    "3e59db0f-ed6c-47ce-8d50-80c0c4572677"
                  ]
                }
                ```

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        request_body = {
            'projectIds': projectIds,
            'workflowSchemeIds': workflowSchemeIds,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/read"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_schemes(self, description, id, name, version, defaultWorkflowId=None, statusMappingsByIssueTypeOverride=None, statusMappingsByWorkflows=None, workflowsForIssueTypes=None) -> Any:
        """
        Updates Jira workflow schemes (company-managed or team-managed projects) with immediate effect, optionally creating a draft if active, and migrates issues asynchronously when changing status mappings.

        Args:
            description (string): The new description for this workflow scheme.
            id (string): The ID of this workflow scheme.
            name (string): The new name for this workflow scheme.
            version (object): The current version details of this workflow scheme.
            defaultWorkflowId (string): The ID of the workflow for issue types without having a mapping defined in this workflow scheme. Only used in global-scoped workflow schemes. If the `defaultWorkflowId` isn't specified, this is set to *Jira Workflow (jira)*.
            statusMappingsByIssueTypeOverride (array): Overrides, for the selected issue types, any status mappings provided in `statusMappingsByWorkflows`. Status mappings are required when the new workflow for an issue type doesn't contain all statuses that the old workflow has. Status mappings can be provided by a combination of `statusMappingsByWorkflows` and `statusMappingsByIssueTypeOverride`.
            statusMappingsByWorkflows (array): The status mappings by workflows. Status mappings are required when the new workflow for an issue type doesn't contain all statuses that the old workflow has. Status mappings can be provided by a combination of `statusMappingsByWorkflows` and `statusMappingsByIssueTypeOverride`.
            workflowsForIssueTypes (array): Mappings from workflows to issue types.
                Example:
                ```json
                {
                  "defaultWorkflowId": "3e59db0f-ed6c-47ce-8d50-80c0c4572677",
                  "description": "description",
                  "id": "10000",
                  "name": "name",
                  "statusMappingsByIssueTypeOverride": [
                    {
                      "issueTypeId": "10001",
                      "statusMappings": [
                        {
                          "newStatusId": "2",
                          "oldStatusId": "1"
                        },
                        {
                          "newStatusId": "4",
                          "oldStatusId": "3"
                        }
                      ]
                    },
                    {
                      "issueTypeId": "10002",
                      "statusMappings": [
                        {
                          "newStatusId": "4",
                          "oldStatusId": "1"
                        },
                        {
                          "newStatusId": "2",
                          "oldStatusId": "3"
                        }
                      ]
                    }
                  ],
                  "statusMappingsByWorkflows": [
                    {
                      "newWorkflowId": "3e59db0f-ed6c-47ce-8d50-80c0c4572677",
                      "oldWorkflowId": "3e59db0f-ed6c-47ce-8d50-80c0c4572677",
                      "statusMappings": [
                        {
                          "newStatusId": "2",
                          "oldStatusId": "1"
                        },
                        {
                          "newStatusId": "4",
                          "oldStatusId": "3"
                        }
                      ]
                    }
                  ],
                  "version": {
                    "id": "527213fc-bc72-400f-aae0-df8d88db2c8a",
                    "versionNumber": 1
                  },
                  "workflowsForIssueTypes": [
                    {
                      "issueTypeIds": [
                        "10000",
                        "10003"
                      ],
                      "workflowId": "3e59db0f-ed6c-47ce-8d50-80c0c4572677"
                    },
                    {
                      "issueTypeIds": [
                        "10001`",
                        "10002"
                      ],
                      "workflowId": "3f83dg2a-ns2n-56ab-9812-42h5j1461629"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful and there is no asynchronous task.

        Tags:
            Workflow schemes
        """
        request_body = {
            'defaultWorkflowId': defaultWorkflowId,
            'description': description,
            'id': id,
            'name': name,
            'statusMappingsByIssueTypeOverride': statusMappingsByIssueTypeOverride,
            'statusMappingsByWorkflows': statusMappingsByWorkflows,
            'version': version,
            'workflowsForIssueTypes': workflowsForIssueTypes,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_scheme_mappings(self, id, workflowsForIssueTypes, defaultWorkflowId=None) -> dict[str, Any]:
        """
        Updates workflow scheme status mappings asynchronously for issue types and triggers issue migrations if needed.

        Args:
            id (string): The ID of the workflow scheme.
            workflowsForIssueTypes (array): The new workflow to issue type mappings for this workflow scheme.
            defaultWorkflowId (string): The ID of the new default workflow for this workflow scheme. Only used in global-scoped workflow schemes. If it isn't specified, is set to *Jira Workflow (jira)*.
                Example:
                ```json
                {
                  "defaultWorkflowId": "10010",
                  "id": "10001",
                  "workflowsForIssueTypes": [
                    {
                      "issueTypeIds": [
                        "10010",
                        "10011"
                      ],
                      "workflowId": "10001"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        request_body = {
            'defaultWorkflowId': defaultWorkflowId,
            'id': id,
            'workflowsForIssueTypes': workflowsForIssueTypes,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/update/mappings"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_scheme(self, id) -> Any:
        """
        Deletes a specified workflow scheme in Jira, which cannot be active (used by projects), and returns a success status upon completion.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme(self, id, returnDraftIfExists=None) -> dict[str, Any]:
        """
        Retrieves a workflow scheme by ID from Jira, optionally returning the draft version if it exists.

        Args:
            id (string): id
            returnDraftIfExists (boolean): Returns the workflow scheme's draft rather than scheme itself, if set to true. If the workflow scheme does not have a draft, then the workflow scheme is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}"
        query_params = {k: v for k, v in [('returnDraftIfExists', returnDraftIfExists)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_scheme(self, id, defaultWorkflow=None, description=None, draft=None, id_body=None, issueTypeMappings=None, issueTypes=None, lastModified=None, lastModifiedUser=None, name=None, originalDefaultWorkflow=None, originalIssueTypeMappings=None, self_arg_body=None, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Updates a workflow scheme by setting a new default workflow, allowing for the creation or update of a draft scheme if the original is active.

        Args:
            id (string): id
            defaultWorkflow (string): The name of the default workflow for the workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira. If `defaultWorkflow` is not specified when creating a workflow scheme, it is set to *Jira Workflow (jira)*.
            description (string): The description of the workflow scheme.
            draft (boolean): Whether the workflow scheme is a draft or not.
            id_body (integer): The ID of the workflow scheme.
            issueTypeMappings (object): The issue type to workflow mappings, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            issueTypes (object): The issue types available in Jira.
            lastModified (string): The date-time that the draft workflow scheme was last modified. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            lastModifiedUser (string): The user that last modified the draft workflow scheme. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            name (string): The name of the workflow scheme. The name must be unique. The maximum length is 255 characters. Required when creating a workflow scheme.
            originalDefaultWorkflow (string): For draft workflow schemes, this property is the name of the default workflow for the original workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira.
            originalIssueTypeMappings (object): For draft workflow schemes, this property is the issue type to workflow mappings for the original workflow scheme, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            self_arg_body (string): self
            updateDraftIfNeeded (boolean): Whether to create or update a draft workflow scheme when updating an active workflow scheme. An active workflow scheme is a workflow scheme that is used by at least one project. The following examples show how this property works:

         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `true`: If a draft workflow scheme exists, it is updated. Otherwise, a draft workflow scheme is created.
         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `false`: An error is returned, as active workflow schemes cannot be updated.
         *  Update an inactive workflow scheme with `updateDraftIfNeeded` set to `true`: The workflow scheme is updated, as inactive workflow schemes do not require drafts to update.

        Defaults to `false`.
                Example:
                ```json
                {
                  "defaultWorkflow": "jira",
                  "description": "The description of the example workflow scheme.",
                  "issueTypeMappings": {
                    "10000": "scrum workflow"
                  },
                  "name": "Example workflow scheme",
                  "updateDraftIfNeeded": false
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'defaultWorkflow': defaultWorkflow,
            'description': description,
            'draft': draft,
            'id': id_body,
            'issueTypeMappings': issueTypeMappings,
            'issueTypes': issueTypes,
            'lastModified': lastModified,
            'lastModifiedUser': lastModifiedUser,
            'name': name,
            'originalDefaultWorkflow': originalDefaultWorkflow,
            'originalIssueTypeMappings': originalIssueTypeMappings,
            'self': self_arg_body,
            'updateDraftIfNeeded': updateDraftIfNeeded,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_workflow_scheme_draft_from_parent(self, id) -> dict[str, Any]:
        """
        Creates a draft copy of a specified workflow scheme in Jira using the REST API.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/createdraft"
        query_params = {}
        response = self._post(url, data={}, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_default_workflow(self, id, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Deletes the default workflow from a Jira workflow scheme, resetting it to the system default (jira workflow) and optionally creates/updates a draft workflow scheme if specified.

        Args:
            id (string): id
            updateDraftIfNeeded (boolean): Set to true to create or update the draft of a workflow scheme and delete the mapping from the draft, when the workflow scheme cannot be edited. Defaults to `false`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/default"
        query_params = {k: v for k, v in [('updateDraftIfNeeded', updateDraftIfNeeded)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_default_workflow(self, id, returnDraftIfExists=None) -> dict[str, Any]:
        """
        Retrieves the default workflow assigned to unassociated issue types in a specified Jira workflow scheme.

        Args:
            id (string): id
            returnDraftIfExists (boolean): Set to `true` to return the default workflow for the workflow scheme's draft rather than scheme itself. If the workflow scheme does not have a draft, then the default workflow for the workflow scheme is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/default"
        query_params = {k: v for k, v in [('returnDraftIfExists', returnDraftIfExists)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_default_workflow(self, id, workflow, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Updates the default workflow in a Jira Cloud workflow scheme, which applies to all unassigned issue types.

        Args:
            id (string): id
            workflow (string): The name of the workflow to set as the default workflow.
            updateDraftIfNeeded (boolean): Whether a draft workflow scheme is created or updated when updating an active workflow scheme. The draft is updated with the new default workflow. Defaults to `false`.
                Example:
                ```json
                {
                  "updateDraftIfNeeded": false,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_scheme_draft(self, id) -> Any:
        """
        Deletes a draft workflow scheme for a specified workflow scheme ID using the Jira Cloud platform REST API.

        Args:
            id (string): id

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme_draft(self, id) -> dict[str, Any]:
        """
        Retrieves the draft workflow scheme for a specified workflow scheme ID in Jira Cloud, allowing modifications to the active workflow scheme through its draft copy.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_scheme_draft(self, id, defaultWorkflow=None, description=None, draft=None, id_body=None, issueTypeMappings=None, issueTypes=None, lastModified=None, lastModifiedUser=None, name=None, originalDefaultWorkflow=None, originalIssueTypeMappings=None, self_arg_body=None, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Updates a draft workflow scheme, creating one if it does not exist for the specified active workflow scheme, using the provided details such as default workflow and issue type mappings.

        Args:
            id (string): id
            defaultWorkflow (string): The name of the default workflow for the workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira. If `defaultWorkflow` is not specified when creating a workflow scheme, it is set to *Jira Workflow (jira)*.
            description (string): The description of the workflow scheme.
            draft (boolean): Whether the workflow scheme is a draft or not.
            id_body (integer): The ID of the workflow scheme.
            issueTypeMappings (object): The issue type to workflow mappings, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            issueTypes (object): The issue types available in Jira.
            lastModified (string): The date-time that the draft workflow scheme was last modified. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            lastModifiedUser (string): The user that last modified the draft workflow scheme. A modification is a change to the issue type-project mappings only. This property does not apply to non-draft workflows.
            name (string): The name of the workflow scheme. The name must be unique. The maximum length is 255 characters. Required when creating a workflow scheme.
            originalDefaultWorkflow (string): For draft workflow schemes, this property is the name of the default workflow for the original workflow scheme. The default workflow has *All Unassigned Issue Types* assigned to it in Jira.
            originalIssueTypeMappings (object): For draft workflow schemes, this property is the issue type to workflow mappings for the original workflow scheme, where each mapping is an issue type ID and workflow name pair. Note that an issue type can only be mapped to one workflow in a workflow scheme.
            self_arg_body (string): self
            updateDraftIfNeeded (boolean): Whether to create or update a draft workflow scheme when updating an active workflow scheme. An active workflow scheme is a workflow scheme that is used by at least one project. The following examples show how this property works:

         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `true`: If a draft workflow scheme exists, it is updated. Otherwise, a draft workflow scheme is created.
         *  Update an active workflow scheme with `updateDraftIfNeeded` set to `false`: An error is returned, as active workflow schemes cannot be updated.
         *  Update an inactive workflow scheme with `updateDraftIfNeeded` set to `true`: The workflow scheme is updated, as inactive workflow schemes do not require drafts to update.

        Defaults to `false`.
                Example:
                ```json
                {
                  "defaultWorkflow": "jira",
                  "description": "The description of the example workflow scheme.",
                  "issueTypeMappings": {
                    "10000": "scrum workflow"
                  },
                  "name": "Example workflow scheme",
                  "updateDraftIfNeeded": false
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'defaultWorkflow': defaultWorkflow,
            'description': description,
            'draft': draft,
            'id': id_body,
            'issueTypeMappings': issueTypeMappings,
            'issueTypes': issueTypes,
            'lastModified': lastModified,
            'lastModifiedUser': lastModifiedUser,
            'name': name,
            'originalDefaultWorkflow': originalDefaultWorkflow,
            'originalIssueTypeMappings': originalIssueTypeMappings,
            'self': self_arg_body,
            'updateDraftIfNeeded': updateDraftIfNeeded,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_draft_default_workflow(self, id) -> dict[str, Any]:
        """
        Deletes the default workflow for a draft workflow scheme, resetting it to Jira's system workflow, using the specified scheme ID.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/default"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_draft_default_workflow(self, id) -> dict[str, Any]:
        """
        Retrieves the default workflow configuration for a draft workflow scheme in Jira.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/default"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_draft_default_workflow(self, id, workflow, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Sets the default workflow for a draft workflow scheme in Jira, enabling configuration changes before publication.

        Args:
            id (string): id
            workflow (string): The name of the workflow to set as the default workflow.
            updateDraftIfNeeded (boolean): Whether a draft workflow scheme is created or updated when updating an active workflow scheme. The draft is updated with the new default workflow. Defaults to `false`.
                Example:
                ```json
                {
                  "updateDraftIfNeeded": false,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/default"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_scheme_draft_issue_type(self, id, issueType) -> dict[str, Any]:
        """
        Deletes a specific issue type mapping from a draft workflow scheme in Jira using the provided workflow scheme ID and issue type.

        Args:
            id (string): id
            issueType (string): issueType

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme_draft_issue_type(self, id, issueType) -> dict[str, Any]:
        """
        Retrieves the workflow configuration for a specific issue type in a draft workflow scheme.

        Args:
            id (string): id
            issueType (string): issueType

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_workflow_scheme_draft_issue_type(self, id, issueType, issueType_body=None, updateDraftIfNeeded=None, workflow=None) -> dict[str, Any]:
        """
        Updates an issue type in a workflow scheme draft using the Jira Cloud API, allowing modifications to workflow mappings without affecting the active scheme until published.

        Args:
            id (string): id
            issueType (string): issueType
            issueType_body (string): The ID of the issue type. Not required if updating the issue type-workflow mapping.
            updateDraftIfNeeded (boolean): Set to true to create or update the draft of a workflow scheme and update the mapping in the draft, when the workflow scheme cannot be edited. Defaults to `false`. Only applicable when updating the workflow-issue types mapping.
            workflow (string): The name of the workflow.
                Example:
                ```json
                {
                  "issueType": "10000",
                  "updateDraftIfNeeded": false,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        request_body = {
            'issueType': issueType_body,
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def publish_draft_workflow_scheme(self, id, validateOnly=None, statusMappings=None) -> Any:
        """
        Publishes a draft workflow scheme in Jira, replacing the active scheme upon successful execution.

        Args:
            id (string): id
            validateOnly (boolean): Whether the request only performs a validation.
            statusMappings (array): Mappings of statuses to new statuses for issue types.
                Example:
                ```json
                {
                  "statusMappings": [
                    {
                      "issueTypeId": "10001",
                      "newStatusId": "1",
                      "statusId": "3"
                    },
                    {
                      "issueTypeId": "10001",
                      "newStatusId": "2",
                      "statusId": "2"
                    },
                    {
                      "issueTypeId": "10002",
                      "newStatusId": "10003",
                      "statusId": "10005"
                    },
                    {
                      "issueTypeId": "10003",
                      "newStatusId": "1",
                      "statusId": "4"
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is only for validation and is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'statusMappings': statusMappings,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/publish"
        query_params = {k: v for k, v in [('validateOnly', validateOnly)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_draft_workflow_mapping(self, id, workflowName) -> Any:
        """
        Deletes a specific workflow associated with a draft workflow scheme in Jira.

        Args:
            id (string): id
            workflowName (string): The name of the workflow.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_draft_workflow(self, id, workflowName=None) -> dict[str, Any]:
        """
        Retrieves the workflow configuration for a draft workflow scheme in Jira by ID and optional workflow name.

        Args:
            id (string): id
            workflowName (string): The name of a workflow in the scheme. Limits the results to the workflow-issue type mapping for the specified workflow.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_draft_workflow_mapping(self, id, workflowName, defaultMapping=None, issueTypes=None, updateDraftIfNeeded=None, workflow=None) -> dict[str, Any]:
        """
        Updates the draft workflow scheme's associated workflow for a specified workflow name.

        Args:
            id (string): id
            workflowName (string): The name of the workflow.
            defaultMapping (boolean): Whether the workflow is the default workflow for the workflow scheme.
            issueTypes (array): The list of issue type IDs.
            updateDraftIfNeeded (boolean): Whether a draft workflow scheme is created or updated when updating an active workflow scheme. The draft is updated with the new workflow-issue types mapping. Defaults to `false`.
            workflow (string): The name of the workflow. Optional if updating the workflow-issue types mapping.
                Example:
                ```json
                {
                  "issueTypes": [
                    "10000"
                  ],
                  "updateDraftIfNeeded": true,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow scheme drafts
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'defaultMapping': defaultMapping,
            'issueTypes': issueTypes,
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/draft/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_scheme_issue_type(self, id, issueType, updateDraftIfNeeded=None) -> dict[str, Any]:
        """
        Removes the workflow-issue type mapping for a specified issue type in a workflow scheme, creating/updating a draft if the scheme is active and updateDraftIfNeeded is enabled.

        Args:
            id (string): id
            issueType (string): issueType
            updateDraftIfNeeded (boolean): Set to true to create or update the draft of a workflow scheme and update the mapping in the draft, when the workflow scheme cannot be edited. Defaults to `false`.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/issuetype/{issueType}"
        query_params = {k: v for k, v in [('updateDraftIfNeeded', updateDraftIfNeeded)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow_scheme_issue_type(self, id, issueType, returnDraftIfExists=None) -> dict[str, Any]:
        """
        Retrieves the workflow associated with a specific issue type in a workflow scheme, optionally returning the draft configuration if it exists.

        Args:
            id (string): id
            issueType (string): issueType
            returnDraftIfExists (boolean): Returns the mapping from the workflow scheme's draft rather than the workflow scheme, if set to true. If no draft exists, the mapping from the workflow scheme is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/issuetype/{issueType}"
        query_params = {k: v for k, v in [('returnDraftIfExists', returnDraftIfExists)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def set_workflow_scheme_issue_type(self, id, issueType, issueType_body=None, updateDraftIfNeeded=None, workflow=None) -> dict[str, Any]:
        """
        Sets the workflow for a specific issue type in a workflow scheme using the provided ID and issue type parameters.

        Args:
            id (string): id
            issueType (string): issueType
            issueType_body (string): The ID of the issue type. Not required if updating the issue type-workflow mapping.
            updateDraftIfNeeded (boolean): Set to true to create or update the draft of a workflow scheme and update the mapping in the draft, when the workflow scheme cannot be edited. Defaults to `false`. Only applicable when updating the workflow-issue types mapping.
            workflow (string): The name of the workflow.
                Example:
                ```json
                {
                  "issueType": "10000",
                  "updateDraftIfNeeded": false,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if issueType is None:
            raise ValueError("Missing required parameter 'issueType'")
        request_body = {
            'issueType': issueType_body,
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/issuetype/{issueType}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_workflow_mapping(self, id, workflowName, updateDraftIfNeeded=None) -> Any:
        """
        Deletes a specific workflow from a workflow scheme identified by the provided ID, optionally updating a draft if the scheme is active, using the Jira Cloud REST API.

        Args:
            id (string): id
            workflowName (string): The name of the workflow.
            updateDraftIfNeeded (boolean): Set to true to create or update the draft of a workflow scheme and delete the mapping from the draft, when the workflow scheme cannot be edited. Defaults to `false`.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName), ('updateDraftIfNeeded', updateDraftIfNeeded)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_workflow(self, id, workflowName=None, returnDraftIfExists=None) -> dict[str, Any]:
        """
        Retrieves the workflow configuration for a specified workflow scheme in Jira, optionally returning draft configurations if they exist.

        Args:
            id (string): id
            workflowName (string): The name of a workflow in the scheme. Limits the results to the workflow-issue type mapping for the specified workflow.
            returnDraftIfExists (boolean): Returns the mapping from the workflow scheme's draft rather than the workflow scheme, if set to true. If no draft exists, the mapping from the workflow scheme is returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName), ('returnDraftIfExists', returnDraftIfExists)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def update_workflow_mapping(self, id, workflowName, defaultMapping=None, issueTypes=None, updateDraftIfNeeded=None, workflow=None) -> dict[str, Any]:
        """
        Updates a specified workflow scheme by assigning a new workflow, identified by the `workflowName` query parameter, to it using the Jira Cloud platform's REST API.

        Args:
            id (string): id
            workflowName (string): The name of the workflow.
            defaultMapping (boolean): Whether the workflow is the default workflow for the workflow scheme.
            issueTypes (array): The list of issue type IDs.
            updateDraftIfNeeded (boolean): Whether a draft workflow scheme is created or updated when updating an active workflow scheme. The draft is updated with the new workflow-issue types mapping. Defaults to `false`.
            workflow (string): The name of the workflow. Optional if updating the workflow-issue types mapping.
                Example:
                ```json
                {
                  "issueTypes": [
                    "10000"
                  ],
                  "updateDraftIfNeeded": true,
                  "workflow": "jira"
                }
                ```

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'defaultMapping': defaultMapping,
            'issueTypes': issueTypes,
            'updateDraftIfNeeded': updateDraftIfNeeded,
            'workflow': workflow,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/workflowscheme/{id}/workflow"
        query_params = {k: v for k, v in [('workflowName', workflowName)] if v is not None}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_project_usages_for_workflow_scheme(self, workflowSchemeId, nextPageToken=None, maxResults=None) -> dict[str, Any]:
        """
        Retrieves the list of projects associated with a specific workflow scheme using pagination.

        Args:
            workflowSchemeId (string): workflowSchemeId
            nextPageToken (string): The cursor for pagination
            maxResults (integer): The maximum number of results to return. Must be an integer between 1 and 200.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Workflow schemes
        """
        if workflowSchemeId is None:
            raise ValueError("Missing required parameter 'workflowSchemeId'")
        url = f"{self.base_url}/rest/api/3/workflowscheme/{workflowSchemeId}/projectUsages"
        query_params = {k: v for k, v in [('nextPageToken', nextPageToken), ('maxResults', maxResults)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_ids_of_worklogs_deleted_since(self, since=None) -> dict[str, Any]:
        """
        Retrieves a list of IDs and delete timestamps for worklogs that have been deleted since a specified time using the Jira API.

        Args:
            since (integer): The date and time, as a UNIX timestamp in milliseconds, after which deleted worklogs are returned.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        url = f"{self.base_url}/rest/api/3/worklog/deleted"
        query_params = {k: v for k, v in [('since', since)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_worklogs_for_ids(self, ids, expand=None) -> list[Any]:
        """
        Retrieves a list of worklogs for specified IDs using the Jira API and returns their details.

        Args:
            ids (array): A list of worklog IDs.
                Example:
                ```json
                {
                  "ids": [
                    1,
                    2,
                    5,
                    10
                  ]
                }
                ```
            expand (string): Use [expand](#expansion) to include additional information about worklogs in the response. This parameter accepts `properties` that returns the properties of each worklog.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        request_body = {
            'ids': ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/api/3/worklog/list"
        query_params = {k: v for k, v in [('expand', expand)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_ids_of_worklogs_modified_since(self, since=None, expand=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of updated worklogs in Jira with optional filtering by timestamp and property expansion.

        Args:
            since (integer): The date and time, as a UNIX timestamp in milliseconds, after which updated worklogs are returned.
            expand (string): Use [expand](#expansion) to include additional information about worklogs in the response. This parameter accepts `properties` that returns the properties of each worklog.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Issue worklogs
        """
        url = f"{self.base_url}/rest/api/3/worklog/updated"
        query_params = {k: v for k, v in [('since', since), ('expand', expand)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def addon_properties_resource_get_addon_properties_get(self, addonKey) -> dict[str, Any]:
        """
        Retrieves all property keys for a specified Atlassian Connect app.

        Args:
            addonKey (string): addonKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            App properties
        """
        if addonKey is None:
            raise ValueError("Missing required parameter 'addonKey'")
        url = f"{self.base_url}/rest/atlassian-connect/1/addons/{addonKey}/properties"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def addon_properties_resource_delete_addon_property_delete(self, addonKey, propertyKey) -> Any:
        """
        Deletes a specific property of an Atlassian Connect app using the "DELETE" method, requiring the app's addon key and the property key to be specified in the request path.

        Args:
            addonKey (string): addonKey
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            App properties
        """
        if addonKey is None:
            raise ValueError("Missing required parameter 'addonKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def addon_properties_resource_get_addon_property_get(self, addonKey, propertyKey) -> dict[str, Any]:
        """
        Retrieves a specific property value for a Connect app using the provided addon key and property key.

        Args:
            addonKey (string): addonKey
            propertyKey (string): propertyKey

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            App properties
        """
        if addonKey is None:
            raise ValueError("Missing required parameter 'addonKey'")
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def dynamic_modules_resource_remove_modules_delete(self, moduleKey=None) -> Any:
        """
        Removes specified or all dynamically registered modules for the calling app via query parameters.

        Args:
            moduleKey (array): The key of the module to remove. To include multiple module keys, provide multiple copies of this parameter.
        For example, `moduleKey=dynamic-attachment-entity-property&moduleKey=dynamic-select-field`.
        Nonexistent keys are ignored.

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Dynamic modules
        """
        url = f"{self.base_url}/rest/atlassian-connect/1/app/module/dynamic"
        query_params = {k: v for k, v in [('moduleKey', moduleKey)] if v is not None}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dynamic_modules_resource_get_modules_get(self) -> dict[str, Any]:
        """
        Retrieves all dynamically registered modules for the calling Connect app in Jira.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            Dynamic modules
        """
        url = f"{self.base_url}/rest/atlassian-connect/1/app/module/dynamic"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dynamic_modules_resource_register_modules_post(self, modules) -> Any:
        """
        Registers dynamic modules in Atlassian Connect apps using the POST method, allowing the specification of modules to be registered via a JSON object.

        Args:
            modules (array): A list of app modules in the same format as the `modules` property in the
        [app descriptor](https://developer.atlassian.com/cloud/jira/platform/app-descriptor/).

        Returns:
            Any: Returned if the request is successful.

        Tags:
            Dynamic modules
        """
        request_body = {
            'modules': modules,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/atlassian-connect/1/app/module/dynamic"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def app_issue_field_value_update_resource_update_issue_fields_put(self, updateValueList=None) -> Any:
        """
        Updates multiple entity properties (up to 50 per request) for a specified object during Connect app migrations.

        Args:
            updateValueList (array): The list of custom field update details.
                Example:
                ```json
                {
                  "updateValueList": [
                    {
                      "_type": "StringIssueField",
                      "issueID": 10001,
                      "fieldID": 10076,
                      "string": "new string value"
                    },
                    {
                      "_type": "TextIssueField",
                      "issueID": 10002,
                      "fieldID": 10077,
                      "text": "new text value"
                    },
                    {
                      "_type": "SingleSelectIssueField",
                      "issueID": 10003,
                      "fieldID": 10078,
                      "optionID": "1"
                    },
                    {
                      "_type": "MultiSelectIssueField",
                      "issueID": 10004,
                      "fieldID": 10079,
                      "optionID": "2"
                    },
                    {
                      "_type": "RichTextIssueField",
                      "issueID": 10005,
                      "fieldID": 10080,
                      "richText": "new rich text value"
                    },
                    {
                      "_type": "NumberIssueField",
                      "issueID": 10006,
                      "fieldID": 10082,
                      "number": 54
                    }
                  ]
                }
                ```

        Returns:
            Any: Returned if the request is successful.

        Tags:
            App migration
        """
        request_body = {
            'updateValueList': updateValueList,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/atlassian-connect/1/migration/field"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def migration_resource_update_entity_properties_value_put(self, entityType, items) -> Any:
        """
        Updates properties for a specific entity type during Atlassian Connect app migration using the provided transfer ID.

        Args:
            entityType (string): entityType

        Returns:
            Any: Returned if the request is successful.

        Tags:
            App migration
        """
        if entityType is None:
            raise ValueError("Missing required parameter 'entityType'")
        # Use items array directly as request body
        request_body = items
        url = f"{self.base_url}/rest/atlassian-connect/1/migration/properties/{entityType}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def migration_resource_workflow_rule_search_post(self, ruleIds, workflowEntityId, expand=None) -> dict[str, Any]:
        """
        Searches for and returns workflow transition rule configurations migrated from server to cloud, owned by the calling Connect app, using the Jira Cloud REST API.

        Args:
            ruleIds (array): The list of workflow rule IDs.
            workflowEntityId (string): The workflow ID. Example: 'a498d711-685d-428d-8c3e-bc03bb450ea7'.
            expand (string): Use expand to include additional information in the response. This parameter accepts `transition` which, for each rule, returns information about the transition the rule is assigned to. Example: 'transition'.

        Returns:
            dict[str, Any]: Returned if the request is successful.

        Tags:
            App migration
        """
        request_body = {
            'expand': expand,
            'ruleIds': ruleIds,
            'workflowEntityId': workflowEntityId,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/rest/atlassian-connect/1/migration/workflow/rule/search"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def service_registry_resource_services_get(self, serviceIds) -> list[Any]:
        """
        Retrieves and registers services from the Atlassian Connect service registry using the provided service IDs.

        Args:
            serviceIds (array): The ID of the services (the strings starting with "b:" need to be decoded in Base64). Example: '["ari:cloud:graph::service/ca075ed7-6ea7-4563-acb3-000000000000/f51d7252-61e0-11ee-b94d-000000000000", "ari:cloud:graph::service/ca075ed7-6ea7-4563-acb3-000000000000/f51d7252-61e0-11ee-b94d-000000000001"]'.

        Returns:
            list[Any]: Returned if the request is successful.

        Tags:
            Service Registry
        """
        url = f"{self.base_url}/rest/atlassian-connect/1/service-registry"
        query_params = {k: v for k, v in [('serviceIds', serviceIds)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_forge_app_property(self, propertyKey) -> Any:
        """
        Deletes a property identified by the provided `propertyKey` from the application using the DELETE method and returns a successful response if the operation completes without returning any content.

        Args:
            propertyKey (string): propertyKey

        Returns:
            Any: Returned if the request is successful.

        Tags:
            App properties
        """
        if propertyKey is None:
            raise ValueError("Missing required parameter 'propertyKey'")
        url = f"{self.base_url}/rest/forge/1/app/properties/{propertyKey}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def list_tools(self):
        return [
            self.get_banner,
            self.set_banner,
            self.get_custom_fields_configurations,
            self.update_multiple_custom_field_values,
            self.get_custom_field_configuration,
            self.update_custom_field_configuration,
            self.update_custom_field_value,
            self.get_application_property,
            self.get_advanced_settings,
            self.set_application_property,
            self.get_all_application_roles,
            self.get_application_role,
            self.get_attachment_content,
            self.get_attachment_meta,
            self.get_attachment_thumbnail,
            self.remove_attachment,
            self.get_attachment,
            self.expand_attachment_for_humans,
            self.expand_attachment_for_machines,
            self.get_audit_records,
            self.get_all_system_avatars,
            self.submit_bulk_delete,
            self.get_bulk_editable_fields,
            self.submit_bulk_edit,
            self.submit_bulk_move,
            self.get_available_transitions,
            self.submit_bulk_transition,
            self.submit_bulk_unwatch,
            self.submit_bulk_watch,
            self.get_bulk_operation_progress,
            self.get_bulk_changelogs,
            self.get_all_user_data_classification_levels,
            self.get_comments_by_ids,
            self.get_comment_property_keys,
            self.delete_comment_property,
            self.get_comment_property,
            self.find_components_for_projects,
            self.create_component,
            self.delete_component,
            self.get_component,
            self.update_component,
            self.get_component_related_issues,
            self.get_configuration,
            self.get_selected_time_tracking_implementation,
            self.select_time_tracking_implementation,
            self.get_available_time_tracking_implementations,
            self.get_shared_time_tracking_configuration,
            self.set_shared_time_tracking_configuration,
            self.get_custom_field_option,
            self.get_all_dashboards,
            self.create_dashboard,
            self.bulk_edit_dashboards,
            self.get_all_available_dashboard_gadgets,
            self.get_dashboards_paginated,
            self.get_all_gadgets,
            self.add_gadget,
            self.remove_gadget,
            self.update_gadget,
            self.get_dashboard_item_property_keys,
            self.delete_dashboard_item_property,
            self.get_dashboard_item_property,
            self.delete_dashboard,
            self.get_dashboard,
            self.update_dashboard,
            self.copy_dashboard,
            self.get_policy,
            self.get_policies,
            self.get_events,
            self.analyse_expression,
            self.evaluate_jira_expression,
            self.evaluate_jsisjira_expression,
            self.get_fields,
            self.create_custom_field,
            self.remove_associations,
            self.create_associations,
            self.get_fields_paginated,
            self.get_trashed_fields_paginated,
            self.update_custom_field,
            self.get_contexts_for_field,
            self.create_custom_field_context,
            self.get_default_values,
            self.set_default_values,
            self.get_issue_type_mappings_for_contexts,
            self.get_custom_field_contexts_for_projects_and_issue_types,
            self.get_project_context_mapping,
            self.delete_custom_field_context,
            self.update_custom_field_context,
            self.add_issue_types_to_context,
            self.remove_issue_types_from_context,
            self.get_options_for_context,
            self.create_custom_field_option,
            self.update_custom_field_option,
            self.reorder_custom_field_options,
            self.delete_custom_field_option,
            self.replace_custom_field_option,
            self.assign_projects_to_custom_field_context,
            self.remove_custom_field_context_from_projects,
            self.get_contexts_for_field_deprecated,
            self.get_screens_for_field,
            self.get_all_issue_field_options,
            self.create_issue_field_option,
            self.get_selectable_issue_field_options,
            self.get_visible_issue_field_options,
            self.delete_issue_field_option,
            self.get_issue_field_option,
            self.update_issue_field_option,
            self.replace_issue_field_option,
            self.delete_custom_field,
            self.restore_custom_field,
            self.trash_custom_field,
            self.get_all_field_configurations,
            self.create_field_configuration,
            self.delete_field_configuration,
            self.update_field_configuration,
            self.get_field_configuration_items,
            self.update_field_configuration_items,
            self.get_all_field_configuration_schemes,
            self.create_field_configuration_scheme,
            self.get_field_configuration_scheme_mappings,
            self.get_field_configuration_scheme_project_mapping,
            self.assign_field_configuration_scheme_to_project,
            self.delete_field_configuration_scheme,
            self.update_field_configuration_scheme,
            self.set_field_configuration_scheme_mapping,
            self.remove_issue_types_from_global_field_configuration_scheme,
            self.create_filter,
            self.get_default_share_scope,
            self.set_default_share_scope,
            self.get_favourite_filters,
            self.get_my_filters,
            self.get_filters_paginated,
            self.delete_filter,
            self.get_filter,
            self.update_filter,
            self.reset_columns,
            self.get_columns,
            self.set_columns,
            self.delete_favourite_for_filter,
            self.set_favourite_for_filter,
            self.change_filter_owner,
            self.get_share_permissions,
            self.add_share_permission,
            self.delete_share_permission,
            self.get_share_permission,
            self.remove_group,
            self.get_group,
            self.create_group,
            self.bulk_get_groups,
            self.get_users_from_group,
            self.remove_user_from_group,
            self.add_user_to_group,
            self.find_groups,
            self.find_users_and_groups,
            self.get_license,
            self.create_issue,
            self.archive_issues_async,
            self.archive_issues,
            self.create_issues,
            self.bulk_fetch_issues,
            self.get_create_issue_meta,
            self.get_create_issue_meta_issue_types,
            self.get_create_issue_meta_issue_type_id,
            self.get_issue_limit_report,
            self.get_issue_picker_resource,
            self.bulk_set_issues_properties_list,
            self.bulk_set_issue_properties_by_issue,
            self.bulk_delete_issue_property,
            self.bulk_set_issue_property,
            self.unarchive_issues,
            self.get_is_watching_issue_bulk,
            self.delete_issue,
            self.get_issue,
            self.edit_issue,
            self.assign_issue,
            self.get_change_logs,
            self.get_change_logs_by_ids,
            self.get_comments,
            self.add_comment,
            self.delete_comment,
            self.get_comment,
            self.update_comment,
            self.get_edit_issue_meta,
            self.notify,
            self.get_issue_property_keys,
            self.delete_issue_property,
            self.get_issue_property,
            self.delete_remote_issue_link_by_global_id,
            self.get_remote_issue_links,
            self.create_or_update_remote_issue_link,
            self.delete_remote_issue_link_by_id,
            self.get_remote_issue_link_by_id,
            self.update_remote_issue_link,
            self.get_transitions,
            self.do_transition,
            self.remove_vote,
            self.get_votes,
            self.add_vote,
            self.remove_watcher,
            self.get_issue_watchers,
            self.bulk_delete_worklogs,
            self.get_issue_worklog,
            self.add_worklog,
            self.bulk_move_worklogs,
            self.delete_worklog,
            self.get_worklog,
            self.update_worklog,
            self.get_worklog_property_keys,
            self.delete_worklog_property,
            self.get_worklog_property,
            self.link_issues,
            self.delete_issue_link,
            self.get_issue_link,
            self.get_issue_link_types,
            self.create_issue_link_type,
            self.delete_issue_link_type,
            self.get_issue_link_type,
            self.update_issue_link_type,
            self.export_archived_issues,
            self.get_issue_security_schemes,
            self.create_issue_security_scheme,
            self.get_security_levels,
            self.set_default_levels,
            self.get_security_level_members,
            self.search_projects_using_security_schemes,
            self.associate_schemes_to_projects,
            self.search_security_schemes,
            self.get_issue_security_scheme,
            self.update_issue_security_scheme,
            self.get_issue_security_level_members,
            self.delete_security_scheme,
            self.add_security_level,
            self.remove_level,
            self.update_security_level,
            self.add_security_level_members,
            self.remove_member_from_security_level,
            self.get_issue_all_types,
            self.create_issue_type,
            self.get_issue_types_for_project,
            self.delete_issue_type,
            self.get_issue_type,
            self.update_issue_type,
            self.get_alternative_issue_types,
            self.get_issue_type_property_keys,
            self.delete_issue_type_property,
            self.get_issue_type_property,
            self.get_all_issue_type_schemes,
            self.create_issue_type_scheme,
            self.get_issue_type_schemes_mapping,
            self.get_issue_type_scheme_for_projects,
            self.assign_issue_type_scheme_to_project,
            self.delete_issue_type_scheme,
            self.update_issue_type_scheme,
            self.add_issue_types_to_issue_type_scheme,
            self.reorder_issue_types_in_issue_type_scheme,
            self.remove_issue_type_from_issue_type_scheme,
            self.get_issue_type_screen_schemes,
            self.create_issue_type_screen_scheme,
            self.get_issue_type_screen_scheme_mappings,
            self.get_issue_type_screen_scheme_project_associations,
            self.assign_issue_type_screen_scheme_to_project,
            self.delete_issue_type_screen_scheme,
            self.update_issue_type_screen_scheme,
            self.append_mappings_for_issue_type_screen_scheme,
            self.update_default_screen_scheme,
            self.remove_mappings_from_issue_type_screen_scheme,
            self.get_projects_for_issue_type_screen_scheme,
            self.get_auto_complete,
            self.get_auto_complete_post,
            self.get_field_auto_complete_for_query_string,
            self.get_precomputations,
            self.update_precomputations,
            self.get_precomputations_by_id,
            self.match_issues,
            self.parse_jql_queries,
            self.migrate_queries,
            self.sanitise_jql_queries,
            self.get_all_labels,
            self.get_approximate_license_count,
            self.get_approximate_application_license_count,
            self.get_my_permissions,
            self.remove_preference,
            self.get_preference,
            self.delete_locale,
            self.get_locale,
            self.set_locale,
            self.get_current_user,
            self.get_notification_schemes,
            self.create_notification_scheme,
            self.get_notification_scheme_to_project_mappings,
            self.get_notification_scheme,
            self.update_notification_scheme,
            self.add_notifications,
            self.delete_notification_scheme,
            self.remove_notification_from_notification_scheme,
            self.get_all_permissions,
            self.get_bulk_permissions,
            self.get_permitted_projects,
            self.get_all_permission_schemes,
            self.create_permission_scheme,
            self.delete_permission_scheme,
            self.get_permission_scheme,
            self.update_permission_scheme,
            self.get_permission_scheme_grants,
            self.create_permission_grant,
            self.delete_permission_scheme_entity,
            self.get_permission_scheme_grant,
            self.get_plans,
            self.create_plan,
            self.get_plan,
            self.archive_plan,
            self.duplicate_plan,
            self.get_teams,
            self.add_atlassian_team,
            self.remove_atlassian_team,
            self.get_atlassian_team,
            self.create_plan_only_team,
            self.delete_plan_only_team,
            self.get_plan_only_team,
            self.trash_plan,
            self.get_priorities,
            self.create_priority,
            self.set_default_priority,
            self.move_priorities,
            self.search_priorities,
            self.delete_priority,
            self.get_priority,
            self.update_priority,
            self.get_priority_schemes,
            self.create_priority_scheme,
            self.suggested_priorities_for_mappings,
            self.get_available_priorities_by_priority_scheme,
            self.delete_priority_scheme,
            self.update_priority_scheme,
            self.get_priorities_by_priority_scheme,
            self.get_projects_by_priority_scheme,
            self.get_all_projects,
            self.create_project,
            self.create_project_with_custom_template,
            self.get_recent,
            self.search_projects,
            self.get_all_project_types,
            self.get_all_accessible_project_types,
            self.get_project_type_by_key,
            self.get_accessible_project_type_by_key,
            self.delete_project,
            self.get_project,
            self.update_project,
            self.archive_project,
            self.update_project_avatar,
            self.delete_project_avatar,
            self.get_all_project_avatars,
            self.remove_default_project_classification,
            self.get_default_project_classification,
            self.update_default_project_classification,
            self.get_project_components_paginated,
            self.get_project_components,
            self.delete_project_asynchronously,
            self.get_features_for_project,
            self.toggle_feature_for_project,
            self.get_project_property_keys,
            self.delete_project_property,
            self.get_project_property,
            self.restore,
            self.get_project_roles,
            self.delete_actor,
            self.get_project_role,
            self.add_actor_users,
            self.set_actors,
            self.get_project_role_details,
            self.get_all_statuses,
            self.get_project_versions_paginated,
            self.get_project_versions,
            self.get_project_email,
            self.update_project_email,
            self.get_hierarchy,
            self.get_project_issue_security_scheme,
            self.get_notification_scheme_for_project,
            self.get_assigned_permission_scheme,
            self.assign_permission_scheme,
            self.get_security_levels_for_project,
            self.get_all_project_categories,
            self.create_project_category,
            self.remove_project_category,
            self.get_project_category_by_id,
            self.update_project_category,
            self.validate_project_key,
            self.get_valid_project_key,
            self.get_valid_project_name,
            self.get_resolutions,
            self.create_resolution,
            self.set_default_resolution,
            self.move_resolutions,
            self.search_resolutions,
            self.delete_resolution,
            self.get_resolution,
            self.update_resolution,
            self.get_all_project_roles,
            self.create_project_role,
            self.delete_project_role,
            self.get_project_role_by_id,
            self.partial_update_project_role,
            self.fully_update_project_role,
            self.delete_project_role_actors_from_role,
            self.get_project_role_actors_for_role,
            self.add_project_role_actors_to_role,
            self.get_screens,
            self.create_screen,
            self.add_field_to_default_screen,
            self.get_bulk_screen_tabs,
            self.delete_screen,
            self.update_screen,
            self.get_available_screen_fields,
            self.get_all_screen_tabs,
            self.add_screen_tab,
            self.delete_screen_tab,
            self.rename_screen_tab,
            self.get_all_screen_tab_fields,
            self.add_screen_tab_field,
            self.remove_screen_tab_field,
            self.move_screen_tab_field,
            self.move_screen_tab,
            self.get_screen_schemes,
            self.create_screen_scheme,
            self.delete_screen_scheme,
            self.update_screen_scheme,
            self.search_for_issues_using_jql,
            self.search_for_issues_using_jql_post,
            self.count_issues,
            self.search_for_issues_ids,
            self.search_and_reconsile_issues_using_jql,
            self.search_and_reconsile_issues_using_jql_post,
            self.get_issue_security_level,
            self.get_server_info,
            self.get_issue_navigator_default_columns,
            self.get_statuses,
            self.get_status,
            self.get_status_categories,
            self.get_status_category,
            self.delete_statuses_by_id,
            self.get_statuses_by_id,
            self.create_statuses,
            self.update_statuses,
            self.search,
            self.get_project_issue_type_usages_for_status,
            self.get_project_usages_for_status,
            self.get_workflow_usages_for_status,
            self.get_task,
            self.cancel_task,
            self.get_ui_modifications,
            self.create_ui_modification,
            self.delete_ui_modification,
            self.update_ui_modification,
            self.get_avatars,
            self.delete_avatar,
            self.get_avatar_image_by_type,
            self.get_avatar_image_by_id,
            self.get_avatar_image_by_owner,
            self.remove_user,
            self.get_user,
            self.create_user,
            self.find_bulk_assignable_users,
            self.find_assignable_users,
            self.bulk_get_users,
            self.bulk_get_users_migration,
            self.reset_user_columns,
            self.get_user_default_columns,
            self.get_user_email,
            self.get_user_email_bulk,
            self.get_user_groups,
            self.get_user_nav_property,
            self.find_users_with_all_permissions,
            self.find_users_for_picker,
            self.get_user_property_keys,
            self.delete_user_property,
            self.get_user_property,
            self.find_users,
            self.find_users_by_query,
            self.find_user_keys_by_query,
            self.find_users_with_browse_permission,
            self.get_all_users_default,
            self.get_all_users,
            self.create_version,
            self.delete_version,
            self.get_version,
            self.update_version,
            self.merge_versions,
            self.move_version,
            self.get_version_related_issues,
            self.get_related_work,
            self.create_related_work,
            self.update_related_work,
            self.delete_and_replace_version,
            self.get_version_unresolved_issues,
            self.delete_related_work,
            self.delete_webhook_by_id,
            self.get_dynamic_webhooks_for_app,
            self.register_dynamic_webhooks,
            self.get_failed_webhooks,
            self.refresh_webhooks,
            self.get_all_workflows,
            self.create_workflow,
            self.get_workflow_transition_rule_configurations,
            self.update_workflow_transition_rule_configurations,
            self.delete_workflow_transition_rule_configurations,
            self.get_workflows_paginated,
            self.delete_workflow_transition_property,
            self.get_workflow_transition_properties,
            self.create_workflow_transition_property,
            self.update_workflow_transition_property,
            self.delete_inactive_workflow,
            self.get_workflow_project_issue_type_usages,
            self.get_project_usages_for_workflow,
            self.get_workflow_scheme_usages_for_workflow,
            self.read_workflows,
            self.workflow_capabilities,
            self.create_workflows,
            self.validate_create_workflows,
            self.search_workflows,
            self.update_workflows,
            self.validate_update_workflows,
            self.get_all_workflow_schemes,
            self.create_workflow_scheme,
            self.get_workflow_scheme_project_associations,
            self.assign_scheme_to_project,
            self.read_workflow_schemes,
            self.update_schemes,
            self.update_workflow_scheme_mappings,
            self.delete_workflow_scheme,
            self.get_workflow_scheme,
            self.update_workflow_scheme,
            self.create_workflow_scheme_draft_from_parent,
            self.delete_default_workflow,
            self.get_default_workflow,
            self.update_default_workflow,
            self.delete_workflow_scheme_draft,
            self.get_workflow_scheme_draft,
            self.update_workflow_scheme_draft,
            self.delete_draft_default_workflow,
            self.get_draft_default_workflow,
            self.update_draft_default_workflow,
            self.delete_workflow_scheme_draft_issue_type,
            self.get_workflow_scheme_draft_issue_type,
            self.set_workflow_scheme_draft_issue_type,
            self.publish_draft_workflow_scheme,
            self.delete_draft_workflow_mapping,
            self.get_draft_workflow,
            self.update_draft_workflow_mapping,
            self.delete_workflow_scheme_issue_type,
            self.get_workflow_scheme_issue_type,
            self.set_workflow_scheme_issue_type,
            self.delete_workflow_mapping,
            self.get_workflow,
            self.update_workflow_mapping,
            self.get_project_usages_for_workflow_scheme,
            self.get_ids_of_worklogs_deleted_since,
            self.get_worklogs_for_ids,
            self.get_ids_of_worklogs_modified_since,
            self.addon_properties_resource_get_addon_properties_get,
            self.addon_properties_resource_delete_addon_property_delete,
            self.addon_properties_resource_get_addon_property_get,
            self.dynamic_modules_resource_remove_modules_delete,
            self.dynamic_modules_resource_get_modules_get,
            self.dynamic_modules_resource_register_modules_post,
            self.app_issue_field_value_update_resource_update_issue_fields_put,
            self.migration_resource_update_entity_properties_value_put,
            self.migration_resource_workflow_rule_search_post,
            self.service_registry_resource_services_get,
            self.delete_forge_app_property
        ]
