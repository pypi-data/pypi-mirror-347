from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration

class SlackApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='slackapp', integration=integration, **kwargs)
        self.base_url = "https://slack.com/api"

    def adminapps_approve_app_installation(self, app_id=None, request_id=None, team_id=None) -> dict[str, Any]:
        """
        Approves an app install request for a specific workspace or across an entire enterprise using the Slack App Management API.

        Args:
            app_id (string): The id of the app to approve.
            request_id (string): The id of the request to approve.
            team_id (string): team_id

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.apps, admin
        """
        request_body = {
            'app_id': app_id,
            'request_id': request_id,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.apps.approve"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminappsapproved_list(self, token, limit=None, cursor=None, team_id=None, enterprise_id=None) -> dict[str, Any]:
        """
        Retrieves a list of approved apps for administrators using the Slack API, with optional filtering by team, enterprise, and pagination controls.

        Args:
            token (string): A required string parameter used for authentication in the query string of the GET operation, necessary for accessing the list of approved admin apps.
            limit (integer): The maximum number of approved apps to return in the response.
            cursor (string): A string parameter used for cursor-based pagination, allowing retrieval of data in a specific order by referencing a unique identifier, such as a timestamp or encoded token, to fetch subsequent pages.
            team_id (string): The `team_id` parameter filters the list of approved apps by a specific team identifier.
            enterprise_id (string): The `enterprise_id` query parameter is a string value used to filter the list of approved applications by the specified enterprise ID during the GET operation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.apps.approved, admin
        """
        url = f"{self.base_url}/admin.apps.approved.list"
        query_params = {k: v for k, v in [('token', token), ('limit', limit), ('cursor', cursor), ('team_id', team_id), ('enterprise_id', enterprise_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminappsrequests_list(self, token, limit=None, cursor=None, team_id=None) -> dict[str, Any]:
        """
        Lists pending app installation requests for a Slack Enterprise Grid workspace, allowing filtering by team and pagination.

        Args:
            token (string): The token parameter is a required string passed in the query to authenticate and authorize the request for listing admin app requests.
            limit (integer): Specifies the maximum number of results to include in the response for the list of admin app requests.
            cursor (string): An opaque token used for cursor-based pagination, specifying the starting point for fetching the next set of results in the list of admin app requests.
            team_id (string): Filters the list of admin app requests to include only those associated with the specified team ID.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.apps.requests, admin
        """
        url = f"{self.base_url}/admin.apps.requests.list"
        query_params = {k: v for k, v in [('token', token), ('limit', limit), ('cursor', cursor), ('team_id', team_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminapps_restrict_app(self, app_id=None, request_id=None, team_id=None) -> dict[str, Any]:
        """
        Restricts an app for installation on a specific workspace or across an entire enterprise using the Slack API, preventing future installations while retaining existing ones.

        Args:
            app_id (string): The id of the app to restrict.
            request_id (string): The id of the request to restrict.
            team_id (string): team_id

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.apps, admin
        """
        request_body = {
            'app_id': app_id,
            'request_id': request_id,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.apps.restrict"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminappsrestricted_get_list(self, token, limit=None, cursor=None, team_id=None, enterprise_id=None) -> dict[str, Any]:
        """
        Retrieves a list of restricted apps for a team or enterprise using the Slack API, allowing administrators to manage app restrictions based on provided parameters such as team ID, enterprise ID, and pagination options.

        Args:
            token (string): Required security token for authentication, passed as a query parameter for accessing restricted admin applications list.
            limit (integer): Specifies the maximum number of restricted applications to return in the response.
            cursor (string): A unique identifier or token used to mark the position in the dataset, allowing the retrieval of the next page of results in a paginated list.
            team_id (string): ID of the team to filter the list of restricted apps.
            enterprise_id (string): Filters the results to include only applications restricted to the specified enterprise identifier.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.apps.restricted, admin
        """
        url = f"{self.base_url}/admin.apps.restricted.list"
        query_params = {k: v for k, v in [('token', token), ('limit', limit), ('cursor', cursor), ('team_id', team_id), ('enterprise_id', enterprise_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversations_archive_channel(self, channel_id) -> dict[str, Any]:
        """
        Archives a public or private channel across an entire Enterprise Grid organization using an admin-level token with the required scope.

        Args:
            channel_id (string): The channel to archive.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.archive"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_convert_to_private_channel(self, channel_id) -> dict[str, Any]:
        """
        Converts a public channel to a private channel in Slack using the admin API, available only for Enterprise Grid workspaces.

        Args:
            channel_id (string): The channel to convert to private.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.convertToPrivate"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_create_channel_based_conversation(self, is_private, name, description=None, org_wide=None, team_id=None) -> dict[str, Any]:
        """
        Creates a new public or private channel in an Enterprise Grid organization using the Slack Admin API, requiring the `admin.conversations:write` scope.

        Args:
            is_private (boolean): When `true`, creates a private channel instead of a public channel
            name (string): Name of the public or private channel to create.
            description (string): Description of the public or private channel to create.
            org_wide (boolean): When `true`, the channel will be available org-wide. Note: if the channel is not `org_wide=true`, you must specify a `team_id` for this channel
            team_id (string): The workspace to create the channel in. Note: this argument is required unless you set `org_wide=true`.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'description': description,
            'is_private': is_private,
            'name': name,
            'org_wide': org_wide,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_delete_channel(self, channel_id) -> dict[str, Any]:
        """
        Deletes a public or private channel using the Slack API and returns a success status message.

        Args:
            channel_id (string): The channel to delete.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_disconnect_shared_channel(self, channel_id, leaving_team_ids=None) -> dict[str, Any]:
        """
        Disconnects one or more workspaces from a connected channel using the Slack Admin API, requiring an authentication token with the `admin.conversations:write` scope.

        Args:
            channel_id (string): The channel to be disconnected from some workspaces.
            leaving_team_ids (string): The team to be removed from the channel. Currently only a single team id can be specified.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
            'leaving_team_ids': leaving_team_ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.disconnectShared"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversationsekm_list_original_connected_channel_info(self, token, channel_ids=None, team_ids=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves original connected channel IDs for EKM encryption keys, allowing for key revocation on read-only channels, and lists disconnected channels that were once connected to other workspaces.

        Args:
            token (string): A required string parameter passed in the query string to authenticate and authorize access to the original connected channel information list.
            channel_ids (string): A comma-separated list of channel IDs to filter the original connected channel information retrieved by the API.
            team_ids (string): Comma-separated list of team IDs to filter the original connected channel information results.
            limit (integer): Specifies the maximum number of original connected channel information records to return in the response.
            cursor (string): A cursor string used for pagination to retrieve the next set of results in the list.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations.ekm, admin
        """
        url = f"{self.base_url}/admin.conversations.ekm.listOriginalConnectedChannelInfo"
        query_params = {k: v for k, v in [('token', token), ('channel_ids', channel_ids), ('team_ids', team_ids), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversations_get_conversation_prefs(self, channel_id) -> dict[str, Any]:
        """
        Retrieves the posting and threading permissions (conversation preferences) for a specified public or private channel in an Enterprise Grid workspace.

        Args:
            channel_id (string): **channel_id**: A required string parameter specifying the unique identifier of the channel for which conversation preferences are to be retrieved.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        url = f"{self.base_url}/admin.conversations.getConversationPrefs"
        query_params = {k: v for k, v in [('channel_id', channel_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversations_get_teams_list(self, channel_id, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a list of workspaces connected to a specified public or private channel within an Enterprise Grid organization using the Slack API.

        Args:
            channel_id (string): The unique identifier of the channel for which to retrieve team conversation details; this parameter is required and passed in the query string.
            cursor (string): A string parameter used for cursor-based pagination, providing a unique identifier to fetch the next page of results in a specific order.
            limit (integer): Specifies the maximum number of teams returned in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        url = f"{self.base_url}/admin.conversations.getTeams"
        query_params = {k: v for k, v in [('channel_id', channel_id), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversations_invite_user_to_channel(self, channel_id, user_ids) -> dict[str, Any]:
        """
        Invites users to a public or private channel using the Slack Admin API, requiring an authentication token with the `admin.conversations:write` scope.

        Args:
            channel_id (string): The channel that the users will be invited to.
            user_ids (string): The users to invite.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
            'user_ids': user_ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.invite"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_rename_channel(self, channel_id, name) -> dict[str, Any]:
        """
        Renames a public or private channel in an Enterprise Grid workspace using admin privileges.

        Args:
            channel_id (string): The channel to rename.
            name (string): name

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.rename"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversationsrestrict_access_add_group_idp_groups(self, channel_id, group_id, token, team_id=None) -> dict[str, Any]:
        """
        Adds an IDP group to a private Slack channel's allowlist, allowing only members of the specified group to access the channel, requiring the `admin.conversations:write` OAuth scope.

        Args:
            channel_id (string): The channel to link this group to.
            group_id (string): The [IDP Group](https://slack.com/help/articles/115001435788-Connect-identity-provider-groups-to-your-Enterprise-Grid-org) ID to be an allowlist for the private channel.
            token (string): Authentication token. Requires scope: `admin.conversations:write`
            team_id (string): The workspace where the channel exists. This argument is required for channels only tied to one workspace, and optional for channels that are shared across an organization.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations.restrictAccess, admin
        """
        request_body = {
            'channel_id': channel_id,
            'group_id': group_id,
            'team_id': team_id,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.restrictAccess.addGroup"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversationsrestrict_access_list_groups(self, token, channel_id, team_id=None) -> dict[str, Any]:
        """
        Lists the IDP groups with access to a specified private channel on Slack using the Enterprise Grid workspace, requiring the channel ID and an authentication token with the necessary admin scope.

        Args:
            token (string): Required authentication token for accessing restricted group listings.
            channel_id (string): The **channel_id** parameter, required for the listGroups operation, specifies the unique identifier of the channel for which to retrieve restricted access groups.
            team_id (string): Optional identifier for the workspace where the channel exists, required only if the channel is tied to a single workspace, but optional for channels shared across multiple workspaces.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations.restrictAccess, admin
        """
        url = f"{self.base_url}/admin.conversations.restrictAccess.listGroups"
        query_params = {k: v for k, v in [('token', token), ('channel_id', channel_id), ('team_id', team_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversationsrestrict_access_remove_idp_group(self, channel_id, group_id, team_id, token) -> dict[str, Any]:
        """
        Removes an IDP group from a private channel's allowlist using the Slack API, potentially removing members who are only part of this group.

        Args:
            channel_id (string): The channel to remove the linked group from.
            group_id (string): The [IDP Group](https://slack.com/help/articles/115001435788-Connect-identity-provider-groups-to-your-Enterprise-Grid-org) ID to remove from the private channel.
            team_id (string): The workspace where the channel exists. This argument is required for channels only tied to one workspace, and optional for channels that are shared across an organization.
            token (string): Authentication token. Requires scope: `admin.conversations:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations.restrictAccess, admin
        """
        request_body = {
            'channel_id': channel_id,
            'group_id': group_id,
            'team_id': team_id,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.restrictAccess.removeGroup"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_search_channels(self, team_ids=None, query=None, limit=None, cursor=None, search_channel_types=None, sort=None, sort_dir=None) -> dict[str, Any]:
        """
        Searches for public or private channels across specified teams in an Enterprise organization using a search query, with options to filter by channel type and sort results.

        Args:
            team_ids (string): A comma-separated string of team IDs to filter the search results to conversations within those teams.
            query (string): The search query string used to specify the search terms for finding conversations in the admin context.
            limit (integer): The maximum number of conversation results to return in the response.
            cursor (string): A cursor string used for pagination to retrieve the next set of conversation search results starting from a specific position.
            search_channel_types (string): A comma-separated string specifying channel types to include or exclude in the search results, such as private, archived, or external shared channels, allowing filtering by any of the provided types.
            sort (string): Specifies the field to sort the results by; for example, "sort=date" would sort conversations by date.
            sort_dir (string): The "sort_dir" query parameter specifies the direction of sorting for the search results, typically accepting values like "asc" for ascending or "desc" for descending order.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        url = f"{self.base_url}/admin.conversations.search"
        query_params = {k: v for k, v in [('team_ids', team_ids), ('query', query), ('limit', limit), ('cursor', cursor), ('search_channel_types', search_channel_types), ('sort', sort), ('sort_dir', sort_dir)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminconversations_set_conversation_prefs(self, channel_id, prefs) -> dict[str, Any]:
        """
        Sets the posting and threading permissions for a public or private Slack channel using the `admin.conversations.setConversationPrefs` API operation.

        Args:
            channel_id (string): The channel to set the prefs for
            prefs (string): The prefs for this channel in a stringified JSON format.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
            'prefs': prefs,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.setConversationPrefs"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_set_teams_workspace_connection(self, channel_id, org_channel=None, target_team_ids=None, team_id=None) -> dict[str, Any]:
        """
        Sets or updates the workspaces connected to a channel in an Enterprise Grid organization, allowing the channel to be configured as a regular or shared channel across specified workspaces.

        Args:
            channel_id (string): The encoded `channel_id` to add or remove to workspaces.
            org_channel (boolean): True if channel has to be converted to an org channel
            target_team_ids (string): A comma-separated list of workspaces to which the channel should be shared. Not required if the channel is being shared org-wide.
            team_id (string): The workspace to which the channel belongs. Omit this argument if the channel is a cross-workspace shared channel.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
            'org_channel': org_channel,
            'target_team_ids': target_team_ids,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.setTeams"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminconversations_unarchive_channel(self, channel_id) -> dict[str, Any]:
        """
        Unarchives a public or private Slack channel using the Slack Admin API with a "POST" request.

        Args:
            channel_id (string): The channel to unarchive.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.conversations, admin
        """
        request_body = {
            'channel_id': channel_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.conversations.unarchive"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminemoji_add_emoji(self, name, token, url) -> dict[str, Any]:
        """
        Adds a custom emoji across an Enterprise Grid organization using the Slack Admin API.

        Args:
            name (string): The name of the emoji to be removed. Colons (`:myemoji:`) around the value are not required, although they may be included.
            token (string): Authentication token. Requires scope: `admin.teams:write`
            url (string): The URL of a file to use as an image for the emoji. Square images under 128KB and with transparent backgrounds work best.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.emoji, admin
        """
        request_body = {
            'name': name,
            'token': token,
            'url': url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.emoji.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminemoji_alias_add(self, alias_for, name, token) -> dict[str, Any]:
        """
        Adds an alias for an existing emoji across an Enterprise Grid organization using Slack's Admin API, requiring the `admin.teams:write` scope.

        Args:
            alias_for (string): The alias of the emoji.
            name (string): The name of the emoji to be aliased. Colons (`:myemoji:`) around the value are not required, although they may be included.
            token (string): Authentication token. Requires scope: `admin.teams:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.emoji, admin
        """
        request_body = {
            'alias_for': alias_for,
            'name': name,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.emoji.addAlias"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminemoji_list_enterprise_emoji(self, token, cursor=None, limit=None) -> dict[str, Any]:
        """
        Lists custom emoji across an entire Enterprise Grid organization for admins using a token with the required admin scope.

        Args:
            token (string): Required authentication token for validating access to the list of emojis via the GET operation.
            cursor (string): A cursor string used for pagination to fetch the next set of emoji data from the list.
            limit (integer): Specifies the maximum number of items to return in the response for the emoji list.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.emoji, admin
        """
        url = f"{self.base_url}/admin.emoji.list"
        query_params = {k: v for k, v in [('token', token), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminemoji_remove_enterprise_emoji(self, name, token) -> dict[str, Any]:
        """
        Removes a custom emoji from an entire Enterprise Grid organization using the Slack Admin API with required admin authentication.

        Args:
            name (string): The name of the emoji to be removed. Colons (`:myemoji:`) around the value are not required, although they may be included.
            token (string): Authentication token. Requires scope: `admin.teams:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.emoji, admin
        """
        request_body = {
            'name': name,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.emoji.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminemoji_rename_emoji(self, name, new_name, token) -> dict[str, Any]:
        """
        Renames a custom emoji across an Enterprise Grid organization using the Slack Admin API.

        Args:
            name (string): The name of the emoji to be renamed. Colons (`:myemoji:`) around the value are not required, although they may be included.
            new_name (string): The new name of the emoji.
            token (string): Authentication token. Requires scope: `admin.teams:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.emoji, admin
        """
        request_body = {
            'name': name,
            'new_name': new_name,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.emoji.rename"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def admininvite_requests_approve_request(self, invite_request_id=None, team_id=None) -> dict[str, Any]:
        """
        Approves an invite request using the Slack API, requiring admin authentication.

        Args:
            invite_request_id (string): ID of the request to invite.
            team_id (string): ID for the workspace where the invite request was made.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.inviteRequests, admin
        """
        request_body = {
            'invite_request_id': invite_request_id,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.inviteRequests.approve"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def admininvite_requestsapproved_list(self, team_id=None, cursor=None, limit=None) -> dict[str, Any]:
        """
        Lists all approved workspace invite requests in a Slack organization, supporting pagination and filtering by team.

        Args:
            team_id (string): The team_id query parameter specifies the ID of the team for which the approved invite requests should be listed.
            cursor (string): A string token used for cursor-based pagination to retrieve the next set of approved invite requests in the list.
            limit (integer): Specifies the maximum number of approved invite requests to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.inviteRequests.approved, admin
        """
        url = f"{self.base_url}/admin.inviteRequests.approved.list"
        query_params = {k: v for k, v in [('team_id', team_id), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def admininvite_requestsdenied_list(self, team_id=None, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a list of denied invite requests for a Slack workspace using the "GET" method, requiring authentication via a Slack token with admin privileges.

        Args:
            team_id (string): Identifies the team ID to filter denied invite requests by team membership.
            cursor (string): A string cursor used to fetch the next or previous page of invite requests, typically included in the request to specify the starting point for data retrieval.
            limit (integer): The `limit` parameter specifies the maximum number of denied invite requests to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.inviteRequests.denied, admin
        """
        url = f"{self.base_url}/admin.inviteRequests.denied.list"
        query_params = {k: v for k, v in [('team_id', team_id), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def admininvite_requests_deny_request(self, invite_request_id=None, team_id=None) -> dict[str, Any]:
        """
        Denies an invitation request using the POST method with admin-level access.

        Args:
            invite_request_id (string): ID of the request to invite.
            team_id (string): ID for the workspace where the invite request was made.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.inviteRequests, admin
        """
        request_body = {
            'invite_request_id': invite_request_id,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.inviteRequests.deny"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def admininvite_requests_list_pending_workspace_invite_requests(self, team_id=None, cursor=None, limit=None) -> dict[str, Any]:
        """
        Lists all pending invite requests for a specified Slack workspace, requiring an admin token with the "admin.invites:read" scope.

        Args:
            team_id (string): Filters the list of invite requests by specifying the ID of the team for which the requests should be retrieved.
            cursor (string): A string cursor used for pagination, indicating the position from which to retrieve the next set of invite requests.
            limit (integer): The maximum number of invite requests to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.inviteRequests, admin
        """
        url = f"{self.base_url}/admin.inviteRequests.list"
        query_params = {k: v for k, v in [('team_id', team_id), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminteamsadmins_get_all(self, token, team_id, limit=None, cursor=None) -> dict[str, Any]:
        """
        Lists all administrators of a specified workspace within an Enterprise Grid organization using the Slack Admin API.

        Args:
            token (string): The token parameter in the query is a required string used to authenticate and authorize the request for listing team admins.
            team_id (string): Identifier of the team for which to retrieve a list of admins, required for successful API invocation.
            limit (integer): The "limit" parameter specifies the maximum number of results to return in the response for the list of admins.
            cursor (string): The cursor parameter is a string used for cursor-based pagination to specify the position in the dataset from which to continue listing team admins in subsequent requests.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.admins, admin
        """
        url = f"{self.base_url}/admin.teams.admins.list"
        query_params = {k: v for k, v in [('token', token), ('limit', limit), ('cursor', cursor), ('team_id', team_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminteams_create_enterprise_team(self, team_domain, team_name, team_description=None, team_discoverability=None) -> dict[str, Any]:
        """
        Creates a new workspace for an enterprise organization using the Slack Admin API, requiring authentication and specific team details.

        Args:
            team_domain (string): Team domain (for example, slacksoftballteam).
            team_name (string): Team name (for example, Slack Softball Team).
            team_description (string): Description for the team.
            team_discoverability (string): Who can join the team. A team's discoverability can be `open`, `closed`, `invite_only`, or `unlisted`.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams, admin
        """
        request_body = {
            'team_description': team_description,
            'team_discoverability': team_discoverability,
            'team_domain': team_domain,
            'team_name': team_name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminteams_list_all(self, limit=None, cursor=None) -> dict[str, Any]:
        """
        Lists all teams in an Enterprise organization using the Slack API, returning details such as team IDs, names, and primary owners.

        Args:
            limit (integer): Specifies the maximum number of team records to return in the response.
            cursor (string): A cursor string used for pagination to fetch the next set of results in the list of teams.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams, admin
        """
        url = f"{self.base_url}/admin.teams.list"
        query_params = {k: v for k, v in [('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminteamsowners_list_owners(self, token, team_id, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a list of owners for a specified team using the provided team ID, optionally filtering results by limit and cursor, and authenticates via Slack admin authentication.

        Args:
            token (string): Required token for authentication, passed as a query parameter to authorize access to the list of team owners.
            team_id (string): The team_id parameter is a required string value passed in the query string to identify the specific team for which to list owners.
            limit (integer): Specifies the maximum number of team owners to be returned in the response.
            cursor (string): A unique identifier used for cursor-based pagination, specifying the position from which to retrieve the next set of team owners.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.owners, admin
        """
        url = f"{self.base_url}/admin.teams.owners.list"
        query_params = {k: v for k, v in [('token', token), ('team_id', team_id), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminteamssettings_get_info(self, team_id) -> dict[str, Any]:
        """
        Retrieves settings information for a specified team using the Slack API and requires an authentication token with appropriate admin scopes.

        Args:
            team_id (string): Required identifier for the team whose settings information is to be retrieved.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        url = f"{self.base_url}/admin.teams.settings.info"
        query_params = {k: v for k, v in [('team_id', team_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminteamssettings_set_default_channels(self, channel_ids, team_id, token) -> dict[str, Any]:
        """
        Sets the default channels of a Slack workspace using the Slack Admin API, ensuring new members are automatically added to these channels upon joining.

        Args:
            channel_ids (string): An array of channel IDs.
            team_id (string): ID for the workspace to set the default channel for.
            token (string): Authentication token. Requires scope: `admin.teams:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        request_body = {
            'channel_ids': channel_ids,
            'team_id': team_id,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.settings.setDefaultChannels"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminteamssettings_set_description(self, description, team_id) -> dict[str, Any]:
        """
        Sets the description of a specified Slack workspace using the Slack API, requiring an authentication token with the `admin.teams:write` scope.

        Args:
            description (string): The new description for the workspace.
            team_id (string): ID for the workspace to set the description for.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        request_body = {
            'description': description,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.settings.setDescription"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminteamssettings_set_discoverability_of_workspace(self, discoverability, team_id) -> dict[str, Any]:
        """
        Sets the discoverability of a Slack workspace using the Slack Admin API, allowing admins to control whether a workspace is visible to others within an Enterprise Grid organization.

        Args:
            discoverability (string): This workspace's discovery setting. It must be set to one of `open`, `invite_only`, `closed`, or `unlisted`.
            team_id (string): The ID of the workspace to set discoverability on.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        request_body = {
            'discoverability': discoverability,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.settings.setDiscoverability"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminteamssettings_set_icon(self, image_url, team_id, token) -> dict[str, Any]:
        """
        Sets the icon of a Slack workspace using the Slack API and requires the "admin.teams:write" scope, returning a success status message upon completion.

        Args:
            image_url (string): Image URL for the icon
            team_id (string): ID for the workspace to set the icon for.
            token (string): Authentication token. Requires scope: `admin.teams:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        request_body = {
            'image_url': image_url,
            'team_id': team_id,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.settings.setIcon"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminteamssettings_set_name(self, name, team_id) -> dict[str, Any]:
        """
        Sets the name of a specified Enterprise Grid workspace using the Slack Admin API with required authentication and permissions.

        Args:
            name (string): The new name of the workspace.
            team_id (string): ID for the workspace to set the name for.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.teams.settings, admin
        """
        request_body = {
            'name': name,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.teams.settings.setName"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusergroups_add_default_channels(self, channel_ids, usergroup_id, team_id=None) -> dict[str, Any]:
        """
        Adds one or more default channels to an IDP group in an Enterprise Grid workspace using the Slack API.

        Args:
            channel_ids (string): Comma separated string of channel IDs.
            usergroup_id (string): ID of the IDP group to add default channels for.
            team_id (string): The workspace to add default channels in.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.usergroups, admin
        """
        request_body = {
            'channel_ids': channel_ids,
            'team_id': team_id,
            'usergroup_id': usergroup_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.usergroups.addChannels"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusergroups_associate_default_workspaces(self, team_ids, usergroup_id, auto_provision=None) -> dict[str, Any]:
        """
        Adds teams to user groups using the provided request body and returns a status message if successful.

        Args:
            team_ids (string): A comma separated list of encoded team (workspace) IDs. Each workspace *MUST* belong to the organization associated with the token.
            usergroup_id (string): An encoded usergroup (IDP Group) ID.
            auto_provision (boolean): When `true`, this method automatically creates new workspace accounts for the IDP group members.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.usergroups, admin
        """
        request_body = {
            'auto_provision': auto_provision,
            'team_ids': team_ids,
            'usergroup_id': usergroup_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.usergroups.addTeams"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusergroups_list_channels_get(self, usergroup_id, team_id=None, include_num_members=None) -> dict[str, Any]:
        """
        Retrieves a list of channels linked to an org-level IDP group (user group) using the Slack API, requiring a user group ID and supporting optional parameters for team ID and member count inclusion.

        Args:
            usergroup_id (string): Required string identifier for the user group, used to filter channels in the response.
            team_id (string): Identifies the specific team for which to retrieve user group channels.
            include_num_members (boolean): Whether to include the number of members in the response for the listed channels.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.usergroups, admin
        """
        url = f"{self.base_url}/admin.usergroups.listChannels"
        query_params = {k: v for k, v in [('usergroup_id', usergroup_id), ('team_id', team_id), ('include_num_members', include_num_members)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminusergroups_remove_channels(self, channel_ids, usergroup_id) -> dict[str, Any]:
        """
        Removes one or more default channels from an org-level IDP group (user group) using the Slack API.

        Args:
            channel_ids (string): Comma-separated string of channel IDs
            usergroup_id (string): ID of the IDP Group

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.usergroups, admin
        """
        request_body = {
            'channel_ids': channel_ids,
            'usergroup_id': usergroup_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.usergroups.removeChannels"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_add_workspace_user(self, team_id, user_id, channel_ids=None, is_restricted=None, is_ultra_restricted=None) -> dict[str, Any]:
        """
        Assigns or reinstates a user to an Enterprise Grid workspace, adding them as a member or guest as specified, and reactivating their account if previously deactivated.

        Args:
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): The ID of the user to add to the workspace.
            channel_ids (string): Comma separated values of channel IDs to add user in the new workspace.
            is_restricted (boolean): True if user should be added to the workspace as a guest.
            is_ultra_restricted (boolean): True if user should be added to the workspace as a single-channel guest.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'channel_ids': channel_ids,
            'is_restricted': is_restricted,
            'is_ultra_restricted': is_ultra_restricted,
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.assign"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_invite_user_to_workspace(self, channel_ids, email, team_id, custom_message=None, guest_expiration_ts=None, is_restricted=None, is_ultra_restricted=None, real_name=None, resend=None) -> dict[str, Any]:
        """
        Invites a user to a Slack workspace using the Slack API and requires an authentication token with the necessary scopes.

        Args:
            channel_ids (string): A comma-separated list of `channel_id`s for this user to join. At least one channel is required.
            email (string): The email address of the person to invite.
            team_id (string): The ID (`T1234`) of the workspace.
            custom_message (string): An optional message to send to the user in the invite email.
            guest_expiration_ts (string): Timestamp when guest account should be disabled. Only include this timestamp if you are inviting a guest user and you want their account to expire on a certain date.
            is_restricted (boolean): Is this user a multi-channel guest user? (default: false)
            is_ultra_restricted (boolean): Is this user a single channel guest user? (default: false)
            real_name (string): Full name of the user.
            resend (boolean): Allow this invite to be resent in the future if a user has not signed up yet. (default: false)

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'channel_ids': channel_ids,
            'custom_message': custom_message,
            'email': email,
            'guest_expiration_ts': guest_expiration_ts,
            'is_restricted': is_restricted,
            'is_ultra_restricted': is_ultra_restricted,
            'real_name': real_name,
            'resend': resend,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.invite"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_list_workspace_users(self, team_id, cursor=None, limit=None) -> dict[str, Any]:
        """
        Lists users in an Enterprise Grid workspace, supporting pagination and filtering by team ID, requiring an admin token with the appropriate scope.

        Args:
            team_id (string): **team_id**: A required string parameter identifying the team for which to list users.
            cursor (string): Opaque token used to fetch the next or previous page of users, typically provided by the server in response to a previous request.
            limit (integer): The "limit" parameter specifies the maximum number of user records to return in a single response for the GET operation at "/admin.users.list".

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        url = f"{self.base_url}/admin.users.list"
        query_params = {k: v for k, v in [('team_id', team_id), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def adminusers_remove_user_from_workspace(self, team_id, user_id) -> dict[str, Any]:
        """
        Removes a user from a Slack workspace using the Slack API and returns a status message, requiring a valid authentication token with the "admin.users:write" scope.

        Args:
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): The ID of the user to remove.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminuserssession_invalidate_session(self, session_id, team_id) -> dict[str, Any]:
        """
        Invalidates a single user session on a Slack workspace, logging the user out of that session while leaving other active sessions unaffected.

        Args:
            session_id (integer): session_id
            team_id (string): ID of the team that the session belongs to

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users.session, admin
        """
        request_body = {
            'session_id': session_id,
            'team_id': team_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.session.invalidate"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminuserssession_reset_sessions(self, user_id, mobile_only=None, web_only=None) -> dict[str, Any]:
        """
        Resets all active sessions for a specified user in an Enterprise Grid workspace, unauthenticating the user and causing their Slack clients to clear local caches.

        Args:
            user_id (string): The ID of the user to wipe sessions for
            mobile_only (boolean): Only expire mobile sessions (default: false)
            web_only (boolean): Only expire web sessions (default: false)

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users.session, admin
        """
        request_body = {
            'mobile_only': mobile_only,
            'user_id': user_id,
            'web_only': web_only,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.session.reset"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_set_admin_user(self, team_id, user_id) -> dict[str, Any]:
        """
        Promotes an existing user to a workspace administrator role using the Slack API and requires the "admin.users:write" permission scope.

        Args:
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): The ID of the user to designate as an admin.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.setAdmin"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_set_expiration_guest(self, expiration_ts, team_id, user_id) -> dict[str, Any]:
        """
        Sets an expiration for a guest user in a Slack workspace using the Slack Admin API, requiring an authentication token and details such as expiration timestamp, team ID, and user ID.

        Args:
            expiration_ts (integer): Timestamp when guest account should be disabled.
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): The ID of the user to set an expiration for.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'expiration_ts': expiration_ts,
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.setExpiration"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_set_workspace_owner(self, team_id, user_id) -> dict[str, Any]:
        """
        Sets an existing regular user or admin as a workspace owner in an Enterprise Grid workspace using the Slack API.

        Args:
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): Id of the user to promote to owner.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.setOwner"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def adminusers_set_regular_user(self, team_id, user_id) -> dict[str, Any]:
        """
        Converts an existing guest user, admin user, or owner in an Enterprise Grid workspace to a regular user.

        Args:
            team_id (string): The ID (`T1234`) of the workspace.
            user_id (string): The ID of the user to designate as a regular user.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            admin.users, admin
        """
        request_body = {
            'team_id': team_id,
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/admin.users.setRegular"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def api_test(self, error=None, foo=None) -> dict[str, Any]:
        """
        Tests an API endpoint using the "GET" method at the "/api.test" path, accepting optional query parameters "error" and "foo," and returns a response indicating success or default behavior.

        Args:
            error (string): The "error" query parameter is a string used to specify or filter error information related to the request.
            foo (string): The "foo" parameter is a query string input of type string, used in the GET operation at "/api.test" to provide additional filtering or context.

        Returns:
            dict[str, Any]: Standard success response

        Tags:
            api
        """
        url = f"{self.base_url}/api.test"
        query_params = {k: v for k, v in [('error', error), ('foo', foo)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appseventauthorizations_get_list(self, event_context, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a list of authorizations for a specified event context, providing information about which app installations have visibility to the event.

        Args:
            event_context (string): The `event_context` parameter specifies the context or scope in which events are processed or filtered for the authorization list operation.
            cursor (string): A unique identifier or token used for cursor-based pagination, specifying the starting point for retrieving the next set of authorizations in the list.
            limit (integer): Specifies the maximum number of authorization records to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            apps.event.authorizations, apps
        """
        url = f"{self.base_url}/apps.event.authorizations.list"
        query_params = {k: v for k, v in [('event_context', event_context), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissions_list_permissions(self, token=None) -> dict[str, Any]:
        """
        Retrieves information about the current permissions of a Slack app using the "GET" method with the "/apps.permissions.info" path.

        Args:
            token (string): The token parameter in the query is a string used to provide an access token for authentication and authorization when calling the API endpoint.

        Returns:
            dict[str, Any]: Standard success response when used with a user token

        Tags:
            apps.permissions, apps
        """
        url = f"{self.base_url}/apps.permissions.info"
        query_params = {k: v for k, v in [('token', token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissions_additional_scopes_request(self, token, scopes, trigger_id) -> dict[str, Any]:
        """
        Requests app permissions using the Slack API by specifying the required scopes and trigger ID, returning a response after the request is processed.

        Args:
            token (string): Required authentication token sent as a query parameter for verifying access to the API operation.
            scopes (string): Required string parameter specifying the permissions scopes for the app permissions request.
            trigger_id (string): The unique identifier of the API trigger that initiates the permissions request.

        Returns:
            dict[str, Any]: Standard success response when used with a user token

        Tags:
            apps.permissions, apps
        """
        url = f"{self.base_url}/apps.permissions.request"
        query_params = {k: v for k, v in [('token', token), ('scopes', scopes), ('trigger_id', trigger_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissionsresources_get_resources_list(self, token, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of resource grants that the app has on a team, including resource IDs and types.

        Args:
            token (string): A required string parameter containing an authorization token used for authentication and authorization to list application permissions and resources.
            cursor (string): A unique string identifier used for cursor-based pagination, allowing retrieval of the next or previous page of resources by marking the position in the dataset.
            limit (integer): Specifies the maximum number of results to return for each request, allowing control over the amount of data retrieved in the list of application permissions resources.

        Returns:
            dict[str, Any]: Typical successful paginated response

        Tags:
            apps.permissions.resources, apps
        """
        url = f"{self.base_url}/apps.permissions.resources.list"
        query_params = {k: v for k, v in [('token', token), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissionsscopes_get_list(self, token) -> dict[str, Any]:
        """
        Retrieves a list of permission scopes that an app has been granted in a Slack workspace using the provided token.

        Args:
            token (string): Required string parameter for the authentication token to be passed in the query string for accessing the list of app permissions scopes.

        Returns:
            dict[str, Any]: Typical successful paginated response

        Tags:
            apps.permissions.scopes, apps
        """
        url = f"{self.base_url}/apps.permissions.scopes.list"
        query_params = {k: v for k, v in [('token', token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissionsusers_list_user_grants(self, token, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves the list of user grants and their corresponding permission scopes that the app has on a Slack team, supporting pagination via cursor and limit parameters.

        Args:
            token (string): The token parameter in the query is a required string used to authenticate and authorize the request to list user permissions in the app.
            cursor (string): A string parameter used for cursor pagination, indicating the position from which to retrieve the next set of users in the list of app permissions.
            limit (integer): The "limit" parameter, an integer, specifies the maximum number of results to return in a single response for the "GET /apps.permissions.users.list" operation.

        Returns:
            dict[str, Any]: Typical successful paginated response

        Tags:
            apps.permissions.users, apps
        """
        url = f"{self.base_url}/apps.permissions.users.list"
        query_params = {k: v for k, v in [('token', token), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def appspermissionsusers_request_modal(self, token, scopes, trigger_id, user) -> dict[str, Any]:
        """
        Requests specific permissions for a user using the Slack API, requiring a token, scopes, trigger ID, and user ID, and returns a response based on the request's success or failure.

        Args:
            token (string): Required authentication token for requesting user permissions, passed as a query string to verify access.
            scopes (string): Specifies the permissions to request for the user, represented as a string listing one or more scopes.
            trigger_id (string): A unique identifier for the trigger, required for the GET operation at the specified path.
            user (string): The "user" parameter is a required string that must be provided in the query to identify the user requesting app permissions.

        Returns:
            dict[str, Any]: Standard success response when used with a user token

        Tags:
            apps.permissions.users, apps
        """
        url = f"{self.base_url}/apps.permissions.users.request"
        query_params = {k: v for k, v in [('token', token), ('scopes', scopes), ('trigger_id', trigger_id), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def apps_uninstall(self, token=None, client_id=None, client_secret=None) -> dict[str, Any]:
        """
        Uninstalls an application using the provided token, client ID, and client secret, returning a status message.

        Args:
            token (string): An authentication string passed as a query parameter to verify access rights for uninstalling apps, though typically tokens are recommended to be passed via headers for enhanced security.
            client_id (string): A unique identifier for the client application, used to authenticate and authorize API requests for the uninstall operation.
            client_secret (string): A confidential string used to authenticate the application making the GET request to uninstall an app, typically provided in the query parameters.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            apps
        """
        url = f"{self.base_url}/apps.uninstall"
        query_params = {k: v for k, v in [('token', token), ('client_id', client_id), ('client_secret', client_secret)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def auth_revoke(self, token, test=None) -> dict[str, Any]:
        """
        Revokes an authentication token using the GET method at the "/auth.revoke" endpoint, accepting a mandatory token and an optional test parameter, and returns a status response.

        Args:
            token (string): Token to be revoked, passed as a query string for the GET operation at the /auth.revoke path.
            test (boolean): A boolean query parameter named "test" used in the GET operation at "/auth.revoke" to specify a test condition.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            auth
        """
        url = f"{self.base_url}/auth.revoke"
        query_params = {k: v for k, v in [('token', token), ('test', test)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def auth_test(self) -> dict[str, Any]:
        """
        Tests the authentication using a provided token via the GET method at the "/auth.test" path.

        Returns:
            dict[str, Any]: Standard success response when used with a user token

        Tags:
            auth
        """
        url = f"{self.base_url}/auth.test"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def bots_info(self, token, bot=None) -> dict[str, Any]:
        """
        Retrieves extended information about a bot user in Slack, such as its name and icons, using its unique bot ID.

        Args:
            token (string): The token parameter is a required string passed in the query string to authenticate and authorize the request for retrieving bot information.
            bot (string): Specifies the bot identifier as a string to retrieve information about a specific bot via the GET operation.

        Returns:
            dict[str, Any]: When successful, returns bot info by bot ID.

        Tags:
            bots
        """
        url = f"{self.base_url}/bots.info"
        query_params = {k: v for k, v in [('token', token), ('bot', bot)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def calls_add(self, external_unique_id, join_url, title=None, created_by=None, date_start=None, desktop_app_join_url=None, external_display_id=None, users=None) -> dict[str, Any]:
        """
        Registers a new Call in Slack by submitting call details via a POST request with authentication.

        Args:
            external_unique_id (string): An ID supplied by the 3rd-party Call provider. It must be unique across all Calls from that service.
            join_url (string): The URL required for a client to join the Call.
            title (string): The name of the Call.
            created_by (string): The valid Slack user ID of the user who created this Call. When this method is called with a user token, the `created_by` field is optional and defaults to the authed user of the token. Otherwise, the field is required.
            date_start (integer): Call start time in UTC UNIX timestamp format
            desktop_app_join_url (string): When supplied, available Slack clients will attempt to directly launch the 3rd-party Call with this URL.
            external_display_id (string): An optional, human-readable ID supplied by the 3rd-party Call provider. If supplied, this ID will be displayed in the Call object.
            users (string): The list of users to register as participants in the Call. [Read more on how to specify users here](https://slack.dev).

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls
        """
        request_body = {
            'title': title,
            'created_by': created_by,
            'date_start': date_start,
            'desktop_app_join_url': desktop_app_join_url,
            'external_display_id': external_display_id,
            'external_unique_id': external_unique_id,
            'join_url': join_url,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/calls.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def calls_end(self, id, duration=None) -> dict[str, Any]:
        """
        Ends an active Slack call by sending a POST request to the "/calls.end" endpoint, requiring a valid authentication token and the call ID returned from the "calls.add" method.

        Args:
            id (string): `id` returned when registering the call using the [`calls.add`](https://slack.dev) method.
            duration (integer): Call duration in seconds

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls
        """
        request_body = {
            'duration': duration,
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/calls.end"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def calls_info(self, id) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific call by its ID using the provided authentication token.

        Args:
            id (string): Mandatory string identifier used to specify the call for which information is requested.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls
        """
        url = f"{self.base_url}/calls.info"
        query_params = {k: v for k, v in [('id', id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def callsparticipants_add_new_participant(self, id, users) -> dict[str, Any]:
        """
        Adds participants to a call using the Slack API, requiring a Slack authentication token and form data.

        Args:
            id (string): `id` returned by the [`calls.add`](https://slack.dev) method.
            users (string): The list of users to add as participants in the Call. [Read more on how to specify users here](https://slack.dev).

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls.participants, calls
        """
        request_body = {
            'id': id,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/calls.participants.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def callsparticipants_register_removed(self, id, users) -> dict[str, Any]:
        """
        Removes a participant from an active call using a POST request with required authentication.

        Args:
            id (string): `id` returned by the [`calls.add`](https://slack.dev) method.
            users (string): The list of users to remove as participants in the Call. [Read more on how to specify users here](https://slack.dev).

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls.participants, calls
        """
        request_body = {
            'id': id,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/calls.participants.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def calls_update(self, id, title=None, desktop_app_join_url=None, join_url=None) -> dict[str, Any]:
        """
        Updates a call using the provided form data and returns a successful response if the operation is completed.

        Args:
            id (string): `id` returned by the [`calls.add`](https://slack.dev) method.
            title (string): The name of the Call.
            desktop_app_join_url (string): When supplied, available Slack clients will attempt to directly launch the 3rd-party Call with this URL.
            join_url (string): The URL required for a client to join the Call.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            calls
        """
        request_body = {
            'title': title,
            'desktop_app_join_url': desktop_app_join_url,
            'id': id,
            'join_url': join_url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/calls.update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_delete(self, as_user=None, channel=None, ts=None) -> dict[str, Any]:
        """
        Deletes a message from a conversation in Slack using the provided channel and message timestamp, requiring appropriate user or bot authentication.

        Args:
            as_user (boolean): Pass true to delete the message as the authed user with `chat:write:user` scope. [Bot users](https://slack.dev) in this context are considered authed users. If unused or false, the message will be deleted with `chat:write:bot` scope.
            channel (string): Channel containing the message to be deleted.
            ts (number): Timestamp of the message to be deleted.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'channel': channel,
            'ts': ts,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_delete_scheduled_message(self, as_user=None, channel=None, scheduled_message_id=None) -> dict[str, Any]:
        """
        Deletes a pending scheduled Slack message before it is sent using the Slack API, requiring a valid authentication token and either the `chat:write:user` or `chat:write:bot` scope.

        Args:
            as_user (boolean): Pass true to delete the message as the authed user with `chat:write:user` scope. [Bot users](https://slack.dev) in this context are considered authed users. If unused or false, the message will be deleted with `chat:write:bot` scope.
            channel (string): The channel the scheduled_message is posting to
            scheduled_message_id (string): `scheduled_message_id` returned from call to chat.scheduleMessage

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'channel': channel,
            'scheduled_message_id': scheduled_message_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.deleteScheduledMessage"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_get_permalink(self, token, channel, message_ts) -> dict[str, Any]:
        """
        Retrieves a permalink URL for a specific message in a Slack channel using the message's timestamp and channel ID.

        Args:
            token (string): Required authentication token passed as a query parameter to authenticate the request for retrieving a chat permalink.
            channel (string): The channel parameter specifies the unique identifier of the channel containing the message for which the permalink is requested.
            message_ts (string): The "message_ts" parameter is a required string value indicating the timestamp of the message from which to generate a permalink.

        Returns:
            dict[str, Any]: Standard success response

        Tags:
            chat
        """
        url = f"{self.base_url}/chat.getPermalink"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('message_ts', message_ts)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def chat_me_message(self, channel=None, text=None) -> dict[str, Any]:
        """
        Sends a "me" message to a specified Slack channel using the Slack API, allowing users to express themselves in a personalized way.

        Args:
            channel (string): Channel to send message to. Can be a public channel, private group or IM channel. Can be an encoded ID, or a name.
            text (string): Text of the message to send.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'channel': channel,
            'text': text,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.meMessage"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_post_ephemeral(self, as_user=None, attachments=None, blocks=None, channel=None, icon_emoji=None, icon_url=None, link_names=None, parse=None, text=None, thread_ts=None, user=None, username=None) -> dict[str, Any]:
        """
        Posts an ephemeral message visible only to a specified user within a channel or conversation, using authentication and content parameters to deliver context-sensitive, non-persistent notifications.

        Args:
            as_user (boolean): Pass true to post the message as the authed user. Defaults to true if the chat:write:bot scope is not included. Otherwise, defaults to false.
            attachments (string): A JSON-based array of structured attachments, presented as a URL-encoded string.
            blocks (string): A JSON-based array of structured blocks, presented as a URL-encoded string.
            channel (string): Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.
            icon_emoji (string): Emoji to use as the icon for this message. Overrides `icon_url`. Must be used in conjunction with `as_user` set to `false`, otherwise ignored. See [authorship](https://slack.dev) below.
            icon_url (string): URL to an image to use as the icon for this message. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](https://slack.dev) below.
            link_names (boolean): Find and link channel names and usernames.
            parse (string): Change how messages are treated. Defaults to `none`. See [below](https://slack.dev).
            text (string): How this field works and whether it is required depends on other fields you use in your API call. [See below](https://slack.dev) for more detail.
            thread_ts (string): Provide another message's `ts` value to post this message in a thread. Avoid using a reply's `ts` value; use its parent's value instead. Ephemeral messages in threads are only shown if there is already an active thread.
            user (string): `id` of the user who will receive the ephemeral message. The user should be in the channel specified by the `channel` argument.
            username (string): Set your bot's user name. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](https://slack.dev) below.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'attachments': attachments,
            'blocks': blocks,
            'channel': channel,
            'icon_emoji': icon_emoji,
            'icon_url': icon_url,
            'link_names': link_names,
            'parse': parse,
            'text': text,
            'thread_ts': thread_ts,
            'user': user,
            'username': username,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.postEphemeral"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_post_message(self, as_user=None, attachments=None, blocks=None, channel=None, icon_emoji=None, icon_url=None, link_names=None, mrkdwn=None, parse=None, reply_broadcast=None, text=None, thread_ts=None, unfurl_links=None, unfurl_media=None, username=None) -> dict[str, Any]:
        """
        Sends a message to a Slack channel using the `chat.postMessage` method, requiring a valid Slack authentication token and supporting various message formats such as text, attachments, and blocks.

        Args:
            as_user (boolean): Pass true to post the message as the authed user, instead of as a bot. Defaults to false. See [authorship](https://slack.dev) below.
            attachments (string): A JSON-based array of structured attachments, presented as a URL-encoded string.
            blocks (string): A JSON-based array of structured blocks, presented as a URL-encoded string.
            channel (string): Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name. See [below](https://slack.dev) for more details.
            icon_emoji (string): Emoji to use as the icon for this message. Overrides `icon_url`. Must be used in conjunction with `as_user` set to `false`, otherwise ignored. See [authorship](https://slack.dev) below.
            icon_url (string): URL to an image to use as the icon for this message. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](https://slack.dev) below.
            link_names (boolean): Find and link channel names and usernames.
            mrkdwn (boolean): Disable Slack markup parsing by setting to `false`. Enabled by default.
            parse (string): Change how messages are treated. Defaults to `none`. See [below](https://slack.dev).
            reply_broadcast (boolean): Used in conjunction with `thread_ts` and indicates whether reply should be made visible to everyone in the channel or conversation. Defaults to `false`.
            text (string): How this field works and whether it is required depends on other fields you use in your API call. [See below](https://slack.dev) for more detail.
            thread_ts (string): Provide another message's `ts` value to make this message a reply. Avoid using a reply's `ts` value; use its parent instead.
            unfurl_links (boolean): Pass true to enable unfurling of primarily text-based content.
            unfurl_media (boolean): Pass false to disable unfurling of media content.
            username (string): Set your bot's user name. Must be used in conjunction with `as_user` set to false, otherwise ignored. See [authorship](https://slack.dev) below.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'attachments': attachments,
            'blocks': blocks,
            'channel': channel,
            'icon_emoji': icon_emoji,
            'icon_url': icon_url,
            'link_names': link_names,
            'mrkdwn': mrkdwn,
            'parse': parse,
            'reply_broadcast': reply_broadcast,
            'text': text,
            'thread_ts': thread_ts,
            'unfurl_links': unfurl_links,
            'unfurl_media': unfurl_media,
            'username': username,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.postMessage"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_schedule_message(self, as_user=None, attachments=None, blocks=None, channel=None, link_names=None, parse=None, post_at=None, reply_broadcast=None, text=None, thread_ts=None, unfurl_links=None, unfurl_media=None) -> dict[str, Any]:
        """
        Schedules a message to be sent to a public channel, private channel, or direct message conversation in Slack at a specified future time, supporting text, blocks, and attachments.

        Args:
            as_user (boolean): Pass true to post the message as the authed user, instead of as a bot. Defaults to false. See [chat.postMessage](chat.postMessage#authorship).
            attachments (string): A JSON-based array of structured attachments, presented as a URL-encoded string.
            blocks (string): A JSON-based array of structured blocks, presented as a URL-encoded string.
            channel (string): Channel, private group, or DM channel to send message to. Can be an encoded ID, or a name. See [below](https://slack.dev) for more details.
            link_names (boolean): Find and link channel names and usernames.
            parse (string): Change how messages are treated. Defaults to `none`. See [chat.postMessage](chat.postMessage#formatting).
            post_at (string): Unix EPOCH timestamp of time in future to send the message.
            reply_broadcast (boolean): Used in conjunction with `thread_ts` and indicates whether reply should be made visible to everyone in the channel or conversation. Defaults to `false`.
            text (string): How this field works and whether it is required depends on other fields you use in your API call. [See below](https://slack.dev) for more detail.
            thread_ts (number): Provide another message's `ts` value to make this message a reply. Avoid using a reply's `ts` value; use its parent instead.
            unfurl_links (boolean): Pass true to enable unfurling of primarily text-based content.
            unfurl_media (boolean): Pass false to disable unfurling of media content.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'attachments': attachments,
            'blocks': blocks,
            'channel': channel,
            'link_names': link_names,
            'parse': parse,
            'post_at': post_at,
            'reply_broadcast': reply_broadcast,
            'text': text,
            'thread_ts': thread_ts,
            'unfurl_links': unfurl_links,
            'unfurl_media': unfurl_media,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.scheduleMessage"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chatscheduled_messages_list(self, channel=None, latest=None, oldest=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a list of pending scheduled messages from Slack by optionally specifying a channel, time range, and pagination parameters.

        Args:
            channel (string): The **channel** parameter specifies the Slack channel for which to retrieve scheduled messages.
            latest (number): The "latest" parameter filters the list to include only the most recent scheduled messages based on the specified number of messages.
            oldest (number): Filter the list of scheduled messages to include only those with a scheduled time at or after the given Unix timestamp.
            limit (integer): The "limit" parameter, an integer, specifies the maximum number of scheduled messages to return in the response for the "GET /chat.scheduledMessages.list" operation.
            cursor (string): Used for cursor-based pagination, this string parameter specifies a unique identifier to retrieve the next set of scheduled messages in the list.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat.scheduledMessages, chat
        """
        url = f"{self.base_url}/chat.scheduledMessages.list"
        query_params = {k: v for k, v in [('channel', channel), ('latest', latest), ('oldest', oldest), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def chat_unfurl(self, channel, ts, unfurls=None, user_auth_message=None, user_auth_required=None, user_auth_url=None) -> dict[str, Any]:
        """
        Unfurls a link in a Slack message, allowing custom formatting and display of user-posted URLs, using the Slack API's `chat.unfurl` method.

        Args:
            channel (string): Channel ID of the message
            ts (string): Timestamp of the message to add unfurl behavior to.
            unfurls (string): URL-encoded JSON map with keys set to URLs featured in the the message, pointing to their unfurl blocks or message attachments.
            user_auth_message (string): Provide a simply-formatted string to send as an ephemeral message to the user as invitation to authenticate further and enable full unfurling behavior
            user_auth_required (boolean): Set to `true` or `1` to indicate the user must install your Slack app to trigger unfurls for this domain
            user_auth_url (string): Send users to this custom URL where they will complete authentication in your app to fully trigger unfurling. Value should be properly URL-encoded.

        Returns:
            dict[str, Any]: Typical, minimal success response

        Tags:
            chat
        """
        request_body = {
            'channel': channel,
            'ts': ts,
            'unfurls': unfurls,
            'user_auth_message': user_auth_message,
            'user_auth_required': user_auth_required,
            'user_auth_url': user_auth_url,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.unfurl"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def chat_update(self, as_user=None, attachments=None, blocks=None, channel=None, link_names=None, parse=None, text=None, ts=None) -> dict[str, Any]:
        """
        Updates an existing message in a Slack channel using specified text, attachments, or blocks with required authentication.

        Args:
            as_user (string): Pass true to update the message as the authed user. [Bot users](https://slack.dev) in this context are considered authed users.
            attachments (string): A JSON-based array of structured attachments, presented as a URL-encoded string. This field is required when not presenting `text`. If you don't include this field, the message's previous `attachments` will be retained. To remove previous `attachments`, include an empty array for this field.
            blocks (string): A JSON-based array of [structured blocks](https://slack.dev), presented as a URL-encoded string. If you don't include this field, the message's previous `blocks` will be retained. To remove previous `blocks`, include an empty array for this field.
            channel (string): Channel containing the message to be updated.
            link_names (string): Find and link channel names and usernames. Defaults to `none`. If you do not specify a value for this field, the original value set for the message will be overwritten with the default, `none`.
            parse (string): Change how messages are treated. Defaults to `client`, unlike `chat.postMessage`. Accepts either `none` or `full`. If you do not specify a value for this field, the original value set for the message will be overwritten with the default, `client`.
            text (string): New text for the message, using the [default formatting rules](https://slack.dev). It's not required when presenting `blocks` or `attachments`.
            ts (string): Timestamp of the message to be updated.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            chat
        """
        request_body = {
            'as_user': as_user,
            'attachments': attachments,
            'blocks': blocks,
            'channel': channel,
            'link_names': link_names,
            'parse': parse,
            'text': text,
            'ts': ts,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/chat.update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_archive(self, channel=None) -> dict[str, Any]:
        """
        Archives a Slack conversation using the specified authentication token and required scopes for the channel type.

        Args:
            channel (string): ID of conversation to archive

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.archive"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_close(self, channel=None) -> dict[str, Any]:
        """
        Closes a direct message or multi-person direct message in Slack using the Slack API and returns a status message.

        Args:
            channel (string): Conversation to close.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.close"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_create(self, is_private=None, name=None) -> dict[str, Any]:
        """
        Creates a new public or private channel in a Slack workspace using the Conversations API.

        Args:
            is_private (boolean): Create a private channel instead of a public one
            name (string): Name of the public or private channel to create

        Returns:
            dict[str, Any]: If successful, the command returns a rather stark [conversation object](https://slack.dev)

        Tags:
            conversations
        """
        request_body = {
            'is_private': is_private,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_history(self, token=None, channel=None, latest=None, oldest=None, inclusive=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a portion of a Slack conversation's message history using the `conversations.history` method, allowing filtering by time range, inclusion criteria, and pagination controls.

        Args:
            token (string): Authentication token used to access conversation history.
            channel (string): The ID of the channel to retrieve the conversation history from.
            latest (number): Specifies the number of the latest conversation messages to retrieve from the history.
            oldest (number): Timestamp (in seconds) of the oldest message to include in the conversation history results.
            inclusive (boolean): Determines whether to include the messages at the end of the history range in the response.
            limit (integer): Specifies the maximum number of conversation history entries to retrieve in a single API call.
            cursor (string): A string token used for cursor-based pagination to fetch the next set of conversation history results starting from a specific point.

        Returns:
            dict[str, Any]: Typical success response containing a channel's messages

        Tags:
            conversations
        """
        url = f"{self.base_url}/conversations.history"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('latest', latest), ('oldest', oldest), ('inclusive', inclusive), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def conversations_info(self, token=None, channel=None, include_locale=None, include_num_members=None) -> dict[str, Any]:
        """
        Retrieves information about a specific Slack conversation, such as a channel or direct message, using the provided channel ID and optional parameters for locale and member count.

        Args:
            token (string): Token passed as a query parameter to authenticate access to conversation information.
            channel (string): Specifies the name of the channel for which conversation information is requested.
            include_locale (boolean): Include the locale information in the conversation details when set to true.
            include_num_members (boolean): Indicates whether to include the number of members in the conversation information response.

        Returns:
            dict[str, Any]: Typical success response for a public channel. (Also, a response from a private channel and a multi-party IM is very similar to this example.)

        Tags:
            conversations
        """
        url = f"{self.base_url}/conversations.info"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('include_locale', include_locale), ('include_num_members', include_num_members)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def conversations_invite(self, channel=None, users=None) -> dict[str, Any]:
        """
        Invites up to 1000 users to a public or private Slack channel using the Slack API and requires a valid authentication token.

        Args:
            channel (string): The ID of the public or private channel to invite user(s) to.
            users (string): A comma separated list of user IDs. Up to 1000 users may be listed.

        Returns:
            dict[str, Any]: Typical success response when an invitation is extended

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.invite"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_join(self, channel=None) -> dict[str, Any]:
        """
        Joins a user to an existing Slack conversation using the Conversations API and returns a conversation object if successful.

        Args:
            channel (string): ID of conversation to join

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.join"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_kick(self, channel=None, user=None) -> dict[str, Any]:
        """
        Removes a user from a Slack channel using the Slack API.

        Args:
            channel (string): ID of conversation to remove user from.
            user (string): User ID to be removed.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'user': user,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.kick"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_leave(self, channel=None) -> dict[str, Any]:
        """
        Removes the calling user from a Slack conversation using the provided authentication token.

        Args:
            channel (string): Conversation to leave

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.leave"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_list(self, token=None, exclude_archived=None, types=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a list of channel-like conversations in a Slack workspace using the GET method, with options to exclude archived channels, specify conversation types, limit results, and paginate through the list.

        Args:
            token (string): The token parameter in the query string is a string used for authentication to authorize and identify the client making the GET request to the /conversations.list endpoint.
            exclude_archived (boolean): Exclude archived conversations from the list of results.
            types (string): Specifies the types of conversations to include in the list, as a string query parameter.
            limit (integer): Specifies the maximum number of conversations to return in the response, with a default value of 1.
            cursor (string): A cursor string used for pagination to specify the position from which to continue retrieving the next set of conversation results.

        Returns:
            dict[str, Any]: Typical success response with only public channels

        Tags:
            conversations
        """
        url = f"{self.base_url}/conversations.list"
        query_params = {k: v for k, v in [('token', token), ('exclude_archived', exclude_archived), ('types', types), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def conversations_mark(self, channel=None, ts=None) -> dict[str, Any]:
        """
        Moves the read cursor in a specified Slack conversation for the authenticated user, marking a given position as read and broadcasting this update to their active connections.

        Args:
            channel (string): Channel or conversation to set the read cursor for.
            ts (number): Unique identifier of message you want marked as most recently seen in this conversation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'ts': ts,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.mark"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_members(self, token=None, channel=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of member user IDs in a specified Slack conversation using the "conversations.members" method.

        Args:
            token (string): Authentication token used to verify access when retrieving conversation members via the GET operation at "/conversations.members".
            channel (string): The ID of the conversation channel to retrieve the list of members for.
            limit (integer): The "limit" parameter specifies the maximum number of conversation members to return in the response for the GET operation at "/conversations.members".
            cursor (string): A cursor string used for pagination to fetch the next set of conversation members starting after the specified position.

        Returns:
            dict[str, Any]: Typical paginated success response

        Tags:
            conversations
        """
        url = f"{self.base_url}/conversations.members"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def conversations_open(self, channel=None, return_im=None, users=None) -> dict[str, Any]:
        """
        Opens or resumes a direct message or multi-person direct message using the Slack API, allowing subsequent message sending to the conversation.

        Args:
            channel (string): Resume a conversation by supplying an `im` or `mpim`'s ID. Or provide the `users` field instead.
            return_im (boolean): Boolean, indicates you want the full IM channel definition in the response.
            users (string): Comma separated lists of users. If only one user is included, this creates a 1:1 DM.  The ordering of the users is preserved whenever a multi-person direct message is returned. Supply a `channel` when not supplying `users`.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'return_im': return_im,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.open"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_rename(self, channel=None, name=None) -> dict[str, Any]:
        """
        Renames a conversation in Slack, allowing only the original creator, Workspace Admin, or Channel Manager to change its name within specified naming rules.

        Args:
            channel (string): ID of conversation to rename
            name (string): New name for conversation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.rename"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_replies(self, token=None, channel=None, ts=None, latest=None, oldest=None, inclusive=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a cursor-paginated thread of messages posted to a conversation, using the Slack API, and requires a channel identifier and message timestamp to fetch the thread.

        Args:
            token (string): The token parameter in the query is a string used to authenticate and authorize access to retrieve conversation replies.
            channel (string): Specifies the channel for retrieving conversation replies, where the value is a string identifier.
            ts (number): Timestamp parameter indicating when to retrieve conversation replies.
            latest (number): The "latest" query parameter specifies a timestamp or message number to limit the replies returned to those sent before or at this value.
            oldest (number): The "oldest" parameter specifies the oldest conversation reply timestamp to retrieve, filtering results by date.
            inclusive (boolean): A boolean parameter indicating whether the response should include additional related data, allowing for a more comprehensive view of conversation replies.
            limit (integer): Specifies the maximum number of conversation replies to return in the response.
            cursor (string): A string value that uniquely identifies the position in a paginated result set, used to fetch the next or previous page of replies in the conversation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        url = f"{self.base_url}/conversations.replies"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('ts', ts), ('latest', latest), ('oldest', oldest), ('inclusive', inclusive), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def conversations_set_purpose(self, channel=None, purpose=None) -> dict[str, Any]:
        """
        Updates the purpose (description) of a Slack conversation using the "POST" method, requiring a valid token with appropriate scopes.

        Args:
            channel (string): Conversation to set the purpose of
            purpose (string): A new, specialer purpose

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'purpose': purpose,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.setPurpose"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_set_topic(self, channel=None, topic=None) -> dict[str, Any]:
        """
        Sets the topic for a Slack conversation using the Slack API and returns a success message when the operation is completed.

        Args:
            channel (string): Conversation to set the topic of
            topic (string): The new topic string. Does not support formatting or linkification.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
            'topic': topic,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.setTopic"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def conversations_unarchive(self, channel=None) -> dict[str, Any]:
        """
        Reverses the archival of a Slack conversation, adding the calling user to the conversation, using a user token with write permissions.

        Args:
            channel (string): ID of conversation to unarchive

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            conversations
        """
        request_body = {
            'channel': channel,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/conversations.unarchive"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def dialog_open(self, dialog, trigger_id) -> dict[str, Any]:
        """
        The provided details do not match the standard usage of the Slack API's `dialog.open` method, which typically uses a POST request rather than GET. However, if a hypothetical GET operation were defined at this path, it might involve retrieving information about a dialog based on a trigger ID and dialog parameters. For the standard `dialog.open` POST method, it opens a dialog with a user by exchanging a trigger ID received from another interaction. Given the query's context, it seems there might be confusion with the actual method usage. 

        Correcting for the context provided and assuming a hypothetical scenario where a GET method is used (which is not standard for `dialog.open`), the summary could be: Retrieves information about a dialog using a trigger ID and dialog

        Args:
            dialog (string): Mandatory string parameter specifying the dialog to be opened.
            trigger_id (string): Required string parameter identifying the interaction that triggered the dialog, valid for a short period and used to open a focused dialog with a user.

        Returns:
            dict[str, Any]: Typical success response is quite minimal.

        Tags:
            dialog
        """
        url = f"{self.base_url}/dialog.open"
        query_params = {k: v for k, v in [('dialog', dialog), ('trigger_id', trigger_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dnd_end_dnd(self) -> dict[str, Any]:
        """
        Ends the user's currently scheduled Do Not Disturb session immediately using the Slack API.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            dnd
        """
        url = f"{self.base_url}/dnd.endDnd"
        query_params = {}
        response = self._post(url, data={}, params=query_params, content_type='application/json')
        response.raise_for_status()
        return response.json()

    def dnd_end_snooze(self) -> dict[str, Any]:
        """
        Ends the current user's Do Not Disturb snooze mode immediately using the Slack API.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            dnd
        """
        url = f"{self.base_url}/dnd.endSnooze"
        query_params = {}
        response = self._post(url, data={}, params=query_params, content_type='application/json')
        response.raise_for_status()
        return response.json()

    def dnd_info(self, token=None, user=None) -> dict[str, Any]:
        """
        Retrieves a user's current Do Not Disturb status using the Slack API.

        Args:
            token (string): An authentication token passed in the query string to verify access rights for the requested operation.
            user (string): Specifies the username for fetching specific D&D information.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            dnd
        """
        url = f"{self.base_url}/dnd.info"
        query_params = {k: v for k, v in [('token', token), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dnd_set_snooze(self, num_minutes, token) -> dict[str, Any]:
        """
        Activates or adjusts the duration of a user's Do Not Disturb mode on Slack using the "POST" method, requiring a valid authentication token with the "dnd:write" scope.

        Args:
            num_minutes (string): Number of minutes, from now, to snooze until.
            token (string): Authentication token. Requires scope: `dnd:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            dnd
        """
        request_body = {
            'num_minutes': num_minutes,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/dnd.setSnooze"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def dnd_team_info(self, token=None, users=None) -> dict[str, Any]:
        """
        Retrieves information about the current Do Not Disturb settings for a list of users in a Slack team.

        Args:
            token (string): A security token used for authentication, passed as a query string parameter for the D&D team info retrieval operation.
            users (string): Specifies a string of user identifiers to filter team information in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            dnd
        """
        url = f"{self.base_url}/dnd.teamInfo"
        query_params = {k: v for k, v in [('token', token), ('users', users)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def emoji_list(self, token) -> dict[str, Any]:
        """
        Retrieves a list of custom emoji for a Slack team using the `emoji.list` method.

        Args:
            token (string): Authentication token string required in the query to authorize and authenticate the request for the emoji list.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            emoji
        """
        url = f"{self.base_url}/emoji.list"
        query_params = {k: v for k, v in [('token', token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def filescomments_delete_comment(self, file=None, id=None) -> dict[str, Any]:
        """
        Deletes an existing comment on a file using the Slack API, accessible only to the comment's original author or a Team Administrator.

        Args:
            file (string): File to delete a comment from.
            id (string): The comment to delete.

        Returns:
            dict[str, Any]: Standard success response is very simple

        Tags:
            files.comments, files
        """
        request_body = {
            'file': file,
            'id': id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.comments.delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def files_delete(self, file=None) -> dict[str, Any]:
        """
        Deletes a specified file from the Slack workspace using a POST request with authentication.

        Args:
            file (string): ID of file to delete.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files
        """
        request_body = {
            'file': file,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def files_info(self, token=None, file=None, count=None, page=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific file in a Slack workspace, including the file object, comments, and pagination data.

        Args:
            token (string): Required string token used for authentication and authorization when retrieving file information via the GET operation.
            file (string): The file ID to retrieve detailed information about a specific file.
            count (string): The "count" query parameter specifies the number of items or results to return in the response.
            page (string): The "page" parameter specifies the page number for pagination purposes in the response, passed as a query string in GET requests to "/files.info".
            limit (integer): Specifies the maximum number of file information records to return in the response, as an integer value.
            cursor (string): A unique identifier used for pagination, indicating the position from which to retrieve the next set of results.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files
        """
        url = f"{self.base_url}/files.info"
        query_params = {k: v for k, v in [('token', token), ('file', file), ('count', count), ('page', page), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def files_list(self, token=None, user=None, channel=None, ts_from=None, ts_to=None, types=None, count=None, page=None, show_files_hidden_by_limit=None) -> dict[str, Any]:
        """
        Retrieves a list of files within a Slack team, allowing filtering by user, channel, file type, and time range, with optional parameters to include hidden files in Free workspaces.

        Args:
            token (string): Optional token parameter for authentication, used in rare cases where headers are not feasible, typically requiring additional security measures to prevent exposure.
            user (string): Specifies the user for which to list files, provided as a string value in the query parameter.
            channel (string): Specifies a string value representing the channel for filtering files in the list operation.
            ts_from (number): The "ts_from" parameter is a query parameter of type number used in the GET operation at "/files.list" to specify the starting timestamp for filtering results.
            ts_to (number): The "ts_to" query parameter specifies the upper bound of the timestamp range to filter files by their creation or modification time.
            types (string): Specifies the type of files to include in the response, allowing for filtering by specific file types.
            count (string): The "count" query parameter specifies the number of files to return in the list response.
            page (string): The "page" query parameter specifies the pagination cursor or token to retrieve a specific page of results in the files list.
            show_files_hidden_by_limit (boolean): When set to true, includes files that are normally hidden due to result limits in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files
        """
        url = f"{self.base_url}/files.list"
        query_params = {k: v for k, v in [('token', token), ('user', user), ('channel', channel), ('ts_from', ts_from), ('ts_to', ts_to), ('types', types), ('count', count), ('page', page), ('show_files_hidden_by_limit', show_files_hidden_by_limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def filesremote_add_from_remote(self, title=None, external_id=None, external_url=None, filetype=None, indexable_file_contents=None, preview_image=None, token=None) -> dict[str, Any]:
        """
        Adds a remote file to Slack, making Slack aware of the file without sharing it to a channel.

        Args:
            title (string): Title of the file being shared.
            external_id (string): Creator defined GUID for the file.
            external_url (string): URL of the remote file.
            filetype (string): type of file
            indexable_file_contents (string): A text file (txt, pdf, doc, etc.) containing textual search terms that are used to improve discovery of the remote file.
            preview_image (string): Preview of the document via `multipart/form-data`.
            token (string): Authentication token. Requires scope: `remote_files:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        request_body = {
            'title': title,
            'external_id': external_id,
            'external_url': external_url,
            'filetype': filetype,
            'indexable_file_contents': indexable_file_contents,
            'preview_image': preview_image,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.remote.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def filesremote_get_info(self, token=None, file=None, external_id=None) -> dict[str, Any]:
        """
        Retrieves remote file information using the Slack API when provided with a token, file path, and external ID, returning details about the specified file.

        Args:
            token (string): Authentication token used to verify access rights for retrieving remote file information.
            file (string): Specifies the file name or identifier for remote file information retrieval.
            external_id (string): An optional string parameter used to identify external resources or users uniquely across different systems or services, enabling consistent tracking and correlation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        url = f"{self.base_url}/files.remote.info"
        query_params = {k: v for k, v in [('token', token), ('file', file), ('external_id', external_id)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def filesremote_list_remote_files(self, token=None, channel=None, ts_from=None, ts_to=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of remote files visible in Slack, optionally filtered by channel and time range.

        Args:
            token (string): Token for authentication to access the list of remote files, typically should be passed via headers for security, but here it is accepted as a query parameter.
            channel (string): Specifies the channel to filter results from in the remote file listing operation.
            ts_from (number): The "ts_from" parameter filters the list of files based on the timestamp from which to retrieve files, specified as a number.
            ts_to (number): The "ts_to" parameter filters the list of files by specifying the end timestamp, limiting results to files created or modified up to this time.
            limit (integer): The `limit` parameter specifies the maximum number of file items to return in the response for the `/files.remote.list` operation.
            cursor (string): A string parameter used for cursor-based pagination, typically containing a unique identifier or token that specifies the starting point for retrieving the next set of results.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        url = f"{self.base_url}/files.remote.list"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('ts_from', ts_from), ('ts_to', ts_to), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def filesremote_delete_file(self, external_id=None, file=None, token=None) -> dict[str, Any]:
        """
        Removes a remote file using a POST request, authorized with Slack authentication and returning a response upon successful deletion.

        Args:
            external_id (string): Creator defined GUID for the file.
            file (string): Specify a file by providing its ID.
            token (string): Authentication token. Requires scope: `remote_files:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        request_body = {
            'external_id': external_id,
            'file': file,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.remote.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def filesremote_share_remote_file(self, token=None, file=None, external_id=None, channels=None) -> dict[str, Any]:
        """
        Shares a remote file in a Slack conversation using the specified channels and file details, returning a status message indicating the success of the operation.

        Args:
            token (string): Authentication token used to authorize access to the remote file sharing operation.
            file (string): The "file" query parameter specifies the identifier or path of the remote file to be shared.
            external_id (string): Optional external identifier for the file or user, used to reference specific entities or track interactions.
            channels (string): A comma-separated string specifying the channels to share the remote file with.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        url = f"{self.base_url}/files.remote.share"
        query_params = {k: v for k, v in [('token', token), ('file', file), ('external_id', external_id), ('channels', channels)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def filesremote_update_remote_file(self, title=None, external_id=None, external_url=None, file=None, filetype=None, indexable_file_contents=None, preview_image=None, token=None) -> dict[str, Any]:
        """
        Updates a remote file in Slack using the `POST` method, allowing changes to fields like title, but not `external_id` or `file_id`, and requires the `remote_files:write` scope for authentication.

        Args:
            title (string): Title of the file being shared.
            external_id (string): Creator defined GUID for the file.
            external_url (string): URL of the remote file.
            file (string): Specify a file by providing its ID.
            filetype (string): type of file
            indexable_file_contents (string): File containing contents that can be used to improve searchability for the remote file.
            preview_image (string): Preview of the document via `multipart/form-data`.
            token (string): Authentication token. Requires scope: `remote_files:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files.remote, files
        """
        request_body = {
            'title': title,
            'external_id': external_id,
            'external_url': external_url,
            'file': file,
            'filetype': filetype,
            'indexable_file_contents': indexable_file_contents,
            'preview_image': preview_image,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.remote.update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def files_revoke_public_url(self, file=None) -> dict[str, Any]:
        """
        Revoke the public URL of a file using the POST method, requiring a Slack authentication token with "files:write:user" scope in the header.

        Args:
            file (string): File to revoke

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files
        """
        request_body = {
            'file': file,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.revokePublicURL"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def files_shared_public_url(self, file=None) -> dict[str, Any]:
        """
        Enables public or external sharing for a Slack file using the Slack API and returns a file object with a public permalink.

        Args:
            file (string): File to share

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            files
        """
        request_body = {
            'file': file,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.sharedPublicURL"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def files_upload(self, title=None, channels=None, content=None, file=None, filename=None, filetype=None, initial_comment=None, thread_ts=None, token=None) -> dict[str, Any]:
        """
        Uploads or creates a file to Slack, allowing the file to be shared in specified channels using the POST method with application/x-www-form-urlencoded content.

        Args:
            title (string): Title of file.
            channels (string): Comma-separated list of channel names or IDs where the file will be shared.
            content (string): File contents via a POST variable. If omitting this parameter, you must provide a `file`.
            file (string): File contents via `multipart/form-data`. If omitting this parameter, you must submit `content`.
            filename (string): Filename of file.
            filetype (string): A [file type](https://slack.dev) identifier.
            initial_comment (string): The message text introducing the file in specified `channels`.
            thread_ts (number): Provide another message's `ts` value to upload this file as a reply. Never use a reply's `ts` value; use its parent instead.
            token (string): Authentication token. Requires scope: `files:write:user`

        Returns:
            dict[str, Any]: Success response after uploading a file to a channel with an initial message

        Tags:
            files
        """
        request_body = {
            'title': title,
            'channels': channels,
            'content': content,
            'file': file,
            'filename': filename,
            'filetype': filetype,
            'initial_comment': initial_comment,
            'thread_ts': thread_ts,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/files.upload"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def migration_exchange(self, token, users, team_id=None, to_old=None) -> dict[str, Any]:
        """
        Converts vintage user IDs to Enterprise Grid-compatible global user IDs within a Slack workspace.

        Args:
            token (string): A mandatory string parameter representing a security token required for authentication in the GET operation at the "/migration.exchange" path.
            users (string): Comma-separated list of user identifiers to specify which users are included in the migration exchange request.
            team_id (string): The `team_id` parameter is a string query parameter used in the GET operation at the `/migration.exchange` path to specify the team identifier for the migration exchange operation.
            to_old (boolean): If true, the migration will convert data to an older exchange format.

        Returns:
            dict[str, Any]: Typical success response when mappings exist for the specified user IDs

        Tags:
            migration
        """
        url = f"{self.base_url}/migration.exchange"
        query_params = {k: v for k, v in [('token', token), ('users', users), ('team_id', team_id), ('to_old', to_old)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def oauth_access(self, client_id=None, client_secret=None, code=None, redirect_uri=None, single_channel=None) -> dict[str, Any]:
        """
        Exchanges an OAuth authorization code and client credentials for an access token to authenticate API requests on behalf of a user.

        Args:
            client_id (string): A public identifier for the client application, required for authentication and authorization in OAuth 2.0 flows.
            client_secret (string): The `client_secret` is a confidential string used for client authentication, typically required for confidential clients, and is used in conjunction with the `client_id` to verify the client's identity.
            code (string): The "code" parameter is a string representing the authorization code obtained from the authorization server, typically used in OAuth 2.0 flows to exchange for an access token.
            redirect_uri (string): The redirect_uri query parameter specifies the URI to which the authorization server will redirect the user-agent after authorization, and it must exactly match one of the redirect URIs registered by the client application.
            single_channel (boolean): Whether to restrict the OAuth access token to a single channel context by returning a token usable only for one channel.

        Returns:
            dict[str, Any]: Successful user token negotiation for a single scope

        Tags:
            oauth
        """
        url = f"{self.base_url}/oauth.access"
        query_params = {k: v for k, v in [('client_id', client_id), ('client_secret', client_secret), ('code', code), ('redirect_uri', redirect_uri), ('single_channel', single_channel)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def oauth_token(self, client_id=None, client_secret=None, code=None, redirect_uri=None, single_channel=None) -> dict[str, Any]:
        """
        Retrieves an OAuth token using a client ID, client secret, authorization code, and redirect URI via the "/oauth.token" endpoint, supporting optional single-channel specification.

        Args:
            client_id (string): Unique identifier of the client application, used to authenticate the client when requesting an access token.
            client_secret (string): The client_secret parameter is a mandatory string value used by confidential clients to authenticate themselves with the authorization server during token requests.
            code (string): The authorization code previously received from the authorization server, used to exchange for an access token.
            redirect_uri (string): The redirect_uri query parameter specifies the exact URI to which the authorization server will send the user-agent back after authorization, and it must match a pre-registered redirect URI for the client to ensure security and proper routing of the authorization response.
            single_channel (boolean): Indicates whether to retrieve a single channel token; set to true for a single channel, false otherwise.

        Returns:
            dict[str, Any]: Success example using a workspace app produces a very different kind of response

        Tags:
            oauth
        """
        url = f"{self.base_url}/oauth.token"
        query_params = {k: v for k, v in [('client_id', client_id), ('client_secret', client_secret), ('code', code), ('redirect_uri', redirect_uri), ('single_channel', single_channel)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def oauthv2_exchange_token(self, code, client_id=None, client_secret=None, redirect_uri=None) -> dict[str, Any]:
        """
        Exchanges an authorization code for an access token by validating the client credentials and code in the OAuth 2.0 authorization code flow.

        Args:
            code (string): The authorization code received from the authorization server, used to exchange for an access token.
            client_id (string): The `client_id` is a required string parameter that identifies the client application making the GET request to the `/oauth.v2.access` endpoint, serving as a public identifier for authentication purposes.
            client_secret (string): A secret known only to the application and the authorization server, used for client authentication in OAuth flows.
            redirect_uri (string): The redirect_uri parameter specifies the callback URL to which the authorization server will send the user-agent back after authorization, and it must match a registered redirect URI for the client.

        Returns:
            dict[str, Any]: Successful token request with scopes for both a bot user and a user token

        Tags:
            oauth.v2, oauth
        """
        url = f"{self.base_url}/oauth.v2.access"
        query_params = {k: v for k, v in [('client_id', client_id), ('client_secret', client_secret), ('code', code), ('redirect_uri', redirect_uri)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def pins_add(self, channel, timestamp=None) -> dict[str, Any]:
        """
        Pins a message to a specified Slack channel using the message's timestamp and channel ID, requiring authentication with a token having the "pins:write" scope.

        Args:
            channel (string): Channel to pin the item in.
            timestamp (string): Timestamp of the message to pin.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            pins
        """
        request_body = {
            'channel': channel,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/pins.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def pins_list(self, token, channel) -> Any:
        """
        Lists the items pinned to a specified Slack channel using the provided token, returning a list of pinned items such as messages, files, and file comments.

        Args:
            token (string): A required string parameter representing an authentication token, passed via query string for authentication purposes in the GET operation.
            channel (string): The channel query parameter specifies the ID of the channel from which to list pinned items.

        Returns:
            Any: Typical success response

        Tags:
            pins
        """
        url = f"{self.base_url}/pins.list"
        query_params = {k: v for k, v in [('token', token), ('channel', channel)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def pins_remove(self, channel, timestamp=None) -> dict[str, Any]:
        """
        Un-pins an item such as a file, file comment, or message from a specified Slack channel using a POST request.

        Args:
            channel (string): Channel where the item is pinned to.
            timestamp (string): Timestamp of the message to un-pin.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            pins
        """
        request_body = {
            'channel': channel,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/pins.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reactions_add(self, channel, name, timestamp) -> dict[str, Any]:
        """
        Adds a reaction to a Slack message using the Slack API and requires authentication.

        Args:
            channel (string): Channel where the message to add reaction to was posted.
            name (string): Reaction (emoji) name.
            timestamp (string): Timestamp of the message to add reaction to.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reactions
        """
        request_body = {
            'channel': channel,
            'name': name,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/reactions.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reactions_get(self, token, channel=None, file=None, file_comment=None, full=None, timestamp=None) -> dict[str, Any]:
        """
        Retrieves a list of reactions for a specified channel, file, or file comment using the Slack API, requiring a valid token and optionally filtering by timestamp or including full reaction details.

        Args:
            token (string): The "token" parameter is a required string that must be provided in the query string for authentication purposes when using the GET operation at "/reactions.get" to authorize access to reaction data.
            channel (string): The channel identifier to filter reactions by, specified as a string.
            file (string): The file parameter specifies the identifier of the file for which to retrieve reactions.
            file_comment (string): A query parameter to filter reactions by a specific file comment.
            full (boolean): Whether to return full reaction details or only basic reaction information.
            timestamp (string): The timestamp parameter filters results based on a specific date and time value, expected in an ISO 8601 format string.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reactions
        """
        url = f"{self.base_url}/reactions.get"
        query_params = {k: v for k, v in [('token', token), ('channel', channel), ('file', file), ('file_comment', file_comment), ('full', full), ('timestamp', timestamp)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def reactions_list(self, token, user=None, full=None, count=None, page=None, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a list of reactions with optional filtering by user and pagination controls, requiring a Slack authentication token with read permissions for reactions.

        Args:
            token (string): Required authentication token passed as a query parameter to authenticate the request for listing reactions.
            user (string): Filter reactions by specifying the user, which can be a username or identifier.
            full (boolean): Indicates whether to retrieve a full list of reactions, with `true` returning all reactions and `false` returning a partial list.
            count (integer): The "count" query parameter specifies the maximum number of reaction items to return in the response.
            page (integer): The "page" parameter is an integer query parameter used to specify the page number for pagination in the list of reactions.
            cursor (string): A string used to specify the position in the list of reactions for pagination, allowing retrieval of additional items after or before the specified cursor.
            limit (integer): The `limit` parameter specifies the maximum number of reactions to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reactions
        """
        url = f"{self.base_url}/reactions.list"
        query_params = {k: v for k, v in [('token', token), ('user', user), ('full', full), ('count', count), ('page', page), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def reactions_remove(self, name, channel=None, file=None, file_comment=None, timestamp=None) -> dict[str, Any]:
        """
        Removes a reaction using the Slack API and requires a token for authentication with the necessary "reactions:write" scope.

        Args:
            name (string): Reaction (emoji) name.
            channel (string): Channel where the message to remove reaction from was posted.
            file (string): File to remove reaction from.
            file_comment (string): File comment to remove reaction from.
            timestamp (string): Timestamp of the message to remove reaction from.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reactions
        """
        request_body = {
            'channel': channel,
            'file': file,
            'file_comment': file_comment,
            'name': name,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/reactions.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reminders_add(self, text, time, user=None) -> dict[str, Any]:
        """
        Creates a reminder in Slack using the provided parameters and authentication token.

        Args:
            text (string): The content of the reminder
            time (string): When this reminder should happen: the Unix timestamp (up to five years from now), the number of seconds until the reminder (if within 24 hours), or a natural language description (Ex. "in 15 minutes," or "every Thursday")
            user (string): The user who will receive the reminder. If no user is specified, the reminder will go to user who created it.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reminders
        """
        request_body = {
            'text': text,
            'time': time,
            'user': user,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/reminders.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reminders_complete(self, reminder=None) -> dict[str, Any]:
        """
        Marks a Slack reminder as complete using the Slack API and returns a status message.

        Args:
            reminder (string): The ID of the reminder to be marked as complete

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reminders
        """
        request_body = {
            'reminder': reminder,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/reminders.complete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reminders_delete(self, reminder=None) -> dict[str, Any]:
        """
        Deletes a reminder in Slack using the provided token and returns a success or error response.

        Args:
            reminder (string): The ID of the reminder

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reminders
        """
        request_body = {
            'reminder': reminder,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/reminders.delete"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def reminders_info(self, token=None, reminder=None) -> dict[str, Any]:
        """
        Retrieves information about a reminder using the provided token and reminder identifier, requiring Slack authentication for reminders read access.

        Args:
            token (string): A string token required for authentication to access reminder information, ideally passed securely via headers rather than query parameters to prevent exposure.
            reminder (string): The "reminder" query parameter is a string value used to specify additional information or filter reminders when retrieving reminders information via the GET operation at "/reminders.info".

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reminders
        """
        url = f"{self.base_url}/reminders.info"
        query_params = {k: v for k, v in [('token', token), ('reminder', reminder)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def reminders_list(self, token=None) -> dict[str, Any]:
        """
        Lists all reminders created by or for a given user using the Slack API.

        Args:
            token (string): A string representing the authentication token for accessing the reminders list.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            reminders
        """
        url = f"{self.base_url}/reminders.list"
        query_params = {k: v for k, v in [('token', token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def rtm_connect(self, token, batch_presence_aware=None, presence_sub=None) -> dict[str, Any]:
        """
        Establishes a Real Time Messaging API session with Slack using the provided token, optionally enabling batch presence awareness and presence subscriptions, and returns a WebSocket Message Server URL for real-time event streaming.

        Args:
            token (string): Required authentication token passed as a query parameter, used to verify access rights for the GET operation at the "/rtm.connect" path.
            batch_presence_aware (boolean): Enables batched presence updates, allowing multiple user presence changes to be sent in a single event, improving efficiency when many users change their presence simultaneously.
            presence_sub (boolean): When set to true, enables subscription to user presence change events, allowing the app to receive presence updates only for subscribed users during the websocket session.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            rtm
        """
        url = f"{self.base_url}/rtm.connect"
        query_params = {k: v for k, v in [('token', token), ('batch_presence_aware', batch_presence_aware), ('presence_sub', presence_sub)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_messages(self, token, query, count=None, highlight=None, page=None, sort=None, sort_dir=None) -> dict[str, Any]:
        """
        Searches for messages in a Slack workspace based on a query and returns matching results, allowing for customization with parameters like sorting and highlighting.

        Args:
            token (string): A required string parameter named "token" passed as a query parameter to authenticate the request for retrieving search messages.
            query (string): The search query string to specify the text or keywords to search for in messages.
            count (integer): Optional integer parameter "count" specifying the number of search messages to return, defaulting to 1 if not provided.
            highlight (boolean): Indicates whether to highlight specific parts of the search results in the messages.
            page (integer): The page query parameter specifies the page number of search results to retrieve in the GET /search.messages operation.
            sort (string): Sorts the search results by a specified field, allowing clients to customize the order of returned messages.
            sort_dir (string): The "sort_dir" query parameter specifies the direction of sorting for the search results, typically accepting values like "asc" for ascending or "desc" for descending order.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            search
        """
        url = f"{self.base_url}/search.messages"
        query_params = {k: v for k, v in [('token', token), ('count', count), ('highlight', highlight), ('page', page), ('query', query), ('sort', sort), ('sort_dir', sort_dir)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def stars_add(self, channel=None, file=None, file_comment=None, timestamp=None) -> dict[str, Any]:
        """
        Adds a star to a GitHub repository using the GitHub API, requiring an authentication token for authorization.

        Args:
            channel (string): Channel to add star to, or channel where the message to add star to was posted (used with `timestamp`).
            file (string): File to add star to.
            file_comment (string): File comment to add star to.
            timestamp (string): Timestamp of the message to add star to.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            stars
        """
        request_body = {
            'channel': channel,
            'file': file,
            'file_comment': file_comment,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/stars.add"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def stars_list(self, token=None, count=None, page=None, cursor=None, limit=None) -> dict[str, Any]:
        """
        Retrieves a list of starred items using the provided parameters for pagination and filtering, requiring a valid authentication token.

        Args:
            token (string): An authentication token passed as a query parameter to authorize access for the GET operation at the "/stars.list" path.
            count (string): The "count" query parameter specifies the number of star items to return in the response.
            page (string): The `page` parameter is a query string parameter used to specify the page number for pagination in the GET request to the `/stars.list` endpoint.
            cursor (string): A string token used for cursor-based pagination to fetch the next set of results after the specified position in the list.
            limit (integer): Specifies the maximum number of items to return in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            stars
        """
        url = f"{self.base_url}/stars.list"
        query_params = {k: v for k, v in [('token', token), ('count', count), ('page', page), ('cursor', cursor), ('limit', limit)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def stars_remove(self, channel=None, file=None, file_comment=None, timestamp=None) -> dict[str, Any]:
        """
        Removes a star from an item on behalf of the authenticated user using a POST request with required authentication token.

        Args:
            channel (string): Channel to remove star from, or channel where the message to remove star from was posted (used with `timestamp`).
            file (string): File to remove star from.
            file_comment (string): File comment to remove star from.
            timestamp (string): Timestamp of the message to remove star from.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            stars
        """
        request_body = {
            'channel': channel,
            'file': file,
            'file_comment': file_comment,
            'timestamp': timestamp,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/stars.remove"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def team_access_logs(self, token, before=None, count=None, page=None) -> dict[str, Any]:
        """
        Retrieves access logs for users on a Slack workspace, including details such as user ID, username, IP address, and user agent, and supports pagination and filtering by time range.

        Args:
            token (string): Required authentication token to access team access logs, typically passed in the query string for this operation.
            before (string): Filter access logs by timestamps before a specified date or time.
            count (string): Specifies the number of access logs to return in the response, as a string value.
            page (string): The page parameter is a query string parameter used to specify the page number for accessing team access logs.

        Returns:
            dict[str, Any]: This response demonstrates pagination and two access log entries.

        Tags:
            team
        """
        url = f"{self.base_url}/team.accessLogs"
        query_params = {k: v for k, v in [('token', token), ('before', before), ('count', count), ('page', page)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def team_billable_info(self, token, user=None) -> dict[str, Any]:
        """
        Retrieves billable information for a team member, requiring an admin-level token and optionally specifying a user.

        Args:
            token (string): A required string parameter containing the authentication token, passed in the query string for the GET operation at path "/team.billableInfo".
            user (string): A string parameter specifying the user for whom to retrieve billable information.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            team
        """
        url = f"{self.base_url}/team.billableInfo"
        query_params = {k: v for k, v in [('token', token), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def team_info(self, token, team=None) -> dict[str, Any]:
        """
        Retrieves information about the current Slack team using the provided authentication token.

        Args:
            token (string): Mandatory authentication token passed as a query parameter to authenticate the request for retrieving team information.
            team (string): The "team" parameter is a query string parameter of type string, used to specify the team for which information is requested in the GET operation at the "/team.info" path.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            team
        """
        url = f"{self.base_url}/team.info"
        query_params = {k: v for k, v in [('token', token), ('team', team)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def team_integration_logs(self, token, app_id=None, change_type=None, count=None, page=None, service_id=None, user=None) -> dict[str, Any]:
        """
        Retrieves a paginated list of team integration logs filtered by parameters such as app ID, change type, service ID, and user, requiring admin-level Slack authentication.

        Args:
            token (string): Required authentication token passed as a query parameter for accessing team integration logs.
            app_id (string): Unique identifier for the application requesting access to team integration logs.
            change_type (string): Filter integration logs by the type of change, such as updates or deletions, to retrieve specific log entries.
            count (string): Specifies the number of integration logs to return in the response.
            page (string): The "page" parameter, located in the query string, specifies which page of integration logs to retrieve for the GET operation at "/team.integrationLogs".
            service_id (string): The unique identifier of the service to filter integration logs by.
            user (string): A string parameter specifying the user for whom integration logs are to be retrieved.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            team
        """
        url = f"{self.base_url}/team.integrationLogs"
        query_params = {k: v for k, v in [('token', token), ('app_id', app_id), ('change_type', change_type), ('count', count), ('page', page), ('service_id', service_id), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def teamprofile_get_profile(self, token, visibility=None) -> dict[str, Any]:
        """
        Retrieves the profile field definitions for a Slack team using the GET method, allowing for optional filtering by visibility.

        Args:
            token (string): Authentication token string required to authorize and identify the caller making the request.
            visibility (string): Determines the visibility level of the team profile, as specified by a string value, when retrieving the team profile via the GET operation.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            team.profile, team
        """
        url = f"{self.base_url}/team.profile.get"
        query_params = {k: v for k, v in [('token', token), ('visibility', visibility)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def usergroups_create(self, description=None, channels=None, handle=None, include_count=None, name=None) -> dict[str, Any]:
        """
        Creates a new User Group in Slack using the specified parameters and returns a usergroup object upon success, requiring the `usergroups:write` permission.

        Args:
            description (string): A short description of the User Group.
            channels (string): A comma separated string of encoded channel IDs for which the User Group uses as a default.
            handle (string): A mention handle. Must be unique among channels, users and User Groups.
            include_count (boolean): Include the number of users in each User Group.
            name (string): A name for the User Group. Must be unique among User Groups.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups
        """
        request_body = {
            'description': description,
            'channels': channels,
            'handle': handle,
            'include_count': include_count,
            'name': name,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/usergroups.create"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def usergroups_disable(self, include_count=None, usergroup=None) -> dict[str, Any]:
        """
        Disables an existing Slack User Group using the Slack API and returns a success status message.

        Args:
            include_count (boolean): Include the number of users in the User Group.
            usergroup (string): The encoded ID of the User Group to disable.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups
        """
        request_body = {
            'include_count': include_count,
            'usergroup': usergroup,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/usergroups.disable"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def usergroups_enable(self, include_count=None, usergroup=None) -> dict[str, Any]:
        """
        Enables a previously disabled Slack User Group using the Slack API and returns a status message.

        Args:
            include_count (boolean): Include the number of users in the User Group.
            usergroup (string): The encoded ID of the User Group to enable.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups
        """
        request_body = {
            'include_count': include_count,
            'usergroup': usergroup,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/usergroups.enable"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def usergroups_list(self, token, include_users=None, include_count=None, include_disabled=None) -> dict[str, Any]:
        """
        Retrieves a list of all User Groups in the team, with options to include disabled groups, user counts, and users in each group.

        Args:
            token (string): The "token" parameter is a required string passed in the query string to authenticate API requests for listing user groups.
            include_users (boolean): Indicates whether to include user details in the response.
            include_count (boolean): Indicates whether to include the count of user groups in the response.
            include_disabled (boolean): Indicates whether to include disabled user groups in the response; defaults to excluding them if not specified.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups
        """
        url = f"{self.base_url}/usergroups.list"
        query_params = {k: v for k, v in [('include_users', include_users), ('token', token), ('include_count', include_count), ('include_disabled', include_disabled)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def usergroups_update(self, description=None, channels=None, handle=None, include_count=None, name=None, usergroup=None) -> dict[str, Any]:
        """
        Updates the properties of an existing Slack User Group, requiring a valid token and the `usergroups:write` permission to modify group details.

        Args:
            description (string): A short description of the User Group.
            channels (string): A comma separated string of encoded channel IDs for which the User Group uses as a default.
            handle (string): A mention handle. Must be unique among channels, users and User Groups.
            include_count (boolean): Include the number of users in the User Group.
            name (string): A name for the User Group. Must be unique among User Groups.
            usergroup (string): The encoded ID of the User Group to update.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups
        """
        request_body = {
            'description': description,
            'channels': channels,
            'handle': handle,
            'include_count': include_count,
            'name': name,
            'usergroup': usergroup,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/usergroups.update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def usergroupsusers_list_all_users(self, token, usergroup, include_disabled=None) -> dict[str, Any]:
        """
        Lists users belonging to a specified user group using the Slack API, allowing optional inclusion of disabled users.

        Args:
            token (string): Required authentication token passed via query string to authenticate and authorize access to the operation.
            usergroup (string): **usergroup**: A required string parameter specifying the user group to list users for.
            include_disabled (boolean): Include disabled users in the list of users for the specified user group.

        Returns:
            dict[str, Any]: Standard success response when used with a user token

        Tags:
            usergroups.users, usergroups
        """
        url = f"{self.base_url}/usergroups.users.list"
        query_params = {k: v for k, v in [('token', token), ('include_disabled', include_disabled), ('usergroup', usergroup)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def usergroupsusers_update_list(self, include_count=None, usergroup=None, users=None) -> dict[str, Any]:
        """
        Updates and replaces the entire list of users belonging to a specified Slack user group.

        Args:
            include_count (boolean): Include the number of users in the User Group.
            usergroup (string): The encoded ID of the User Group to update.
            users (string): A comma separated string of encoded user IDs that represent the entire list of users for the User Group.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            usergroups.users, usergroups
        """
        request_body = {
            'include_count': include_count,
            'usergroup': usergroup,
            'users': users,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/usergroups.users.update"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def users_conversations(self, token=None, user=None, types=None, exclude_archived=None, limit=None, cursor=None) -> dict[str, Any]:
        """
        Retrieves a list of all channel-like conversations accessible to a user or app using the Slack API, including public channels, private channels, direct messages, and multi-person direct messages, based on the provided authentication token and optional filters.

        Args:
            token (string): The token query parameter is a string used to provide an access token for authentication and authorization when retrieving user conversations.
            user (string): The ID of the user whose conversations are to be retrieved.
            types (string): A string parameter used to specify the types of conversations to retrieve for users.
            exclude_archived (boolean): Determines whether to exclude archived conversations from the results, set to true to exclude them.
            limit (integer): The "limit" parameter specifies the maximum number of conversation records to return in response to the GET operation at "/users.conversations".
            cursor (string): A unique identifier used for cursor pagination, allowing the retrieval of the next or previous page of user conversations by specifying the starting point in the dataset.

        Returns:
            dict[str, Any]: Typical success response with only public channels. Note how `num_members` and `is_member` are not returned like typical `conversations` objects.

        Tags:
            users
        """
        url = f"{self.base_url}/users.conversations"
        query_params = {k: v for k, v in [('token', token), ('user', user), ('types', types), ('exclude_archived', exclude_archived), ('limit', limit), ('cursor', cursor)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_delete_photo(self, token) -> dict[str, Any]:
        """
        Deletes a user's photo using the Slack API and returns a status message, requiring the "users.profile:write" permission.

        Args:
            token (string): Authentication token. Requires scope: `users.profile:write`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        request_body = {
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/users.deletePhoto"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def users_get_presence(self, token, user=None) -> dict[str, Any]:
        """
        Retrieves a user's current presence information using the Slack API, indicating whether they are active or away and if they have an active connection.

        Args:
            token (string): Required authentication token passed as a query parameter to authenticate the request for retrieving user presence.
            user (string): The "user" query parameter, of type string, specifies the user for whom the presence status should be retrieved.

        Returns:
            dict[str, Any]: When requesting information for a different user, this method just returns the current presence (either `active` or `away`).

        Tags:
            users
        """
        url = f"{self.base_url}/users.getPresence"
        query_params = {k: v for k, v in [('token', token), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_identity(self, token=None) -> Any:
        """
        Retrieves user identity information using the GET method, requiring a Slack authentication token with **identity.basic** scope.

        Args:
            token (string): Optional string parameter used to authenticate or authorize the GET request to retrieve user identity information via the "/users.identity" path.

        Returns:
            Any: You will receive at a minimum the following information:

        Tags:
            users
        """
        url = f"{self.base_url}/users.identity"
        query_params = {k: v for k, v in [('token', token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_info(self, token, include_locale=None, user=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a specified user in a Slack workspace, including their profile data.

        Args:
            token (string): The token query parameter is a required string used to authenticate and authorize the API request to access user information in the GET /users.info operation.
            include_locale (boolean): Indicates whether to include locale information in the response, with a value of true or false.
            user (string): A string parameter used to identify or specify a user in the request.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        url = f"{self.base_url}/users.info"
        query_params = {k: v for k, v in [('token', token), ('include_locale', include_locale), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_list(self, token=None, limit=None, cursor=None, include_locale=None) -> dict[str, Any]:
        """
        Lists all users in a Slack workspace, including invited and deleted/deactivated users, using the "users.list" API operation with parameters for pagination and locale inclusion.

        Args:
            token (string): Required authentication token for accessing the list of users.
            limit (integer): Specifies the maximum number of users to return in the response, defaults to 1.
            cursor (string): A unique string identifier used for cursor-based pagination, indicating the starting point for retrieving the next set of users in the list.
            include_locale (boolean): A boolean query parameter to optionally include locale information in the response.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        url = f"{self.base_url}/users.list"
        query_params = {k: v for k, v in [('token', token), ('limit', limit), ('cursor', cursor), ('include_locale', include_locale)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_lookup_by_email(self, token, email) -> dict[str, Any]:
        """
        Retrieves user information by email using the Slack API and requires a valid token and email address for lookup.

        Args:
            token (string): Required string token passed in the query to authenticate and authorize access for the GET operation at /users.lookupByEmail.
            email (string): The `email` parameter is a required string query parameter used to specify the email address for looking up users.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        url = f"{self.base_url}/users.lookupByEmail"
        query_params = {k: v for k, v in [('token', token), ('email', email)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def usersprofile_get_profile_info(self, token, include_labels=None, user=None) -> dict[str, Any]:
        """
        Retrieves a user's profile information, including custom status and other details, using the Slack API.

        Args:
            token (string): The token parameter in the query is a required string used to authenticate and authorize the request to access the user's profile information.
            include_labels (boolean): Include this boolean query parameter to specify whether to include user profile labels in the response.
            user (string): The user parameter is a string query parameter used to identify the user for whom the profile information is being retrieved.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users.profile, users
        """
        url = f"{self.base_url}/users.profile.get"
        query_params = {k: v for k, v in [('token', token), ('include_labels', include_labels), ('user', user)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def usersprofile_set_profile_info(self, name=None, profile=None, user=None, value=None) -> dict[str, Any]:
        """
        Updates a user's profile information, including name, email, and custom status, using the Slack API.

        Args:
            name (string): Name of a single key to set. Usable only if `profile` is not passed.
            profile (string): Collection of key:value pairs presented as a URL-encoded JSON hash. At most 50 fields may be set. Each field name is limited to 255 characters.
            user (string): ID of user to change. This argument may only be specified by team admins on paid teams.
            value (string): Value to set a single key to. Usable only if `profile` is not passed.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users.profile, users
        """
        request_body = {
            'name': name,
            'profile': profile,
            'user': user,
            'value': value,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/users.profile.set"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def users_set_active(self) -> dict[str, Any]:
        """
        Manually sets a Slack user's status as active, though this method is deprecated and no longer functional.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        url = f"{self.base_url}/users.setActive"
        query_params = {}
        response = self._post(url, data={}, params=query_params, content_type='application/json')
        response.raise_for_status()
        return response.json()

    def users_set_photo(self, token, crop_w=None, crop_x=None, crop_y=None, image=None) -> dict[str, Any]:
        """
        Updates a Slack user's profile image using the `POST` method, requiring a valid authentication token with the `users.profile:write` scope and supporting optional image cropping parameters.

        Args:
            token (string): Authentication token. Requires scope: `users.profile:write`
            crop_w (string): Width/height of crop box (always square)
            crop_x (string): X coordinate of top-left corner of crop box
            crop_y (string): Y coordinate of top-left corner of crop box
            image (string): File contents via `multipart/form-data`.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        request_body = {
            'crop_w': crop_w,
            'crop_x': crop_x,
            'crop_y': crop_y,
            'image': image,
            'token': token,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/users.setPhoto"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def users_set_presence(self, presence) -> dict[str, Any]:
        """
        Manually sets the calling user's presence status in Slack to either "away" or "auto" using a POST request and returns a success indicator.

        Args:
            presence (string): Either `auto` or `away`

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            users
        """
        request_body = {
            'presence': presence,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/users.setPresence"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params, content_type='application/x-www-form-urlencoded')
        response.raise_for_status()
        return response.json()

    def views_open(self, trigger_id, view) -> dict[str, Any]:
        """
        The API operation at path "/views.open" is not defined as using the "GET" method; however, the standard Slack API "views.open" method, which typically uses POST, opens a modal for a user by exchanging a trigger_id and defining a view structure. If it were hypothetically using "GET", the operation would likely retrieve or open a modal view based on a trigger_id and view parameters. However, the Slack API documentation indicates that this operation is performed via POST, not GET.

        Args:
            trigger_id (string): Unique identifier of the trigger to be queried, required for retrieving specific trigger information.
            view (string): Required string parameter to specify the view type for the request.

        Returns:
            dict[str, Any]: Typical success response includes the opened view payload.

        Tags:
            views
        """
        url = f"{self.base_url}/views.open"
        query_params = {k: v for k, v in [('trigger_id', trigger_id), ('view', view)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def views_publish(self, user_id, view, hash=None) -> dict[str, Any]:
        """
        Fetches and publishes a specific view for a user using the provided user ID and view name, optionally filtered by a hash value, and authenticates via a token in the header.

        Args:
            user_id (string): Unique identifier of the user for whom the publication views are being retrieved.
            view (string): The "view" query parameter specifies the identifier of the view to be published.
            hash (string): Unique string identifier used to specify or authenticate the publish view request.

        Returns:
            dict[str, Any]: Typical success response includes the published view payload.

        Tags:
            views
        """
        url = f"{self.base_url}/views.publish"
        query_params = {k: v for k, v in [('user_id', user_id), ('view', view), ('hash', hash)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def views_push(self, trigger_id, view) -> dict[str, Any]:
        """
        Pushes a new view onto the existing view stack in a Slack modal using the `views.push` method, requiring a valid `trigger_id` and a JSON-encoded view object, but this operation is typically performed via the POST method, not GET.

        Args:
            trigger_id (string): A unique identifier for the trigger, required for the GET operation at the "/views.push" path.
            view (string): Specifies the type of view to retrieve in the response, required for the operation, as a string value.

        Returns:
            dict[str, Any]: Typical success response includes the pushed view payload.

        Tags:
            views
        """
        url = f"{self.base_url}/views.push"
        query_params = {k: v for k, v in [('trigger_id', trigger_id), ('view', view)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def views_update(self, view_id=None, external_id=None, view=None, hash=None) -> dict[str, Any]:
        """
        Updates a view using the specified parameters and returns a response, requiring a token in the header and supporting optional query parameters for view ID, external ID, view details, and hash.

        Args:
            view_id (string): A unique string identifier used to specify which view to update in the GET operation at the "/views.update" path.
            external_id (string): Unique identifier provided by the client to associate and track the view across different systems and requests.
            view (string): The "view" query parameter specifies the identifier of the view to be updated.
            hash (string): A string parameter used to specify a unique hash value for the views update operation.

        Returns:
            dict[str, Any]: Typical success response includes the updated view payload.

        Tags:
            views
        """
        url = f"{self.base_url}/views.update"
        query_params = {k: v for k, v in [('view_id', view_id), ('external_id', external_id), ('view', view), ('hash', hash)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def workflows_step_completed(self, workflow_step_execute_id, outputs=None) -> dict[str, Any]:
        """
        Indicates that an app's step in a Slack workflow has completed execution, requiring a workflow step execution ID and optionally providing output data.

        Args:
            workflow_step_execute_id (string): Context identifier that maps to the correct workflow step execution.
            outputs (string): Specifies the output details for the completed workflow step, passed as a string in the query parameter.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            workflows
        """
        url = f"{self.base_url}/workflows.stepCompleted"
        query_params = {k: v for k, v in [('workflow_step_execute_id', workflow_step_execute_id), ('outputs', outputs)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def workflows_step_failed(self, workflow_step_execute_id, error) -> dict[str, Any]:
        """
        Indicates that a step in a Slack workflow has failed using the "workflows.stepFailed" API operation, which requires a token for authentication and returns a status message.

        Args:
            workflow_step_execute_id (string): Context identifier that maps to the correct workflow step execution.
            error (string): A string parameter indicating the error to be queried when retrieving workflows that have failed at a specific step.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            workflows
        """
        url = f"{self.base_url}/workflows.stepFailed"
        query_params = {k: v for k, v in [('workflow_step_execute_id', workflow_step_execute_id), ('error', error)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def workflows_update_step(self, workflow_step_edit_id, inputs=None, outputs=None, step_name=None, step_image_url=None) -> dict[str, Any]:
        """
        Updates the configuration of a workflow step using the "GET" method is not supported; however, the Slack API provides a similar operation via the "POST" method, which updates a workflow step's configuration using parameters such as inputs, outputs, step name, and step image URL.

        Args:
            workflow_step_edit_id (string): Unique identifier for editing a specific workflow step.
            inputs (string): A string parameter specifying the inputs required to update a workflow step.
            outputs (string): Specifies the output details for the workflow update step as a string.
            step_name (string): The name of the workflow step to be updated.
            step_image_url (string): URL of the image associated with the step to be updated in the workflow.

        Returns:
            dict[str, Any]: Typical success response

        Tags:
            workflows
        """
        url = f"{self.base_url}/workflows.updateStep"
        query_params = {k: v for k, v in [('workflow_step_edit_id', workflow_step_edit_id), ('inputs', inputs), ('outputs', outputs), ('step_name', step_name), ('step_image_url', step_image_url)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        return [
            self.adminapps_approve_app_installation,
            self.adminappsapproved_list,
            self.adminappsrequests_list,
            self.adminapps_restrict_app,
            self.adminappsrestricted_get_list,
            self.adminconversations_archive_channel,
            self.adminconversations_convert_to_private_channel,
            self.adminconversations_create_channel_based_conversation,
            self.adminconversations_delete_channel,
            self.adminconversations_disconnect_shared_channel,
            self.adminconversationsekm_list_original_connected_channel_info,
            self.adminconversations_get_conversation_prefs,
            self.adminconversations_get_teams_list,
            self.adminconversations_invite_user_to_channel,
            self.adminconversations_rename_channel,
            self.adminconversationsrestrict_access_add_group_idp_groups,
            self.adminconversationsrestrict_access_list_groups,
            self.adminconversationsrestrict_access_remove_idp_group,
            self.adminconversations_search_channels,
            self.adminconversations_set_conversation_prefs,
            self.adminconversations_set_teams_workspace_connection,
            self.adminconversations_unarchive_channel,
            self.adminemoji_add_emoji,
            self.adminemoji_alias_add,
            self.adminemoji_list_enterprise_emoji,
            self.adminemoji_remove_enterprise_emoji,
            self.adminemoji_rename_emoji,
            self.admininvite_requests_approve_request,
            self.admininvite_requestsapproved_list,
            self.admininvite_requestsdenied_list,
            self.admininvite_requests_deny_request,
            self.admininvite_requests_list_pending_workspace_invite_requests,
            self.adminteamsadmins_get_all,
            self.adminteams_create_enterprise_team,
            self.adminteams_list_all,
            self.adminteamsowners_list_owners,
            self.adminteamssettings_get_info,
            self.adminteamssettings_set_default_channels,
            self.adminteamssettings_set_description,
            self.adminteamssettings_set_discoverability_of_workspace,
            self.adminteamssettings_set_icon,
            self.adminteamssettings_set_name,
            self.adminusergroups_add_default_channels,
            self.adminusergroups_associate_default_workspaces,
            self.adminusergroups_list_channels_get,
            self.adminusergroups_remove_channels,
            self.adminusers_add_workspace_user,
            self.adminusers_invite_user_to_workspace,
            self.adminusers_list_workspace_users,
            self.adminusers_remove_user_from_workspace,
            self.adminuserssession_invalidate_session,
            self.adminuserssession_reset_sessions,
            self.adminusers_set_admin_user,
            self.adminusers_set_expiration_guest,
            self.adminusers_set_workspace_owner,
            self.adminusers_set_regular_user,
            self.api_test,
            self.appseventauthorizations_get_list,
            self.appspermissions_list_permissions,
            self.appspermissions_additional_scopes_request,
            self.appspermissionsresources_get_resources_list,
            self.appspermissionsscopes_get_list,
            self.appspermissionsusers_list_user_grants,
            self.appspermissionsusers_request_modal,
            self.apps_uninstall,
            self.auth_revoke,
            self.auth_test,
            self.bots_info,
            self.calls_add,
            self.calls_end,
            self.calls_info,
            self.callsparticipants_add_new_participant,
            self.callsparticipants_register_removed,
            self.calls_update,
            self.chat_delete,
            self.chat_delete_scheduled_message,
            self.chat_get_permalink,
            self.chat_me_message,
            self.chat_post_ephemeral,
            self.chat_post_message,
            self.chat_schedule_message,
            self.chatscheduled_messages_list,
            self.chat_unfurl,
            self.chat_update,
            self.conversations_archive,
            self.conversations_close,
            self.conversations_create,
            self.conversations_history,
            self.conversations_info,
            self.conversations_invite,
            self.conversations_join,
            self.conversations_kick,
            self.conversations_leave,
            self.conversations_list,
            self.conversations_mark,
            self.conversations_members,
            self.conversations_open,
            self.conversations_rename,
            self.conversations_replies,
            self.conversations_set_purpose,
            self.conversations_set_topic,
            self.conversations_unarchive,
            self.dialog_open,
            self.dnd_end_dnd,
            self.dnd_end_snooze,
            self.dnd_info,
            self.dnd_set_snooze,
            self.dnd_team_info,
            self.emoji_list,
            self.filescomments_delete_comment,
            self.files_delete,
            self.files_info,
            self.files_list,
            self.filesremote_add_from_remote,
            self.filesremote_get_info,
            self.filesremote_list_remote_files,
            self.filesremote_delete_file,
            self.filesremote_share_remote_file,
            self.filesremote_update_remote_file,
            self.files_revoke_public_url,
            self.files_shared_public_url,
            self.files_upload,
            self.migration_exchange,
            self.oauth_access,
            self.oauth_token,
            self.oauthv2_exchange_token,
            self.pins_add,
            self.pins_list,
            self.pins_remove,
            self.reactions_add,
            self.reactions_get,
            self.reactions_list,
            self.reactions_remove,
            self.reminders_add,
            self.reminders_complete,
            self.reminders_delete,
            self.reminders_info,
            self.reminders_list,
            self.rtm_connect,
            self.search_messages,
            self.stars_add,
            self.stars_list,
            self.stars_remove,
            self.team_access_logs,
            self.team_billable_info,
            self.team_info,
            self.team_integration_logs,
            self.teamprofile_get_profile,
            self.usergroups_create,
            self.usergroups_disable,
            self.usergroups_enable,
            self.usergroups_list,
            self.usergroups_update,
            self.usergroupsusers_list_all_users,
            self.usergroupsusers_update_list,
            self.users_conversations,
            self.users_delete_photo,
            self.users_get_presence,
            self.users_identity,
            self.users_info,
            self.users_list,
            self.users_lookup_by_email,
            self.usersprofile_get_profile_info,
            self.usersprofile_set_profile_info,
            self.users_set_active,
            self.users_set_photo,
            self.users_set_presence,
            self.views_open,
            self.views_publish,
            self.views_push,
            self.views_update,
            self.workflows_step_completed,
            self.workflows_step_failed,
            self.workflows_update_step
        ]
