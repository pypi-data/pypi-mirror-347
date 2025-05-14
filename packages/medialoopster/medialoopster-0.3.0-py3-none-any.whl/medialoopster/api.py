import time
import logging
from enum import Enum
from typing import List
from urllib.parse import urlparse, parse_qs, urljoin, urlencode

from requests import Session
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
from pydantic import TypeAdapter, HttpUrl

from medialoopster.exceptions import MedialoopsterError
from medialoopster.schemas import Production, Sequence, Shot

logger = logging.getLogger(__name__)


class Medialoopster:
    """
    Client for the medialoopster API.

    This class provides methods to interact with the medialoopster Media Asset Management System API.
    """

    class AssetType(str, Enum):
        """Enum of supported asset types in medialoopster."""
        VIDEOASSETS = "videoassets"
        IMAGEASSETS = "imageassets"
        AUDIOASSETS = "audioassets"
        PROJECTASSETS = "projectassets"

    def __init__(self, url: str, username: str, password: str, verify: bool = True):
        """
        Initialize a new medialoopster API client.

        Args:
            url: The base URL of the medialoopster API
            username: Username for authentication
            password: Password for authentication
            verify: Whether to verify SSL certificates (default: True)
        """
        self.session = Session()
        self.session.verify = verify

        if all([username, password]):
            self.session.auth = HTTPBasicAuth(username, password)

        self.url = url

    def __enter__(self):
        """Enable context management."""
        return self

    def __exit__(self, *args):
        """Clean up."""
        self.session.close()

    def _build_url(
            self,
            url: str | None = None,
            path: str | None = None,
            params: dict | None = None
    ) -> HttpUrl:
        """
        Build a URL for API requests.

        This method handles URL construction with proper path joining and query parameters.

        Args:
            url: Base URL (defaults to self.url if not provided)
            path: API endpoint path to append to the base URL
            params: Query parameters to include in the URL

        Returns:
            Complete URL with path and query parameters
        """
        url = url if url else self.url
        url = url if url.endswith('/') else f"{url}/"
        url = urljoin(url, url=f"{path}/") if path else url
        parsed_url = urlparse(url)

        query_params = parse_qs(parsed_url.query)
        query_params = query_params | params if params else query_params
        query = urlencode(query_params, doseq=True)

        return urljoin(url, url=f"{parsed_url.path}?{query}")

    def ping(self) -> bool:
        """
        Check if the medialoopster API is reachable.

        This method attempts to connect to the API's ping endpoint to verify connectivity.

        Returns:
            True if the API is reachable, False otherwise
        """
        url = self._build_url(path="ping")
        try:
            response = self.session.get(url=url)
            response.raise_for_status()
        except RequestException:
            return False

        return True

    def asset_import(
            self,
            production=None,
            asset_type=None,
            move_asset=False,
            name=None,
            description=None,
            approval=0,
            path_file=None,
            meta_field_store=None
    ):
        url = self._build_url(path="asset/import")

        request = {
            "production": production,
            "type": asset_type,
            "move_asset": move_asset,
            "asset": {
                "asset_meta": {
                    "name": name,
                    "description": description,
                    "approval": approval,
                    "path_file": path_file,
                    "meta_field_store": meta_field_store or {}
                }
            }
        }

        response = self.session.post(url=url, json=request)
        response.raise_for_status()

        response_json = response.json()

        return response_json.get("asset_import_id", None)

    def get_from_api(
            self,
            path="videoassets",
            url=None,
            production_id=None,
            is_archive=None,
            is_production=None,
            max_retries=3,
    ):
        """
        Generator that fetches data from the API with pagination support.

        Args:
            path: API endpoint path
            url: Full URL (overrides path if provided)
            production_id: Filter by production ID
            is_archive: Filter by archive status
            is_production: Filter by production status
            max_retries: Maximum number of retry attempts per request

        Yields:
            Items from the API response

        Raises:
            MedialoopsterError: If connection fails after max_retries
        """
        if url is None:
            url_params = {}

            if is_archive is not None:
                url_params["is_archive"] = "true" if is_archive else "false"
            if is_production is not None:
                url_params["is_production"] = "true" if is_production else "false"
            if production_id is not None:
                url_params["production"] = production_id

            url = self._build_url(path=path, params=url_params)

        while url:
            for retry in range(max_retries):
                try:
                    response = self.session.get(url=url)
                    response.raise_for_status()
                    break
                except RequestException as e:
                    if retry == max_retries - 1:
                        logger.error(f"Failed to fetch data from {url} after {max_retries} attempts")
                        raise MedialoopsterError(f"Failed to connect to API: {str(e)}") from e
                    logger.warning(f"Retry {retry + 1}/{max_retries} for {url}")
                    time.sleep(1)  # Add a small delay between retries
            else:
                # This will only execute if the for loop completes without a break
                # (which shouldn't happen due to the raise in the exception handler)
                break

            if response.links is not None:
                url = response.links.get("next", {}).get("url", None)
            else:
                url = None

            yield from response.json()

    def get_videoassets(self, production_id=None, is_archive=None, is_production=None):
        return self.get_from_api(
            path="videoassets",
            production_id=production_id,
            is_archive=is_archive,
            is_production=is_production,
        )

    def get_videoassets_count(self) -> int:
        url = self._build_url(path="videoassets")

        try:
            response = self.session.get(url=url)
            response.raise_for_status()
        except RequestException:
            raise MedialoopsterError

        return int(response.headers.get("X-Total-Count"))

    def get_videoasset_sequences(self, asset_id) -> List[Sequence]:
        url = self._build_url(path=f"videoassets/{asset_id}/sequences")

        try:
            response = self.session.get(url=url, timeout=60)
            response.raise_for_status()
        except RequestException:
            raise MedialoopsterError

        return TypeAdapter(List[Sequence]).validate_python(response.json())

    def get_videoasset_shots(self, asset_id) -> List[Shot]:
        url = self._build_url(path=f"videoassets/{asset_id}/shots")

        try:
            response = self.session.get(url=url, timeout=60)
            response.raise_for_status()
        except RequestException:
            raise MedialoopsterError

        return TypeAdapter(List[Shot]).validate_python(response.json())

    def get_asset(self, asset_id=None, asset_type="videoassets", path_file=None):
        if asset_id is not None:
            url = self._build_url(path=f"{asset_type}/{asset_id}")
        elif path_file is not None:
            url = self._build_url(path=f"{asset_type}", params={"path_file": path_file})

        try:
            response = self.session.get(url=url)  # ToDo: Refactoring needed
            response.raise_for_status()
        except RequestException:
            raise MedialoopsterError

        return response.json()

    def search_meta_field_store(self, field: str = None, value: str = None, asset_type: str = "videoassets"):
        """
        Search for assets with a specific value in a meta-field.

        Args:
            field: The meta field name to search in
            value: The value to search for
            asset_type: The type of asset to search in

        Returns:
            List of asset IDs that match the search criteria
        """
        assets = []

        for asset in self.get_from_api(path=asset_type):
            meta_field_store = asset.get("meta_field_store")
            if meta_field_store is not None:
                field_value = meta_field_store.get(field)
                if field_value is not None and field_value == value:
                    assets.append(asset.get("id"))

        return assets

    def archiv_asset(self, content_type_id, asset_id, archive_type, archive_connector):
        url = self._build_url(path="archiveactivities")

        request = [{
            "content_type_id": content_type_id,
            "asset_id": asset_id,
            "archive_type": archive_type,
            "archive_connector": archive_connector,
        }]

        response = self.session.post(url, json=request)
        response.raise_for_status()

        return response.json()

    def restore_asset(self, content_type_id, asset_id):
        url = self._build_url(path="restoreactivities")

        request = [{
            "content_type_id": content_type_id,
            "asset_id": asset_id,
        }]

        response = self.session.post(url, json=request)
        response.raise_for_status()

        return response.json()

    def wait_is_production(self, asset_id, timeout=3600, sleep=30):
        timeout = time.time() + timeout  # timeout in seconds from now
        is_production = False

        while time.time() < timeout:
            try:
                asset = self.get_asset(asset_id=asset_id)
                is_production = asset.get("is_production")

                if is_production:
                    break
            except Exception:
                logger.exception("Error in wait_is_production")

            time.sleep(sleep)  # sleep in seconds

        return is_production

    def disapprove_asset(self, asset_id, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            "status_approval": 0
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def approve_asset(self, asset_id, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            "status_approval": 1
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def delete_asset(self, asset_id, asset_type="videoassets", allow_partial=False):
        url_params = {"allow_partial": "true"} if allow_partial else {}
        url = self._build_url(path=f"{asset_type}/{asset_id}/", params=url_params)

        response = self.session.delete(url)
        response.raise_for_status()

        return True

    def set_date_del_asset(self, asset_id, date_del, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            "date_del": date_del
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def set_date_add_asset(self, asset_id, date_add, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            "date_add": date_add
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def edit_asset(self, asset_id, field: str, value: str | int, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            field: value
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def edit_meta_field_store(self, asset_id, meta_field_store, asset_type="videoassets"):
        url = self._build_url(path=f"{asset_type}/{asset_id}")

        request = {
            "meta_field_store": meta_field_store
        }

        response = self.session.patch(url, json=request)
        response.raise_for_status()

        return response.json()

    def productions(self) -> List[Production]:
        url = self._build_url(path="productions")

        response = self.session.get(url)
        response.raise_for_status()

        return TypeAdapter(List[Production]).validate_python(response.json())

    def production(self, production_id: int | None = None, production_name: str | None = None) -> Production | None:
        if production_id is not None:
            url = self._build_url(path=f"productions/{production_id}")

            response = self.session.get(url)
            response.raise_for_status()

            return Production.model_validate(response.json())
        elif production_name is not None:
            productions = self.productions()
            return next((production for production in productions if production.name == production_name), None)
        else:
            return None
