from typing import Any
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration

class TwitterApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='twitter', integration=integration, **kwargs)
        self.base_url = "https://api.twitter.com"

    def list_batch_compliance_jobs(self, type, status=None, compliance_job_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of compliance jobs based on the specified job type, with optional filtering by status.

        Args:
            type (string): The type parameter specifies the compliance job type and must be either "tweets" or "users".
            status (string): Filters compliance jobs by their current status, which can be one of: created, in_progress, failed, or complete.
            compliance_job_fields (array): A comma separated list of ComplianceJob fields to display. Example: "['created_at', 'download_expires_at', 'download_url', 'id', 'name', 'resumable', 'status', 'type', 'upload_expires_at', 'upload_url']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Compliance
        """
        url = f"{self.base_url}/2/compliance/jobs"
        query_params = {k: v for k, v in [('type', type), ('status', status), ('compliance_job.fields', compliance_job_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_batch_compliance_job(self, type, name=None, resumable=None) -> dict[str, Any]:
        """
        Creates a new compliance job using JSON data in the request body and authenticates the request using a Bearer token.

        Args:
            type (string): Type of compliance job to list.
            name (string): User-provided name for a compliance job. Example: 'my-job'.
            resumable (boolean): If true, this endpoint will return a pre-signed URL with resumable uploads enabled.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Compliance
        """
        request_body = {
            'name': name,
            'resumable': resumable,
            'type': type,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/compliance/jobs"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_batch_compliance_job(self, id, compliance_job_fields=None) -> dict[str, Any]:
        """
        Retrieves information about a compliance job by its ID using the BearerToken for authentication.

        Args:
            id (string): id
            compliance_job_fields (array): A comma separated list of ComplianceJob fields to display. Example: "['created_at', 'download_expires_at', 'download_url', 'id', 'name', 'resumable', 'status', 'type', 'upload_expires_at', 'upload_url']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Compliance
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/compliance/jobs/{id}"
        query_params = {k: v for k, v in [('compliance_job.fields', compliance_job_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dm_conversation_id_create(self, conversation_type=None, message=None, participant_ids=None) -> dict[str, Any]:
        """
        Creates a new group Direct Message conversation and sends an initial message to the specified participants.

        Args:
            conversation_type (string): The conversation type that is being created.
            message (string): message
            participant_ids (array): Participants for the DM Conversation.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        request_body = {
            'conversation_type': conversation_type,
            'message': message,
            'participant_ids': participant_ids,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/dm_conversations"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dm_conversations_with_participant_id_dm_events(self, participant_id, max_results=None, pagination_token=None, event_types=None, dm_event_fields=None, expansions=None, media_fields=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of direct message events for a conversation with a specific participant, allowing for optional filtering by event types and pagination.

        Args:
            participant_id (string): participant_id
            max_results (integer): The maximum number of direct message events to return in the response, with a default of 100.
            pagination_token (string): The opaque token used to retrieve the next page of direct message events in the conversation with the specified participant.
            event_types (array): An optional array parameter specifying the types of DM events to include, such as "MessageCreate", "ParticipantsLeave", and "ParticipantsJoin", with default values of "MessageCreate", "ParticipantsLeave", and "ParticipantsJoin". Example: "['MessageCreate', 'ParticipantsLeave']".
            dm_event_fields (array): A comma separated list of DmEvent fields to display. Example: "['attachments', 'created_at', 'dm_conversation_id', 'entities', 'event_type', 'id', 'participant_ids', 'referenced_tweets', 'sender_id', 'text']".
            expansions (array): A comma separated list of fields to expand. Example: "['attachments.media_keys', 'participant_ids', 'referenced_tweets.id', 'sender_id']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        if participant_id is None:
            raise ValueError("Missing required parameter 'participant_id'")
        url = f"{self.base_url}/2/dm_conversations/with/{participant_id}/dm_events"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('event_types', event_types), ('dm_event.fields', dm_event_fields), ('expansions', expansions), ('media.fields', media_fields), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()


    def get_dm_conversations_id_dm_events(self, id, max_results=None, pagination_token=None, event_types=None, dm_event_fields=None, expansions=None, media_fields=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of direct message events for a specified conversation ID, allowing for optional filtering by event types and pagination.

        Args:
            id (string): id
            max_results (integer): Limits the number of DM events returned in the response, with a default value of 100, allowing users to customize the amount of data retrieved.
            pagination_token (string): Optional token used to paginate responses, specifying the resource to start fetching from for the next page of DM events.
            event_types (array): Filter the types of direct message events to return, such as message creation, participants joining, or leaving; defaults to ["MessageCreate","ParticipantsLeave","ParticipantsJoin"]. Example: "['MessageCreate', 'ParticipantsLeave']".
            dm_event_fields (array): A comma separated list of DmEvent fields to display. Example: "['attachments', 'created_at', 'dm_conversation_id', 'entities', 'event_type', 'id', 'participant_ids', 'referenced_tweets', 'sender_id', 'text']".
            expansions (array): A comma separated list of fields to expand. Example: "['attachments.media_keys', 'participant_ids', 'referenced_tweets.id', 'sender_id']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/dm_conversations/{id}/dm_events"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('event_types', event_types), ('dm_event.fields', dm_event_fields), ('expansions', expansions), ('media.fields', media_fields), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dm_events(self, max_results=None, pagination_token=None, event_types=None, dm_event_fields=None, expansions=None, media_fields=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of direct message events with optional filtering by event types, pagination, and field expansions for media, users, tweets, and DM event details.

        Args:
            max_results (integer): Limits the number of DM events returned in the response, with a default of 100 if not specified.
            pagination_token (string): Optional token used to specify the starting point for paginating the response of DM events.
            event_types (array): An optional array parameter specifying the types of events to retrieve, defaulting to ["MessageCreate", "ParticipantsLeave", "ParticipantsJoin"] if not provided. Example: "['MessageCreate', 'ParticipantsLeave']".
            dm_event_fields (array): A comma separated list of DmEvent fields to display. Example: "['attachments', 'created_at', 'dm_conversation_id', 'entities', 'event_type', 'id', 'participant_ids', 'referenced_tweets', 'sender_id', 'text']".
            expansions (array): A comma separated list of fields to expand. Example: "['attachments.media_keys', 'participant_ids', 'referenced_tweets.id', 'sender_id']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        url = f"{self.base_url}/2/dm_events"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('event_types', event_types), ('dm_event.fields', dm_event_fields), ('expansions', expansions), ('media.fields', media_fields), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def dm_event_delete(self, event_id) -> dict[str, Any]:
        """
        Deletes a DM event by its ID using the DELETE method, requiring authentication via OAuth2UserToken with "dm.read" and "dm.write" scopes or UserToken.

        Args:
            event_id (string): event_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        if event_id is None:
            raise ValueError("Missing required parameter 'event_id'")
        url = f"{self.base_url}/2/dm_events/{event_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_dm_events_by_id(self, event_id, dm_event_fields=None, expansions=None, media_fields=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific direct message event by its event ID with optional expansions and field selections.

        Args:
            event_id (string): event_id
            dm_event_fields (array): A comma separated list of DmEvent fields to display. Example: "['attachments', 'created_at', 'dm_conversation_id', 'entities', 'event_type', 'id', 'participant_ids', 'referenced_tweets', 'sender_id', 'text']".
            expansions (array): A comma separated list of fields to expand. Example: "['attachments.media_keys', 'participant_ids', 'referenced_tweets.id', 'sender_id']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Direct Messages
        """
        if event_id is None:
            raise ValueError("Missing required parameter 'event_id'")
        url = f"{self.base_url}/2/dm_events/{event_id}"
        query_params = {k: v for k, v in [('dm_event.fields', dm_event_fields), ('expansions', expansions), ('media.fields', media_fields), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_likes_compliance_stream(self, backfill_minutes=None, start_time=None, end_time=None) -> Any:
        """
        Streams compliance-related likes data using the GET method, allowing optional filtering by backfill minutes and time range.

        Args:
            backfill_minutes (integer): Specifies the number of minutes of missed data to recover in case of a disconnection, allowing retrieval of up to five minutes of past data.
            start_time (string): The optional start_time query parameter specifies the earliest timestamp from which to retrieve compliance stream data. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): Optional end time to filter the compliance stream, specified as a string. Example: '2021-02-01T18:40:40.000Z'.

        Returns:
            Any: The request has succeeded.

        Tags:
            Compliance
        """
        url = f"{self.base_url}/2/likes/compliance/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('start_time', start_time), ('end_time', end_time)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def likes_firehose_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None, like_with_tweet_author_fields=None, expansions=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Streams a real-time firehose of likes data filtered by partition and optional time range parameters, including expanded tweet and user fields, using Bearer Token authentication.

        Args:
            partition (integer): The partition query parameter specifies the integer identifier of the data subset or bucket to stream from the firehose endpoint, enabling segmented retrieval of likes data.
            backfill_minutes (integer): The number of minutes (up to five) to backfill and recover missed data from the stream after a disconnection.
            start_time (string): Optional query parameter specifying the start time for filtering the firehose stream of likes. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): The end_time query parameter specifies the optional cutoff timestamp to limit the data streamed to only items created before this time. Example: '2021-02-14T18:40:40.000Z'.
            like_with_tweet_author_fields (array): A comma separated list of LikeWithTweetAuthor fields to display. Example: "['created_at', 'id', 'liked_tweet_author_id', 'liked_tweet_id', 'timestamp_ms']".
            expansions (array): A comma separated list of fields to expand. Example: "['liked_tweet_author_id', 'liked_tweet_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Likes
        """
        url = f"{self.base_url}/2/likes/firehose/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('like_with_tweet_author.fields', like_with_tweet_author_fields), ('expansions', expansions), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def likes_sample10_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None, like_with_tweet_author_fields=None, expansions=None, user_fields=None, tweet_fields=None) -> dict[str, Any]:
        """
        Streams a sample of 10 likes using the GET method, optionally filtering by backfill minutes, partition, start and end times, and including specific tweet and user fields.

        Args:
            partition (integer): The partition query parameter specifies the integer identifier of the data partition to retrieve in the sample10 likes stream.
            backfill_minutes (integer): Optional integer parameter to specify the number of minutes of missed data to recover, used for reconnecting after a disconnection in the stream.
            start_time (string): Optional query parameter specifying the start time for filtering the stream of likes; defaults to no filtering if omitted. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): Optional query parameter specifying the end time for filtering the sample stream of likes. Example: '2021-02-14T18:40:40.000Z'.
            like_with_tweet_author_fields (array): A comma separated list of LikeWithTweetAuthor fields to display. Example: "['created_at', 'id', 'liked_tweet_author_id', 'liked_tweet_id', 'timestamp_ms']".
            expansions (array): A comma separated list of fields to expand. Example: "['liked_tweet_author_id', 'liked_tweet_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Likes
        """
        url = f"{self.base_url}/2/likes/sample10/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('like_with_tweet_author.fields', like_with_tweet_author_fields), ('expansions', expansions), ('user.fields', user_fields), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_id_create(self, description=None, name=None, private=None) -> dict[str, Any]:
        """
        Creates a new Twitter list using the X API v2 and returns the newly created list's details.

        Args:
            description (string): description
            name (string): name
            private (boolean): private

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        request_body = {
            'description': description,
            'name': name,
            'private': private,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/lists"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_id_delete(self, id) -> dict[str, Any]:
        """
        Deletes a list specified by its ID using the DELETE method.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/lists/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_id_get(self, id, list_fields=None, expansions=None, user_fields=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a specific Twitter List by its unique identifier, including optional expansions and fields for lists and users.

        Args:
            id (string): id
            list_fields (array): A comma separated list of List fields to display. Example: "['created_at', 'description', 'follower_count', 'id', 'member_count', 'name', 'owner_id', 'private']".
            expansions (array): A comma separated list of fields to expand. Example: "['owner_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/lists/{id}"
        query_params = {k: v for k, v in [('list.fields', list_fields), ('expansions', expansions), ('user.fields', user_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_id_update(self, id, description=None, name=None, private=None) -> dict[str, Any]:
        """
        Updates a list specified by the ID using the provided JSON payload, authenticating with OAuth2 or user tokens.

        Args:
            id (string): id
            description (string): description
            name (string): name
            private (boolean): private

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'description': description,
            'name': name,
            'private': private,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/lists/{id}"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_get_followers(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of users who follow a specified Twitter list using the list ID, with optional parameters for pagination and user data customization.

        Args:
            id (string): id
            max_results (integer): Specifies the maximum number of follower results to return, with a default value of 100.
            pagination_token (string): The pagination_token query parameter is an optional cursor used to retrieve the next page of results when paginating through the followers of a list.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/lists/{id}/followers"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_get_members(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of User objects that are members of a specified Twitter List by the provided List ID.

        Args:
            id (string): id
            max_results (integer): The maximum number of list members to return per page, defaulting to 100.
            pagination_token (string): Optional token used for cursor-based pagination, allowing retrieval of the next subset of members in the list.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/lists/{id}/members"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_add_member(self, id, user_id=None) -> dict[str, Any]:
        """
        Adds one or more members to a specified list by list ID using the POST method.

        Args:
            id (string): id
            user_id (string): Unique identifier of this User. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '2244994945'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'user_id': user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/lists/{id}/members"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_remove_member(self, id, user_id) -> dict[str, Any]:
        """
        Removes a member from a list using the provided list ID and user ID, requiring appropriate permissions for the operation.

        Args:
            id (string): id
            user_id (string): user_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if user_id is None:
            raise ValueError("Missing required parameter 'user_id'")
        url = f"{self.base_url}/2/lists/{id}/members/{user_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def lists_id_tweets(self, id, max_results=None, pagination_token=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of tweets for a specified list by ID using the "GET" method, allowing optional parameters for pagination and field customization.

        Args:
            id (string): id
            max_results (integer): The maximum number of tweets to return per request, with a default value of 100.
            pagination_token (string): Optional query parameter used to request the next page of results by passing the `next_token` value from the previous response.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/lists/{id}/tweets"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_open_api_spec(self) -> dict[str, Any]:
        """
        Retrieves the OpenAPI JSON file at the specified path "/2/openapi.json" using the GET method.

        Returns:
            dict[str, Any]: The request was successful

        Tags:
            General
        """
        url = f"{self.base_url}/2/openapi.json"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_spaces_by_ids(self, ids, space_fields=None, expansions=None, user_fields=None, topic_fields=None) -> dict[str, Any]:
        """
        Retrieves detailed information about specified spaces using the "GET" method, allowing customization through parameters such as space IDs, space fields, space expansions, user fields, and topic fields, while requiring authentication via Bearer or OAuth2 tokens for authorized access.

        Args:
            ids (array): Required array of IDs for the requested spaces.
            space_fields (array): A comma separated list of Space fields to display. Example: "['created_at', 'creator_id', 'ended_at', 'host_ids', 'id', 'invited_user_ids', 'is_ticketed', 'lang', 'participant_count', 'scheduled_start', 'speaker_ids', 'started_at', 'state', 'subscriber_count', 'title', 'topic_ids', 'updated_at']".
            expansions (array): A comma separated list of fields to expand. Example: "['creator_id', 'host_ids', 'invited_user_ids', 'speaker_ids', 'topic_ids']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            topic_fields (array): A comma separated list of Topic fields to display. Example: "['description', 'id', 'name']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces
        """
        url = f"{self.base_url}/2/spaces"
        query_params = {k: v for k, v in [('ids', ids), ('space.fields', space_fields), ('expansions', expansions), ('user.fields', user_fields), ('topic.fields', topic_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_spaces_by_creator_ids(self, user_ids, space_fields=None, expansions=None, user_fields=None, topic_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of spaces by their creator IDs using the specified user IDs, with optional filtering by space fields, space expansions, user fields, and topic fields.

        Args:
            user_ids (array): **user_ids**: Required array of user IDs for filtering spaces by their creators.
            space_fields (array): A comma separated list of Space fields to display. Example: "['created_at', 'creator_id', 'ended_at', 'host_ids', 'id', 'invited_user_ids', 'is_ticketed', 'lang', 'participant_count', 'scheduled_start', 'speaker_ids', 'started_at', 'state', 'subscriber_count', 'title', 'topic_ids', 'updated_at']".
            expansions (array): A comma separated list of fields to expand. Example: "['creator_id', 'host_ids', 'invited_user_ids', 'speaker_ids', 'topic_ids']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            topic_fields (array): A comma separated list of Topic fields to display. Example: "['description', 'id', 'name']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces
        """
        url = f"{self.base_url}/2/spaces/by/creator_ids"
        query_params = {k: v for k, v in [('user_ids', user_ids), ('space.fields', space_fields), ('expansions', expansions), ('user.fields', user_fields), ('topic.fields', topic_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_spaces(self, query, state=None, max_results=None, space_fields=None, expansions=None, user_fields=None, topic_fields=None) -> dict[str, Any]:
        """
        Searches for spaces using the specified query and optional filters like state, and returns the results with customizable fields and expansions.

        Args:
            query (string): The "query" parameter is a required string input for the GET operation at path "/2/spaces/search", used to specify search terms for finding spaces. Example: 'crypto'.
            state (string): Optional query parameter to filter search results by space state, which can be "live," "scheduled," or "all" (default).
            max_results (integer): Limits the number of search results returned, with a default of 100.
            space_fields (array): A comma separated list of Space fields to display. Example: "['created_at', 'creator_id', 'ended_at', 'host_ids', 'id', 'invited_user_ids', 'is_ticketed', 'lang', 'participant_count', 'scheduled_start', 'speaker_ids', 'started_at', 'state', 'subscriber_count', 'title', 'topic_ids', 'updated_at']".
            expansions (array): A comma separated list of fields to expand. Example: "['creator_id', 'host_ids', 'invited_user_ids', 'speaker_ids', 'topic_ids']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            topic_fields (array): A comma separated list of Topic fields to display. Example: "['description', 'id', 'name']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces
        """
        url = f"{self.base_url}/2/spaces/search"
        query_params = {k: v for k, v in [('query', query), ('state', state), ('max_results', max_results), ('space.fields', space_fields), ('expansions', expansions), ('user.fields', user_fields), ('topic.fields', topic_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_space_by_id(self, id, space_fields=None, expansions=None, user_fields=None, topic_fields=None) -> dict[str, Any]:
        """
        Retrieves details about a specific space by its ID, allowing optional customization through space fields, space expansions, user fields, and topic fields, using a Bearer or OAuth2 token for authentication.

        Args:
            id (string): id
            space_fields (array): A comma separated list of Space fields to display. Example: "['created_at', 'creator_id', 'ended_at', 'host_ids', 'id', 'invited_user_ids', 'is_ticketed', 'lang', 'participant_count', 'scheduled_start', 'speaker_ids', 'started_at', 'state', 'subscriber_count', 'title', 'topic_ids', 'updated_at']".
            expansions (array): A comma separated list of fields to expand. Example: "['creator_id', 'host_ids', 'invited_user_ids', 'speaker_ids', 'topic_ids']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            topic_fields (array): A comma separated list of Topic fields to display. Example: "['description', 'id', 'name']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/spaces/{id}"
        query_params = {k: v for k, v in [('space.fields', space_fields), ('expansions', expansions), ('user.fields', user_fields), ('topic.fields', topic_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def space_buyers(self, id, pagination_token=None, max_results=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of buyers for a specific space using the "GET" method, allowing optional pagination and customization of returned user and tweet fields.

        Args:
            id (string): id
            pagination_token (string): Optional token used for pagination to retrieve the next set of results in a sequence.
            max_results (integer): The maximum number of buyer results to return, defaulting to 100 if not specified.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces, Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/spaces/{id}/buyers"
        query_params = {k: v for k, v in [('pagination_token', pagination_token), ('max_results', max_results), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def space_tweets(self, id, max_results=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of tweets from a specified Twitter Space by its ID, with optional parameters to customize the fields and expansions included in the response.

        Args:
            id (string): id
            max_results (integer): The `max_results` parameter limits the number of tweets returned in the response for the GET operation at "/2/spaces/{id}/tweets", with a default of 100. Example: '25'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Spaces, Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/spaces/{id}/tweets"
        query_params = {k: v for k, v in [('max_results', max_results), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_trends(self, woeid, trend_fields=None) -> dict[str, Any]:
        """
        Retrieves trending information by WOEID (Where On Earth ID) using the specified trend fields and returns a response with a valid Bearer token.

        Args:
            woeid (string): woeid
            trend_fields (array): A comma separated list of Trend fields to display. Example: "['trend_name', 'tweet_count']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Trends
        """
        if woeid is None:
            raise ValueError("Missing required parameter 'woeid'")
        url = f"{self.base_url}/2/trends/by/woeid/{woeid}"
        query_params = {k: v for k, v in [('trend.fields', trend_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_tweets_by_id(self, ids, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves one or more Tweets by their IDs and returns associated details, supporting optional parameters for specifying additional fields and expansions.

        Args:
            ids (array): An array of IDs for the tweets to retrieve, required for the operation.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets, important
        """
        url = f"{self.base_url}/2/tweets"
        query_params = {k: v for k, v in [('ids', ids), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_tweet(self, card_uri=None, direct_message_deep_link=None, for_super_followers_only=None, geo=None, media=None, nullcast=None, poll=None, quote_tweet_id=None, reply=None, reply_settings=None, text=None) -> dict[str, Any]:
        """
        Creates a new tweet using the Twitter API v2, requiring an application/json payload and OAuth2 user token for authentication, and returns a 201 status upon successful creation.

        Args:
            card_uri (string): Card Uri Parameter. This is mutually exclusive from Quote Tweet Id, Poll, Media, and Direct Message Deep Link.
            direct_message_deep_link (string): Link to take the conversation from the public timeline to a private Direct Message.
            for_super_followers_only (boolean): Exclusive Tweet for super followers.
            geo (object): Place ID being attached to the Tweet for geo location.
            media (object): Media information being attached to created Tweet. This is mutually exclusive from Quote Tweet Id, Poll, and Card URI.
            nullcast (boolean): Nullcasted (promoted-only) Posts do not appear in the public timeline and are not served to followers.
            poll (object): Poll options for a Tweet with a poll. This is mutually exclusive from Media, Quote Tweet Id, and Card URI.
            quote_tweet_id (string): Unique identifier of this Tweet. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '1346889436626259968'.
            reply (object): Tweet information of the Tweet being replied to.
            reply_settings (string): Settings to indicate who can reply to the Tweet.
            text (string): The content of the Tweet. Example: 'Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        request_body = {
            'card_uri': card_uri,
            'direct_message_deep_link': direct_message_deep_link,
            'for_super_followers_only': for_super_followers_only,
            'geo': geo,
            'media': media,
            'nullcast': nullcast,
            'poll': poll,
            'quote_tweet_id': quote_tweet_id,
            'reply': reply,
            'reply_settings': reply_settings,
            'text': text,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/tweets"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_compliance_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None) -> Any:
        """
        Streams compliance events for tweets in real-time, allowing for the retrieval of events such as post deletions, edits, and withholdings, as well as user account changes, using parameters like partition, backfill_minutes, start_time, and end_time.

        Args:
            partition (integer): Specifies the partition number from which to retrieve compliance stream events, with a required integer value between 1 and 4.
            backfill_minutes (integer): Optional integer parameter to specify the number of minutes of data to recover from a stream disconnection, allowing retrieval of missed tweets.
            start_time (string): Optional string parameter specifying the earliest UTC timestamp from which compliance events will be provided, formatted as YYYY-MM-DDTHH:mm:ssZ. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): The `end_time` parameter specifies the latest UTC timestamp (in ISO 8601 format) until which compliance events will be streamed. Example: '2021-02-14T18:40:40.000Z'.

        Returns:
            Any: The request has succeeded.

        Tags:
            Compliance
        """
        url = f"{self.base_url}/2/tweets/compliance/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweet_counts_full_archive_search(self, query, start_time=None, end_time=None, since_id=None, until_id=None, next_token=None, pagination_token=None, granularity=None, search_count_fields=None) -> dict[str, Any]:
        """
        Retrieves the full-archive count of tweets for a specified query using the "/2/tweets/counts/all" endpoint, allowing optional filtering by start and end times, granularity, and pagination.

        Args:
            query (string): The "query" parameter is a required string used to filter tweets by specifying keywords or phrases, allowing users to retrieve counts for specific topics or hashtags. Example: '(from:TwitterDev OR from:TwitterAPI) has:media -is:retweet'.
            start_time (string): The start_time parameter sets the earliest timestamp from which to begin counting Tweets in the full-archive matching the query, formatted as an ISO 8601 string.
            end_time (string): The end_time parameter specifies the exclusive end timestamp to limit the search query for tweet counts in ISO 8601 format.
            since_id (string): Optional parameter to return results with a Tweet ID greater than the specified ID, effectively retrieving more recent Tweets. Example: '1346889436626259968'.
            until_id (string): Returns tweet counts with Tweet IDs less than (older than) the specified Tweet ID, limiting results to those before this ID. Example: '1346889436626259968'.
            next_token (string): Optional parameter to fetch the next page of results in a paginated response, obtained from the `meta.next_token` field of the previous response.
            pagination_token (string): Used to request the next page of results, providing the value of `next_token` from the previous response to paginate through data.
            granularity (string): The **granularity** parameter specifies the time unit for retrieving tweet counts, allowing options of "minute", "hour", or "day", with "hour" as the default.
            search_count_fields (array): A comma separated list of SearchCount fields to display. Example: "['end', 'start', 'tweet_count']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/counts/all"
        query_params = {k: v for k, v in [('query', query), ('start_time', start_time), ('end_time', end_time), ('since_id', since_id), ('until_id', until_id), ('next_token', next_token), ('pagination_token', pagination_token), ('granularity', granularity), ('search_count.fields', search_count_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweet_counts_recent_search(self, query, start_time=None, end_time=None, since_id=None, until_id=None, next_token=None, pagination_token=None, granularity=None, search_count_fields=None) -> dict[str, Any]:
        """
        Retrieves the count of recent Tweets that match a search query over the last seven days, using the "GET" method with optional parameters for specifying start and end times, granularity, and pagination.

        Args:
            query (string): The search query to filter recent tweets for counting matching tweets. Example: '(from:TwitterDev OR from:TwitterAPI) has:media -is:retweet'.
            start_time (string): Optional start time for the recent Tweet counts query, specified in ISO 8601 format, which determines the beginning of the time window for which Tweet counts are returned.
            end_time (string): Optional string parameter specifying the end time for the range of Tweets to be included in the count results, formatted in ISO 8601/RFC 3339.
            since_id (string): Optional parameter to retrieve recent tweet counts with IDs greater than the specified ID, returning data for tweets posted after that ID. Example: '1346889436626259968'.
            until_id (string): Optional parameter to specify the latest Tweet ID up to which the count of Tweets will be provided. Example: '1346889436626259968'.
            next_token (string): Optional parameter to paginate through results, used to retrieve the next page of tweet count data by including the token from the previous response's `meta.next_token` field.
            pagination_token (string): Optional parameter to paginate through the results, used by passing the `next_token` value from the previous response to retrieve the next page of tweet count data.
            granularity (string): The granularity parameter specifies the time interval for aggregating Tweet counts in the response, with possible values of "minute," "hour" (default), or "day".
            search_count_fields (array): A comma separated list of SearchCount fields to display. Example: "['end', 'start', 'tweet_count']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/counts/recent"
        query_params = {k: v for k, v in [('query', query), ('start_time', start_time), ('end_time', end_time), ('since_id', since_id), ('until_id', until_id), ('next_token', next_token), ('pagination_token', pagination_token), ('granularity', granularity), ('search_count.fields', search_count_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_firehose_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Streams all tweets in real-time using the Firehose API, allowing parameters such as partition, backfill minutes, start and end time, and various field expansions to customize the data retrieved, which requires authentication via a Bearer Token.

        Args:
            partition (integer): A required integer parameter that specifies the partition from which to retrieve the firehose stream data.
            backfill_minutes (integer): The backfill_minutes parameter allows requesting up to five minutes of missed streaming data to be delivered upon reconnection, helping recover Tweets lost during short disconnections; it accepts an integer value from 1 to 5 and is available only with Academic Research access.
            start_time (string): Optional ISO 8601-formatted timestamp indicating the earliest time from which to retrieve tweets, allowing filtering by time period. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): The end_time parameter specifies the exclusive upper bound timestamp to filter tweets created before this time in the stream. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/firehose/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_firehose_stream_lang_en(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Connects to the Twitter Firehose streaming API to receive a real-time stream of English-language tweets with optional filtering and data field expansions.

        Args:
            partition (integer): The `partition` parameter is an integer value required in the query for the GET operation at path "/2/tweets/firehose/stream/lang/en", specifying the partition number for the stream.
            backfill_minutes (integer): Requests up to five minutes of missed streaming data to be delivered upon reconnection, useful for recovering data lost during brief disconnections.
            start_time (string): Optional string parameter specifying the start time in ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ) to filter the oldest Tweets included in the response. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): Optional parameter to specify the end time for filtering tweets in the firehose stream, allowing retrieval of tweets created before this time. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/firehose/stream/lang/en"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_firehose_stream_lang_ja(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a stream of Tweets in Japanese using the Firehose API, allowing for real-time access to a high-volume stream of Tweets based on specified parameters such as partitions and optional backfill minutes, start and end times, and customizable fields for Tweets, users, and media.

        Args:
            partition (integer): The partition number used to identify and organize the data stream, which is required for this operation.
            backfill_minutes (integer): The number of minutes (1 to 5) of missed streaming data to backfill and recover upon reconnection, available only with Academic Research access.
            start_time (string): The start_time parameter specifies the oldest UTC timestamp in ISO 8601 format from which Tweets will be provided, inclusive and in second granularity. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): Optional query parameter to specify the end time for retrieving Tweets in the format compatible with the API's date and time requirements, limiting the results to those created before this time. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/firehose/stream/lang/ja"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_firehose_stream_lang_ko(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Streams real-time tweets in Korean from the Twitter firehose, allowing for optional backfill, specific partitions, and customizable start and end times, with support for various tweet, media, poll, user, and place fields.

        Args:
            partition (integer): The partition parameter specifies the integer partition number to use for streaming tweets.
            backfill_minutes (integer): The number of minutes (1 to 5) of previously missed Tweets to backfill and deliver upon reconnection, allowing recovery of up to five minutes of data missed during a disconnection; duplicates may occur and this feature requires Academic Research access.
            start_time (string): The "start_time" parameter specifies the earliest UTC timestamp from which Tweets should be retrieved, formatted as YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339). Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): end_time: Optional query parameter to specify the exclusive upper bound timestamp for filtering Tweets in the stream, returning only those created before this time. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/firehose/stream/lang/ko"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_firehose_stream_lang_pt(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Streams real-time Tweets in Portuguese using the Firehose API, allowing for filtering by specific parameters such as tweet fields, expansions, media, polls, users, and places, and requires a partition number for the stream.

        Args:
            partition (integer): The **partition** parameter is a required integer that specifies the partition number for the GET operation at the "/2/tweets/firehose/stream/lang/pt" path, used to distribute the stream of tweets across multiple partitions for efficient processing.
            backfill_minutes (integer): The number of minutes (1-5) of missed streaming data to recover and deliver upon reconnection, available only for Academic Research access.
            start_time (string): The "start_time" parameter specifies the starting point for retrieving Tweets, expressed in ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ), indicating the earliest UTC timestamp for which to include Tweets. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): The `end_time` parameter specifies the timestamp, in ISO 8601 format, after which tweets are not included in the response, allowing filtering of the firehose stream by a specific end time. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/firehose/stream/lang/pt"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_label_stream(self, backfill_minutes=None, start_time=None, end_time=None) -> Any:
        """
        Streams tweets labeled with a specific identifier in real-time using the Twitter API, allowing for optional parameters to specify backfill minutes, start time, and end time, and requires authentication via a Bearer Token.

        Args:
            backfill_minutes (integer): The number of minutes (up to five) of missed tweet data to recover and backfill after a disconnection, available for Academic Research access.
            start_time (string): Optional parameter specifying the earliest UTC timestamp (in ISO 8601/RFC 3339 format) from which to retrieve tweets, allowing filtering by creation time. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): Optional parameter specifying the end time in ISO 8601 format for retrieving tweets from a label stream, used to filter tweets created before this time. Example: '2021-02-01T18:40:40.000Z'.

        Returns:
            Any: The request has succeeded.

        Tags:
            Compliance
        """
        url = f"{self.base_url}/2/tweets/label/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('start_time', start_time), ('end_time', end_time)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def sample_stream(self, backfill_minutes=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a real-time sampled stream of public Tweets with optional parameters to specify Tweet, user, media, poll, and place fields, supporting backfill for missed data.

        Args:
            backfill_minutes (integer): The number of minutes (1 to 5) of missed streaming Tweets to backfill and receive upon reconnection, available for Academic Research access.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/sample/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_tweets_sample10_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Streams a random sample of 10% of all Tweets in real-time, allowing optional filtering by specifying additional parameters such as backfill minutes, partition, start and end times, and various field expansions for tweets, media, polls, users, and places.

        Args:
            partition (integer): The "partition" parameter specifies the partition number for the stream, which is required for the GET operation at path "/2/tweets/sample10/stream".
            backfill_minutes (integer): The `backfill_minutes` parameter allows you to request up to five minutes of missed streaming data to be delivered upon reconnection, helping recover data lost during disconnections; it is only available for Academic Research access.
            start_time (string): The `start_time` parameter specifies the earliest UTC timestamp from which tweets are returned, formatted as YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339), and is inclusive. Example: '2021-02-14T18:40:40.000Z'.
            end_time (string): An optional string parameter specifying the end time in seconds since the Unix epoch for which to stop streaming Tweets. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/sample10/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweets_fullarchive_search(self, query, start_time=None, end_time=None, since_id=None, until_id=None, max_results=None, next_token=None, pagination_token=None, sort_order=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves and returns a list of historical Tweets matching a specified query, allowing for filtering by time range, tweet ID, and other parameters.

        Args:
            query (string): The "query" parameter is a required string input used to specify the search criteria for retrieving tweets. Example: '(from:TwitterDev OR from:TwitterAPI) has:media -is:retweet'.
            start_time (string): Optional timestamp specifying the earliest date and time from which to retrieve Tweets, formatted as YYYY-MM-DDTHH:mm:ssZ in ISO 8601/RFC 3339 format; if not specified and end_time is provided, it defaults to 30 days before end_time.
            end_time (string): The **end_time** parameter specifies the most recent UTC timestamp (in ISO 8601/RFC 3339 format) up to which tweets are returned, exclusive of the specified time.
            since_id (string): Optional parameter to return results with IDs greater than (more recent than) the specified ID, useful for fetching new tweets since the last query. Example: '1346889436626259968'.
            until_id (string): Optional parameter specifying the Tweet ID to return results with IDs less than (i.e., older than) the given ID. Example: '1346889436626259968'.
            max_results (integer): Specifies the maximum number of Tweets to return per response page, with a default value of 10.
            next_token (string): Optional parameter used for pagination; it specifies a token to retrieve the next page of results in the search query response.
            pagination_token (string): The pagination_token query parameter is used to retrieve the next page of results by passing the next_token value returned in the previous response, enabling pagination through large result sets.
            sort_order (string): Optional query parameter to specify the order in which tweets are returned, either by most recent first ("recency") or by most relevant first ("relevancy").
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/search/all"
        query_params = {k: v for k, v in [('query', query), ('start_time', start_time), ('end_time', end_time), ('since_id', since_id), ('until_id', until_id), ('max_results', max_results), ('next_token', next_token), ('pagination_token', pagination_token), ('sort_order', sort_order), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweets_recent_search(self, query, start_time=None, end_time=None, since_id=None, until_id=None, max_results=None, next_token=None, pagination_token=None, sort_order=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves recent tweets based on a specified search query, allowing for optional filtering by time range and additional parameters such as tweet fields, expansions, and user details.

        Args:
            query (string): A string parameter used to specify the search query for retrieving recent tweets. Example: '(from:TwitterDev OR from:TwitterAPI) has:media -is:retweet'.
            start_time (string): Optional parameter to specify the earliest time to search for tweets, formatted as ISO8601/RFC3339 (e.g., 2023-05-12T00:00:00Z).
            end_time (string): Optional parameter to specify the UTC timestamp (in YYYY-MM-DDTHH:mm:ssZ format) up to which the returned Tweets are retrieved, exclusive of the specified time.
            since_id (string): Optional parameter to return results with an ID greater than the specified ID, retrieving more recent tweets. Example: '1346889436626259968'.
            until_id (string): Returns results with an ID less than (older than) the specified ID, limiting the search to tweets older than that ID. Example: '1346889436626259968'.
            max_results (integer): The "max_results" parameter specifies the maximum number of recent tweets to return per response page, with a default of 10 and a maximum of 100.
            next_token (string): Optional query parameter used to paginate results, specifying the token from a previous response to fetch the next page of tweets.
            pagination_token (string): Used to request the next page of results by passing the `next_token` value from the previous response.
            sort_order (string): Optional parameter to specify the order of search results, either by "recency" (most recent first) or "relevancy" (most relevant first).
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/search/recent"
        query_params = {k: v for k, v in [('query', query), ('start_time', start_time), ('end_time', end_time), ('since_id', since_id), ('until_id', until_id), ('max_results', max_results), ('next_token', next_token), ('pagination_token', pagination_token), ('sort_order', sort_order), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_stream(self, backfill_minutes=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Streams tweets based on predefined rules using the Twitter API v2, allowing for real-time filtering and retrieval of tweets with optional parameters for backfill minutes, start and end times, and various tweet, media, poll, user, and place fields.

        Args:
            backfill_minutes (integer): The "backfill_minutes" parameter allows clients to request up to five minutes of missed data upon reconnection, helping to recover Tweets that were missed due to a disconnection.
            start_time (string): The "start_time" parameter specifies the earliest UTC timestamp (in ISO 8601 format) from which to include Tweets in the search results. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): The timestamp (in ISO 8601/RFC 3339 format) specifying the exclusive upper bound of the time range for which Tweets will be returned. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/search/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_rules(self, ids=None, max_results=None, pagination_token=None) -> dict[str, Any]:
        """
        Retrieves the active stream filtering rules for a user's Twitter API v2 filtered stream, optionally filtered by rule IDs, with support for pagination and maximum results.

        Args:
            ids (array): Optional array of rule IDs to fetch a subset of rules from the user's active rule set.
            max_results (integer): The maximum number of stream filtering rules to return per response, up to 1000; defaults to 1000 if not specified.
            pagination_token (string): The `pagination_token` parameter is a string used to request the next page of results in a paginated response, typically obtained from the `next_token` value in the previous response.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        url = f"{self.base_url}/2/tweets/search/stream/rules"
        query_params = {k: v for k, v in [('ids', ids), ('max_results', max_results), ('pagination_token', pagination_token)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_rule_count(self, rules_count_fields=None) -> dict[str, Any]:
        """
        Retrieves the counts of Tweets matching specific search rules using the "GET" method, providing a way to analyze the volume of Tweets based on predefined criteria.

        Args:
            rules_count_fields (array): A comma separated list of RulesCount fields to display. Example: "['all_project_client_apps', 'cap_per_client_app', 'cap_per_project', 'client_app_rules_count', 'project_rules_count']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            General
        """
        url = f"{self.base_url}/2/tweets/search/stream/rules/counts"
        query_params = {k: v for k, v in [('rules_count.fields', rules_count_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_tweet_by_id(self, id) -> dict[str, Any]:
        """
        Deletes a specified Tweet by its ID on behalf of an authenticated user.

        Args:
            id (string): id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_tweet_by_id(self, id, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves detailed information about a single Tweet specified by its unique ID, with optional expansions for fields related to the Tweet, user, media, polls, and places.

        Args:
            id (string): id
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}"
        query_params = {k: v for k, v in [('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweets_id_liking_users(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of users who have liked a specified tweet using the provided tweet ID.

        Args:
            id (string): id
            max_results (integer): Specifies the maximum number of liking users to return in a response, with a default value of 100 and a maximum allowed value of 100.
            pagination_token (string): The pagination_token query parameter is an optional token used to retrieve the next page of results in a paginated response for the list of users who liked the tweet.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}/liking_users"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_tweets_that_quote_atweet(self, id, max_results=None, pagination_token=None, exclude=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of quote Tweets for a specified Tweet ID, allowing for optional parameters to customize the results with fields like tweet fields, media fields, and user expansions, and supports pagination for handling large responses.

        Args:
            id (string): id
            max_results (integer): Specifies the maximum number of quote Tweets to return in the response, ranging from 1 to 100, with a default of 10.
            pagination_token (string): pagination_token is an optional query parameter used to retrieve the next page of results by setting it to the next_token value returned in the previous response.
            exclude (array): Optional array parameter to exclude specific types of Tweet results from the response, such as retweets. Example: "['replies', 'retweets']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}/quote_tweets"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('exclude', exclude), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def tweets_id_retweeting_users(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of User objects representing users who have retweeted the Tweet specified by the given Tweet ID.

        Args:
            id (string): id
            max_results (integer): The `max_results` parameter specifies the maximum number of users to return who have retweeted the specified Tweet, with a default value of 100 and a required range of 1 to 100.
            pagination_token (string): Optional parameter used to retrieve the next page of results by passing the value of the `next_token` returned in the previous response.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}/retweeted_by"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_tweets_that_retweet_atweet(self, id, max_results=None, pagination_token=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of retweets for a specified Tweet ID, optionally allowing for pagination and customization of returned fields via query parameters.

        Args:
            id (string): id
            max_results (integer): Specifies the maximum number of retweets to return per request, with a default of 100 and a maximum value of 100.
            pagination_token (string): Used to request the next page of results, set this parameter to the `next_token` value returned in the previous response.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/tweets/{id}/retweets"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def hide_reply_by_id(self, tweet_id, hidden=None) -> dict[str, Any]:
        """
        Hides or unhides a reply to a specified Tweet by its tweet_id.

        Args:
            tweet_id (string): tweet_id
            hidden (boolean): hidden

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if tweet_id is None:
            raise ValueError("Missing required parameter 'tweet_id'")
        request_body = {
            'hidden': hidden,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/tweets/{tweet_id}/hidden"
        query_params = {}
        response = self._put(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_usage_tweets(self, days=None, usage_fields=None) -> dict[str, Any]:
        """
        Retrieves and returns Twitter usage data using the specified fields and optionally filters by a number of days.

        Args:
            days (integer): Number of days to include in the tweet usage data, defaulting to 7 if not specified.
            usage_fields (array): A comma separated list of Usage fields to display. Example: "['cap_reset_day', 'daily_client_app_usage', 'daily_project_usage', 'project_cap', 'project_id', 'project_usage']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Usage
        """
        url = f"{self.base_url}/2/usage/tweets"
        query_params = {k: v for k, v in [('days', days), ('usage.fields', usage_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_by_id(self, ids, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves information about one or more users specified by their IDs, allowing for customization with user fields and expansions.

        Args:
            ids (array): A required query parameter specifying an array of user IDs to retrieve information for multiple users in a single request. Example: '2244994945,6253282,12'.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        url = f"{self.base_url}/2/users"
        query_params = {k: v for k, v in [('ids', ids), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_users_by_username(self, usernames, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves information about one or more users specified by their usernames using the Twitter API, allowing optional specification of additional user fields and expansions.

        Args:
            usernames (array): Required array of usernames to filter users by. Example: 'TwitterDev,TwitterAPI'.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users, important
        """
        url = f"{self.base_url}/2/users/by"
        query_params = {k: v for k, v in [('usernames', usernames), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_user_by_username(self, username, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves information about a user specified by their username, optionally including additional fields and expansions, using the "GET" method with authentication.

        Args:
            username (string): username
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if username is None:
            raise ValueError("Missing required parameter 'username'")
        url = f"{self.base_url}/2/users/by/username/{username}"
        query_params = {k: v for k, v in [('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_users_compliance_stream(self, partition, backfill_minutes=None, start_time=None, end_time=None) -> Any:
        """
        Streams compliance data for users using the "GET" method, supporting optional backfill minutes, start and end times, and requiring a partition parameter.

        Args:
            partition (integer): The "partition" parameter is a required integer query parameter that determines which partition of the compliance stream data to retrieve.
            backfill_minutes (integer): Optional integer parameter to specify the number of minutes of missed data to recover after a disconnection; valid values are between 1 and 5 minutes.
            start_time (string): Optional start time in string format for filtering the compliance stream. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): Optional end time for filtering the compliance stream data, specified as a string. Example: '2021-02-01T18:40:40.000Z'.

        Returns:
            Any: The request has succeeded.

        Tags:
            Compliance
        """
        url = f"{self.base_url}/2/users/compliance/stream"
        query_params = {k: v for k, v in [('backfill_minutes', backfill_minutes), ('partition', partition), ('start_time', start_time), ('end_time', end_time)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_my_user(self, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves detailed information about the authenticated user, including optional expansions and fields for user and tweet data.

        Args:
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        url = f"{self.base_url}/2/users/me"
        query_params = {k: v for k, v in [('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def search_user_by_query(self, query, max_results=None, next_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Searches for users using a query string, returning a list of matching users with optional fields for user details, expansions, and related tweet fields.

        Args:
            query (string): Search query to filter users based on specific criteria. Example: 'someXUser'.
            max_results (integer): Maximum number of results to return in the search query, with a default of 100.
            next_token (string): The token used for pagination to retrieve the next set of user search results.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        url = f"{self.base_url}/2/users/search"
        query_params = {k: v for k, v in [('query', query), ('max_results', max_results), ('next_token', next_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def find_user_by_id(self, id, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves information about a user specified by their ID, with optional parameters for specifying additional user fields, expansions, and tweet fields.

        Args:
            id (string): id
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}"
        query_params = {k: v for k, v in [('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_blocking(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of user objects that are blocked by the specified user ID, allowing for additional fields and expansions to be specified.

        Args:
            id (string): id
            max_results (integer): Limits the number of user blocking records returned in the response, with no default value set and requiring an integer input.
            pagination_token (string): The pagination_token query parameter is an optional opaque string token used to retrieve the next page of results when paginating through a user's blocked accounts.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/blocking"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_users_id_bookmarks(self, id, max_results=None, pagination_token=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of bookmarks for a user with the specified ID, allowing optional pagination and customization of returned fields.

        Args:
            id (string): id
            max_results (integer): The "max_results" parameter, an optional integer query parameter with a default value of 2, limits the number of bookmark results returned when retrieving a user's bookmarks via the GET operation at "/2/users/{id}/bookmarks".
            pagination_token (string): The pagination_token query parameter is an optional token used to retrieve the next page of results in a paginated response for the user's bookmarks.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Bookmarks
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/bookmarks"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def post_users_id_bookmarks(self, id, tweet_id) -> dict[str, Any]:
        """
        Adds bookmarks for a specified user using the provided JSON data and returns a successful response upon completion.

        Args:
            id (string): id
            tweet_id (string): Unique identifier of this Tweet. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '1346889436626259968'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Bookmarks
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'tweet_id': tweet_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/bookmarks"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_bookmarks_delete(self, id, tweet_id) -> dict[str, Any]:
        """
        Deletes a bookmarked tweet for a specified user using the "DELETE" method.

        Args:
            id (string): id
            tweet_id (string): tweet_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Bookmarks
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if tweet_id is None:
            raise ValueError("Missing required parameter 'tweet_id'")
        url = f"{self.base_url}/2/users/{id}/bookmarks/{tweet_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def user_followed_lists(self, id, max_results=None, pagination_token=None, list_fields=None, expansions=None, user_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of Twitter lists followed by a specified user, with optional parameters for pagination, list fields, and user fields.

        Args:
            id (string): id
            max_results (integer): Specifies the maximum number of followed lists to return per page, with a default value of 100.
            pagination_token (string): The pagination_token query parameter is an optional token used to retrieve the next page of results in a paginated response for followed lists.
            list_fields (array): A comma separated list of List fields to display. Example: "['created_at', 'description', 'follower_count', 'id', 'member_count', 'name', 'owner_id', 'private']".
            expansions (array): A comma separated list of fields to expand. Example: "['owner_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/followed_lists"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('list.fields', list_fields), ('expansions', expansions), ('user.fields', user_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_follow(self, id, list_id=None) -> dict[str, Any]:
        """
        Adds a Twitter user to a list of followed lists using the Twitter API and returns a status message.

        Args:
            id (string): id
            list_id (string): The unique identifier of this List. Example: '1146654567674912769'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists, important
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'list_id': list_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/followed_lists"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_unfollow(self, id, list_id) -> dict[str, Any]:
        """
        Deletes the specified list followed by the user identified by the given user ID and list ID.

        Args:
            id (string): id
            list_id (string): list_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if list_id is None:
            raise ValueError("Missing required parameter 'list_id'")
        url = f"{self.base_url}/2/users/{id}/followed_lists/{list_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_followers(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of users who follow a specified user using the Twitter API, with optional parameters for result pagination and additional user or tweet fields.

        Args:
            id (string): id
            max_results (integer): The maximum number of follower results to return in the response.
            pagination_token (string): An optional token used for pagination to continue retrieving followers from a specific point in the dataset.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/followers"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_following(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of users followed by the specified user ID, allowing optional parameters to customize the response with additional user fields, expansions, and tweet fields.

        Args:
            id (string): id
            max_results (integer): Optional parameter to limit the number of results returned in the response for the GET operation at "/2/users/{id}/following", specified as an integer.
            pagination_token (string): An opaque token used for pagination, allowing the retrieval of the next batch of results when navigating through a large dataset of users that the specified user is following.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/following"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_follow(self, id, target_user_id=None) -> dict[str, Any]:
        """
        Follows another user on behalf of the current user using the Twitter API, returning a status message indicating whether the action was successful.

        Args:
            id (string): id
            target_user_id (string): Unique identifier of this User. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '2244994945'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'target_user_id': target_user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/following"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_liked_tweets(self, id, max_results=None, pagination_token=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of tweets liked by the specified user, supporting pagination and optional expansions and fields for tweets, users, media, polls, and places.

        Args:
            id (string): id
            max_results (integer): Optional integer parameter to limit the number of liked tweets returned in the response.
            pagination_token (string): The pagination_token query parameter is an optional opaque string token used to fetch the next page of results in the user's liked tweets timeline.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/liked_tweets"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_like(self, id, tweet_id=None) -> dict[str, Any]:
        """
        Creates a new like for a user's content using the provided user ID and returns a status message.

        Args:
            id (string): id
            tweet_id (string): Unique identifier of this Tweet. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '1346889436626259968'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'tweet_id': tweet_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/likes"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_unlike(self, id, tweet_id) -> dict[str, Any]:
        """
        Deletes a user's like on a specific tweet using the provided user ID and tweet ID, requiring OAuth2UserToken with "like.write," "tweet.read," and "users.read" permissions.

        Args:
            id (string): id
            tweet_id (string): tweet_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if tweet_id is None:
            raise ValueError("Missing required parameter 'tweet_id'")
        url = f"{self.base_url}/2/users/{id}/likes/{tweet_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_list_memberships(self, id, max_results=None, pagination_token=None, list_fields=None, expansions=None, user_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of memberships for a specified user using their ID, allowing for optional filtering by maximum results and pagination, and returns the membership details.

        Args:
            id (string): id
            max_results (integer): The maximum number of membership results to return, defaulting to 100 if not specified.
            pagination_token (string): An optional token used for pagination to navigate through the list of memberships for a user, typically provided in the response of a previous request.
            list_fields (array): A comma separated list of List fields to display. Example: "['created_at', 'description', 'follower_count', 'id', 'member_count', 'name', 'owner_id', 'private']".
            expansions (array): A comma separated list of fields to expand. Example: "['owner_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/list_memberships"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('list.fields', list_fields), ('expansions', expansions), ('user.fields', user_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_mentions(self, id, since_id=None, until_id=None, max_results=None, pagination_token=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves the timeline of tweets that mention the user associated with the provided ID, allowing for customization with parameters such as since and until IDs, pagination tokens, and various field expansions.

        Args:
            id (string): id
            since_id (string): Optional parameter to return results with an ID greater than (i.e., more recent than) the specified ID. Example: '1346889436626259968'.
            until_id (string): Optional identifier to fetch mentions until this specific user ID. Example: '1346889436626259968'.
            max_results (integer): Limits the number of mention items returned in the response.
            pagination_token (string): Optional token used for pagination, allowing continuation from a specific point in the list of mentions.
            start_time (string): Optional start time in string format to filter mentions. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): Optional end time filter for retrieving user mentions, specified in a string format. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/mentions"
        query_params = {k: v for k, v in [('since_id', since_id), ('until_id', until_id), ('max_results', max_results), ('pagination_token', pagination_token), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_muting(self, id, max_results=None, pagination_token=None, user_fields=None, expansions=None, tweet_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of users muted by the specified user using the Twitter API with optional filtering by max results, pagination token, user fields, user expansions, tweet fields, and returns the response upon authorization with the required "mute.read," "tweet.read," and "users.read" scopes.

        Args:
            id (string): id
            max_results (integer): The "max_results" parameter limits the number of results returned in the response for the GET operation at "/2/users/{id}/muting", with a default value of 100.
            pagination_token (string): The token to retrieve the next page of results when paginating through muted users; omit to start from the first page.
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['affiliation.user_id', 'most_recent_tweet_id', 'pinned_tweet_id']".
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/muting"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('user.fields', user_fields), ('expansions', expansions), ('tweet.fields', tweet_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_mute(self, id, target_user_id=None) -> dict[str, Any]:
        """
        Mutes a user identified by their ID using the API, requiring a POST request with appropriate OAuth2 credentials.

        Args:
            id (string): id
            target_user_id (string): Unique identifier of this User. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '2244994945'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'target_user_id': target_user_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/muting"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_owned_lists(self, id, max_results=None, pagination_token=None, list_fields=None, expansions=None, user_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of Twitter Lists owned by the specified user, supporting optional pagination and field expansions.

        Args:
            id (string): id
            max_results (integer): Maximum number of owned lists to return in the response; defaults to 100 if not specified.
            pagination_token (string): An optional token used for pagination, allowing users to fetch subsequent pages of results for the owned lists of a specified user.
            list_fields (array): A comma separated list of List fields to display. Example: "['created_at', 'description', 'follower_count', 'id', 'member_count', 'name', 'owner_id', 'private']".
            expansions (array): A comma separated list of fields to expand. Example: "['owner_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/owned_lists"
        query_params = {k: v for k, v in [('max_results', max_results), ('pagination_token', pagination_token), ('list.fields', list_fields), ('expansions', expansions), ('user.fields', user_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_pinned_lists(self, id, list_fields=None, expansions=None, user_fields=None) -> dict[str, Any]:
        """
        Retrieves the pinned Lists of a specified user by their user ID, returning detailed information about each pinned List.

        Args:
            id (string): id
            list_fields (array): A comma separated list of List fields to display. Example: "['created_at', 'description', 'follower_count', 'id', 'member_count', 'name', 'owner_id', 'private']".
            expansions (array): A comma separated list of fields to expand. Example: "['owner_id']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/pinned_lists"
        query_params = {k: v for k, v in [('list.fields', list_fields), ('expansions', expansions), ('user.fields', user_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_pin(self, id, list_id) -> dict[str, Any]:
        """
        Creates a pinned list for a user identified by {id} using JSON data and OAuth2UserToken or UserToken authentication.

        Args:
            id (string): id
            list_id (string): The unique identifier of this List. Example: '1146654567674912769'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'list_id': list_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/pinned_lists"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_user_unpin(self, id, list_id) -> dict[str, Any]:
        """
        Deletes a specified pinned list from a user's account by user ID and list ID.

        Args:
            id (string): id
            list_id (string): list_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Lists
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if list_id is None:
            raise ValueError("Missing required parameter 'list_id'")
        url = f"{self.base_url}/2/users/{id}/pinned_lists/{list_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_retweets(self, id, tweet_id=None) -> dict[str, Any]:
        """
        Retweets a post using the X API on behalf of a specified user, requiring authentication with OAuth2UserToken and appropriate permissions.

        Args:
            id (string): id
            tweet_id (string): Unique identifier of this Tweet. This is returned as a string in order to avoid complications with languages and tools that cannot handle large integers. Example: '1346889436626259968'.

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        request_body = {
            'tweet_id': tweet_id,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/2/users/{id}/retweets"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_unretweets(self, id, source_tweet_id) -> dict[str, Any]:
        """
        Undoes a retweet of a specified tweet by a user using the Twitter API v2, requiring OAuth authentication and user permissions.

        Args:
            id (string): id
            source_tweet_id (string): source_tweet_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        if source_tweet_id is None:
            raise ValueError("Missing required parameter 'source_tweet_id'")
        url = f"{self.base_url}/2/users/{id}/retweets/{source_tweet_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_timeline(self, id, since_id=None, until_id=None, max_results=None, pagination_token=None, exclude=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a user's reverse chronological timeline, returning tweets in the order they were posted, with optional filtering by time range, tweet IDs, and additional metadata fields.

        Args:
            id (string): id
            since_id (string): The `since_id` parameter specifies the smallest ID of the statuses to be returned, retrieving the newest statuses first, but it may not return all statuses if there are too many between the newest and the specified ID. Example: '791775337160081409'.
            until_id (string): Optional ID to retrieve timelines up to this user ID in reverse chronological order. Example: '1346889436626259968'.
            max_results (integer): **max_results**: Optional integer parameter specifying the maximum number of results to return for the GET operation.
            pagination_token (string): Optional token used to paginate the response, specifying the point to start retrieving resources from in the reverse chronological timeline.
            exclude (array): A query parameter to specify an array of fields or properties to exclude from the response. Example: "['replies', 'retweets']".
            start_time (string): Optional start time parameter to filter timelines by specifying the earliest date and time for which entries should be included. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): The end_time query parameter specifies the optional timestamp that defines the upper bound (latest) for filtering tweets in the reverse chronological timeline of a user. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/timelines/reverse_chronological"
        query_params = {k: v for k, v in [('since_id', since_id), ('until_id', until_id), ('max_results', max_results), ('pagination_token', pagination_token), ('exclude', exclude), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_tweets(self, id, since_id=None, until_id=None, max_results=None, pagination_token=None, exclude=None, start_time=None, end_time=None, tweet_fields=None, expansions=None, media_fields=None, poll_fields=None, user_fields=None, place_fields=None) -> dict[str, Any]:
        """
        Retrieves a list of tweets for a user with the specified ID, allowing optional filtering by tweet ID range, result count, pagination token, excluded fields, and time range, using the "GET" method.

        Args:
            id (string): id
            since_id (string): Returns only Tweets with IDs greater than (more recent than) the specified ID, allowing retrieval of Tweets posted after that ID. Example: '791775337160081409'.
            until_id (string): Returns tweets with IDs less than (older than) the specified until_id, limiting results to tweets posted before that ID. Example: '1346889436626259968'.
            max_results (integer): Specifies the maximum number of tweets to return per GET request for a user's tweets, with this parameter being optional and of type integer.
            pagination_token (string): Optional token used for pagination to continue retrieving results from a previous query.
            exclude (array): A query parameter to exclude specific properties from the response; accepts an array of property names to omit. Example: "['replies', 'retweets']".
            start_time (string): The start_time query parameter is an optional ISO 8601 timestamp string used to specify the earliest time from which to retrieve tweets for the user. Example: '2021-02-01T18:40:40.000Z'.
            end_time (string): Optional query parameter to filter tweets by specifying the end time, in string format, for retrieving tweets before this time. Example: '2021-02-14T18:40:40.000Z'.
            tweet_fields (array): A comma separated list of Tweet fields to display. Example: "['article', 'attachments', 'author_id', 'card_uri', 'context_annotations', 'conversation_id', 'created_at', 'edit_controls', 'edit_history_tweet_ids', 'entities', 'geo', 'id', 'in_reply_to_user_id', 'lang', 'non_public_metrics', 'note_tweet', 'organic_metrics', 'possibly_sensitive', 'promoted_metrics', 'public_metrics', 'referenced_tweets', 'reply_settings', 'scopes', 'source', 'text', 'username', 'withheld']".
            expansions (array): A comma separated list of fields to expand. Example: "['article.cover_media', 'article.media_entities', 'attachments.media_keys', 'attachments.media_source_tweet', 'attachments.poll_ids', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username', 'geo.place_id', 'in_reply_to_user_id', 'entities.note.mentions.username', 'referenced_tweets.id', 'referenced_tweets.id.author_id', 'author_screen_name']".
            media_fields (array): A comma separated list of Media fields to display. Example: "['alt_text', 'duration_ms', 'height', 'media_key', 'non_public_metrics', 'organic_metrics', 'preview_image_url', 'promoted_metrics', 'public_metrics', 'type', 'url', 'variants', 'width']".
            poll_fields (array): A comma separated list of Poll fields to display. Example: "['duration_minutes', 'end_datetime', 'id', 'options', 'voting_status']".
            user_fields (array): A comma separated list of User fields to display. Example: "['affiliation', 'connection_status', 'created_at', 'description', 'entities', 'id', 'location', 'most_recent_tweet_id', 'name', 'pinned_tweet_id', 'profile_banner_url', 'profile_image_url', 'protected', 'public_metrics', 'receives_your_dm', 'subscription_type', 'url', 'username', 'verified', 'verified_type', 'withheld']".
            place_fields (array): A comma separated list of Place fields to display. Example: "['contained_within', 'country', 'country_code', 'full_name', 'geo', 'id', 'name', 'place_type']".

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Tweets, important
        """
        if id is None:
            raise ValueError("Missing required parameter 'id'")
        url = f"{self.base_url}/2/users/{id}/tweets"
        query_params = {k: v for k, v in [('since_id', since_id), ('until_id', until_id), ('max_results', max_results), ('pagination_token', pagination_token), ('exclude', exclude), ('start_time', start_time), ('end_time', end_time), ('tweet.fields', tweet_fields), ('expansions', expansions), ('media.fields', media_fields), ('poll.fields', poll_fields), ('user.fields', user_fields), ('place.fields', place_fields)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_unfollow(self, source_user_id, target_user_id) -> dict[str, Any]:
        """
        Unfollows a target user by deleting the follow relationship between the source user and the target user using the "DELETE" method.

        Args:
            source_user_id (string): source_user_id
            target_user_id (string): target_user_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if source_user_id is None:
            raise ValueError("Missing required parameter 'source_user_id'")
        if target_user_id is None:
            raise ValueError("Missing required parameter 'target_user_id'")
        url = f"{self.base_url}/2/users/{source_user_id}/following/{target_user_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def users_id_unmute(self, source_user_id, target_user_id) -> dict[str, Any]:
        """
        Unmutes a target user using the "DELETE" method on the "/2/users/{source_user_id}/muting/{target_user_id}" path, reversing the mute action applied by the source user to the target user.

        Args:
            source_user_id (string): source_user_id
            target_user_id (string): target_user_id

        Returns:
            dict[str, Any]: The request has succeeded.

        Tags:
            Users
        """
        if source_user_id is None:
            raise ValueError("Missing required parameter 'source_user_id'")
        if target_user_id is None:
            raise ValueError("Missing required parameter 'target_user_id'")
        url = f"{self.base_url}/2/users/{source_user_id}/muting/{target_user_id}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        return [
            self.list_batch_compliance_jobs,
            self.create_batch_compliance_job,
            self.get_batch_compliance_job,
            self.dm_conversation_id_create,
            self.get_dm_conversations_with_participant_id_dm_events,
            self.get_dm_conversations_id_dm_events,
            self.get_dm_events,
            self.dm_event_delete,
            self.get_dm_events_by_id,
            self.get_likes_compliance_stream,
            self.likes_firehose_stream,
            self.likes_sample10_stream,
            self.list_id_create,
            self.list_id_delete,
            self.list_id_get,
            self.list_id_update,
            self.list_get_followers,
            self.list_get_members,
            self.list_add_member,
            self.list_remove_member,
            self.lists_id_tweets,
            self.get_open_api_spec,
            self.find_spaces_by_ids,
            self.find_spaces_by_creator_ids,
            self.search_spaces,
            self.find_space_by_id,
            self.space_buyers,
            self.space_tweets,
            self.get_trends,
            self.find_tweets_by_id,
            self.create_tweet,
            self.get_tweets_compliance_stream,
            self.tweet_counts_full_archive_search,
            self.tweet_counts_recent_search,
            self.get_tweets_firehose_stream,
            self.get_tweets_firehose_stream_lang_en,
            self.get_tweets_firehose_stream_lang_ja,
            self.get_tweets_firehose_stream_lang_ko,
            self.get_tweets_firehose_stream_lang_pt,
            self.get_tweets_label_stream,
            self.sample_stream,
            self.get_tweets_sample10_stream,
            self.tweets_fullarchive_search,
            self.tweets_recent_search,
            self.search_stream,
            self.get_rules,
            self.get_rule_count,
            self.delete_tweet_by_id,
            self.find_tweet_by_id,
            self.tweets_id_liking_users,
            self.find_tweets_that_quote_atweet,
            self.tweets_id_retweeting_users,
            self.find_tweets_that_retweet_atweet,
            self.hide_reply_by_id,
            self.get_usage_tweets,
            self.find_users_by_id,
            self.find_users_by_username,
            self.find_user_by_username,
            self.get_users_compliance_stream,
            self.find_my_user,
            self.search_user_by_query,
            self.find_user_by_id,
            self.users_id_blocking,
            self.get_users_id_bookmarks,
            self.post_users_id_bookmarks,
            self.users_id_bookmarks_delete,
            self.user_followed_lists,
            self.list_user_follow,
            self.list_user_unfollow,
            self.users_id_followers,
            self.users_id_following,
            self.users_id_follow,
            self.users_id_liked_tweets,
            self.users_id_like,
            self.users_id_unlike,
            self.get_user_list_memberships,
            self.users_id_mentions,
            self.users_id_muting,
            self.users_id_mute,
            self.list_user_owned_lists,
            self.list_user_pinned_lists,
            self.list_user_pin,
            self.list_user_unpin,
            self.users_id_retweets,
            self.users_id_unretweets,
            self.users_id_timeline,
            self.users_id_tweets,
            self.users_id_unfollow,
            self.users_id_unmute
        ]
