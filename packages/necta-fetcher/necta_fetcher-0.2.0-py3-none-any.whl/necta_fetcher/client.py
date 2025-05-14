# necta_fetcher/client.py
import requests
from bs4 import BeautifulSoup
from .exceptions import (
    NectaLoginError, NectaTokenError, NectaRequestError,
    NectaResultError, NectaStudentNotFoundError
)

class NectaClient:
    """
    A client to fetch NECTA results programmatically.
    Note: This version hardcodes login credentials.
    """
    LOGIN_URL = "https://ajira.zimamoto.go.tz/login"
    TOKEN_UPDATE_URL = "https://ajira.zimamoto.go.tz" # Page to fetch for updating action tokens
    RESULTS_API_URL = "https://ajira.zimamoto.go.tz/candidates/nectaResult"

    # --- Hardcoded Credentials ---
    # WARNING: Hardcoding credentials is not recommended for production or shared code.
    # This is done as per specific request for this version.
    DEFAULT_EMAIL = "adosomeless@gmail.com"
    DEFAULT_PASSWORD = "Someless11"
    # --- End of Hardcoded Credentials ---

    def __init__(self, email=None, password=None, user_agent=None):
        self.email = email or self.DEFAULT_EMAIL
        self.password = password or self.DEFAULT_PASSWORD
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (compatible; NectaFetcherPackage/0.1.0)'
        })
        self._is_logged_in = False
        self._action_csrf_token = None # CSRF token for POST actions after login

    def _perform_login(self):
        """Handles the login process."""
        if self._is_logged_in:
            return True

        print("Attempting to log in to NECTA portal...")
        try:
            login_page_resp = self.session.get(self.LOGIN_URL, timeout=10)
            login_page_resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise NectaLoginError(f"Error fetching login page: {e}")

        soup = BeautifulSoup(login_page_resp.text, 'html.parser')
        login_token_input = soup.find("input", {"name": "_token"})
        if not login_token_input or not login_token_input.get("value"):
            raise NectaTokenError("Failed to retrieve CSRF token from login page.")
        
        login_csrf_token = login_token_input.get("value")

        login_payload = {
            "email": self.email,
            "password": self.password,
            "_token": login_csrf_token
        }

        try:
            response = self.session.post(self.LOGIN_URL, data=login_payload, timeout=15)
            response.raise_for_status()
            # A more robust check for successful login (e.g., check response.url or content)
            if "dashboard" in response.url.lower() or self.LOGIN_URL not in response.url:
                self._is_logged_in = True
                print("Login successful.")
                # Immediately update tokens needed for subsequent actions
                if not self._refresh_action_token():
                    # If token refresh fails right after login, treat login as incomplete for actions
                    self._is_logged_in = False
                    raise NectaTokenError("Login succeeded but failed to refresh action CSRF token.")
                return True
            else:
                soup_fail = BeautifulSoup(response.text, 'html.parser')
                error_div = soup_fail.find('div', class_='alert-danger')
                error_msg = f"Login failed: {error_div.get_text(strip=True)}" if error_div else "Login failed. Credentials may be incorrect or page structure changed."
                raise NectaLoginError(error_msg)
        except requests.exceptions.RequestException as e:
            raise NectaLoginError(f"Login request failed: {e}")

    def _refresh_action_token(self):
        """
        Refreshes the CSRF token used for POST actions by visiting an authenticated page.
        This token might be different from the login page's CSRF.
        """
        if not self._is_logged_in: # Should not happen if called right after successful _perform_login
             raise NectaLoginError("Cannot refresh action token, not logged in.")

        print("Refreshing action CSRF token...")
        try:
            resp = self.session.get(self.TOKEN_UPDATE_URL, timeout=10)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise NectaTokenError(f"Error fetching page to refresh action token: {e}")

        soup = BeautifulSoup(resp.text, 'html.parser')
        token_input = soup.find("input", {"name": "_token"}) # Common location for action tokens
        if token_input and token_input.get("value"):
            self._action_csrf_token = token_input.get("value")
            print("Action CSRF token updated.")
            return True
        else:
            # Fallback: Check meta tag if common for the site
            meta_tag = soup.find("meta", {"name": "csrf-token"})
            if meta_tag and meta_tag.get("content"):
                self._action_csrf_token = meta_tag.get("content")
                print("Action CSRF token updated from meta tag.")
                return True
            
        self._action_csrf_token = None # Explicitly set to None if not found
        print("Warning: Could not find a new action CSRF token (_token input or meta tag). Subsequent actions might fail.")
        return False # Indicate failure to refresh

    def fetch_student_results(self, index_string: str, year: str, exam_level: str):
        """
        Fetches results for a specific student using their full index number.

        :param index_string: The student's full index number (e.g., "S1143-0100").
        :param year: The year of examination (e.g., "2022").
        :param exam_level: The level of examination (e.g., "CSEE", "ACSEE").
        :return: A dictionary containing the student's results.
        :raises NectaError and its subclasses on failure.
        """
        if not self._is_logged_in:
            self._perform_login() # This will raise NectaLoginError or NectaTokenError on failure

        if not self._action_csrf_token:
            # Attempt to refresh if it's missing, could be a stale session
            print("Action CSRF token missing, attempting refresh...")
            if not self._refresh_action_token() or not self._action_csrf_token:
                raise NectaTokenError("Required action CSRF token is not available. Please try re-login or check token refresh logic.")

        payload = {
            "year": str(year),
            "number": index_string,  # API accepts full index number here
            "level": exam_level,
            "_token": self._action_csrf_token
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        
        # XSRF-TOKEN cookie is often sent as a header by browsers if present
        xsrf_cookie = self.session.cookies.get('XSRF-TOKEN')
        if xsrf_cookie:
            headers["X-XSRF-TOKEN"] = xsrf_cookie

        print(f"Fetching results for {index_string}, Year: {year}, Level: {exam_level}...")
        try:
            response = self.session.post(self.RESULTS_API_URL, data=payload, headers=headers, timeout=30)
            response.raise_for_status() # Raises HTTPError for 4xx/5xx responses
        except requests.exceptions.HTTPError as e:
            # Try to get more details from API's JSON error response
            try:
                error_details = e.response.json()
                msg = error_details.get("message", str(e))
                if "not found" in msg.lower() or e.response.status_code == 404:
                    raise NectaStudentNotFoundError(f"API Error for {index_string}: {msg} (Status: {e.response.status_code})")
                raise NectaResultError(f"API HTTP Error for {index_string}: {msg} (Status: {e.response.status_code})")
            except ValueError: # If error response is not JSON
                raise NectaRequestError(f"HTTP Error {e.response.status_code} for {index_string}. Response: {e.response.text[:200]}")
        except requests.exceptions.RequestException as e:
            raise NectaRequestError(f"Network or request error for {index_string}: {e}")

        try:
            api_response_json = response.json()
        except ValueError: # JSONDecodeError
            raise NectaResultError(f"Invalid JSON response for {index_string}. Content: {response.text[:500]}")

        if api_response_json.get("success") is True and "data" in api_response_json:
            student_data = api_response_json["data"]
            # Verify it's the actual student and not a placeholder
            if isinstance(student_data, dict) and \
               (student_data.get("index_number", "").upper() == index_string.upper() or \
                student_data.get("regno", "").upper() == index_string.upper()): # Check 'regno' too
                
                if str(student_data.get("first_name", "")).upper() == "N/A" and \
                   not student_data.get("subjects"): # Likely a placeholder
                    raise NectaStudentNotFoundError(
                        f"Student {index_string} query returned placeholder 'N/A' data. Results not found."
                    )
                return student_data # Actual student data
            else:
                # Data structure is unexpected for a specific student query that succeeded
                raise NectaResultError(f"API success for {index_string}, but 'data' field is not the expected student structure or index mismatch. Data: {str(student_data)[:200]}")

        elif api_response_json.get("success") is False:
            error_message = api_response_json.get("message", "API returned success=false without a message.")
            if "not found" in error_message.lower():
                 raise NectaStudentNotFoundError(f"Student {index_string} not found: {error_message}")
            raise NectaResultError(f"API error for {index_string}: {error_message}")
        else:
            raise NectaResultError(f"Unexpected API response structure for {index_string}. Response: {str(api_response_json)[:500]}")