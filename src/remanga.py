from requests import Session


class Remanga:
    def __init__(self) -> None:
        self.api = "https://api.remanga.org/api"
        self.public_api = "https://remanga.org/api"
        self.user_id = None
        self.access_token = None
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"}

    def _post(self, endpoint: str, data: dict) -> dict:
        return self.session.post(f"{self.api}{endpoint}", json=data).json()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        return self.session.get(endpoint, params=params).json()

    def login(
            self,
            username: str,
            password: str) -> dict:
        data = {
            "user": username,
            "password": password,
        }
        response = self._post(
            f"{self.api}/users/login/", data)
        if "content" in response:
            self.user_id = response["content"]["id"]
            self.access_token = response["content"]["access_token"]
            self.session.headers["Authorization"] = f"Bearer {self.access_token}"
        return response

    def send_comment(
            self,
            text: str,
            title_id: int,
            is_pinned: bool = False,
            is_spoiler: bool = False) -> dict:
        data = {
            "is_pinned": is_pinned,
            "is_spoiler": is_spoiler,
            "text": text,
            "title": title_id
        }
        return self._post(
            f"{self.api}/activity/comments/?title_id={title_id}", data)

    def similar_titles(self, title: str) -> dict:
        return self._get(
            f"{self.api}/titles/{title}/similar/")

    def search_title(
            self,
            title: str,
            count: int = 5) -> dict:
        params - {
            "query": title,
            "count": count
        }
        return self._get(
            f"{self.api}/search", params)

    def search_publishers(
            self,
            username: str,
            page: int = 1,
            count: int = 10) -> dict:
        params - {
            "count": count,
            "field": "publishers",
            "page": page,
            "query": username
        }
        return self._get(
            f"{self.api}/search", params)

    def edit_profile(
            self,
            username: str = None,
            description: str = None,
            is_private: str = False,
            adult: int = 1,
            sex: int = 0,
            yaoi: int = 0,
            google_id: int = 0,
            is_two_factor_auth: bool = False) -> dict:
        data = {
            "adult": adult,
            "sex": sex,
            "yaoi": yaoi,
            "username": username,
            "description": description,
            "is_private": is_private,
            "google_id": google_id,
            "is_two_factor_auth": is_two_factor_auth
        }
        filtered_data = {
            key: value for key, value in data.items() if value is not None
        }
        return self.session.put(
            f"{self.public_api}/users/current/", data=filtered_data).json()

    def get_report_reasons(self) -> dict:
        return self._get(
            f"{self.api}/reports/?get=reasons&type=title")

    def send_report(
            self,
            message: str,
            reason: int,
            title_id: int,
            type: str = "title") -> dict:
        data = {
            "message": message,
            "reason": reason,
            "target": title_id,
            "type": type
        }
        return self._post(
            f"{self.api}/panel/api/reports/", data)

    def like_comment(
            self,
            comment_id: int,
            type: int = 0) -> dict:
        data = {
            "comment": comment_id,
            "type": type
        }
        return self._post(
            f"{self.api}/activity/votes/", data)

    def get_genres(self) -> dict:
        return self._get(
            f"{self.api}/forms/titles/?get=genres")

    def get_title_info(self, title: str) -> dict:
        return self._get(f"{self.api}/titles/{title}/")

    def get_title_chapters(self, branch_id: int) -> dict:
        return self._get(
            f"{self.api}/titles/chapters/?branch_id={branch_id}")

    def get_title_comments(
            self,
            title_id: int,
            page: int = 1,
            ordering: str = "-id") -> dict:
        return self._get(
            f"{self.api}/activity/comments/?title_id={title_id}&page={page}&ordering={ordering}")

    def get_user_info(self, user_id: str) -> dict:
        return self._get(f"{self.api}/users/{user_id}")

    def get_notifications(
            self,
            count: int = 30,
            page: int = 1,
            status: int = 0,
            type: int = 0) -> dict:
        return self._get(
            f"{self.api}/users/notifications/?count={count}&page={page}&status={status}&type={type}")

    def get_notifications_count(self) -> dict:
        return self._get(
            f"{self.api}/users/notifications/count/")

    def get_account_info(self) -> dict:
        return self._get(f"{self.api}/users/current/")

    def get_daily_top_titles(self, count: int = 5) -> dict:
        return self._get(
            f"{self.api}/titles/daily-top/?count={count}")

    def get_titles_last_chapters(
            self,
            page: int = 1,
            count: int = 5) -> dict:
        return self._get(
            f"{self.api}/titles/last-chapters/?page={page}&count={count}")

    def add_to_bookmarks(
            self,
            title_id: int,
            type: int) -> dict:
        """
        BOOKMARK-TYPES:
            0 - READING,
            1 - WILL READ,
            2 - HAS READ,
            3 - ABANDONED,
            4 - POSTPONED,
            5 - NOT INTERESTING
        """
        data = {
            "mangaId": title_id,
            "title": title_id,
            "type": type
        }
        return self._post(
            f"{self.api}/users/bookmarks/", data=data).json()

    def change_password(
            self,
            old_password: str,
            new_password: str) -> dict:
        data = {
            "old_password": old_password,
            "confirm_password": new_password,
            "password": new_password
        }
        return self.session.put(
            f"{self.api}/users/current/", data).json()

    def bill_promo_code(self, promo_code: str) -> dict:
        data = {
            "promo_code": promo_code
        }
        return self._post(
            f"{self.api}/billing/promo-codes/", data)

    def create_publishers(
            self,
            name: str,
            vk_url: str) -> dict:
        data = {
            "name": name,
            "vk": vk_url
        }
        return self._post(
            f"{self.api}/publishers/", data)

    def rate_title(
            self,
            title_id: int,
            rating: int = 10) -> dict:
        data = {
            "rating": rating,
            "title": title_id
        }
        return self._post(
            f"{self.api}/activity/ratings/", data)

    def like_chapter(
            self,
            chapter_id: int,
            type: int = 0) -> dict:
        data = {
            "chapter": chapter_id,
            "type": type
        }
        return self._post(
            f"{self.api}/activity/votes/", data)

    def get_categories(self) -> dict:
        return self._get(f"{self.api}/forms/titles/?get=categories")

    def get_age_limits(self) -> dict:
        return self._get(f"{self.api}/forms/titles/?get=age_limit")

    def get_types(self) -> dict:
        return self._get(f"{self.api}/forms/titles/?get=types")

    def get_statuses(self) -> dict:
        return self._get(f"{self.api}/forms/titles/?get=status")

    def get_user_bookmarks(
            self,
            type: int,
            user_id: int,
            page: int = 1) -> dict:
        return self._get(
            f"{self.api}/users/{user_id}/bookmarks/?ordering=-chapter_date&page={page}&type={type}")

    def get_user_history(
            self,
            user_id: int,
            page: int = 1) -> dict:
        return self._get(
            f"{self.api}/users/{user_id}/history/?page={page}")

    def get_social_notifications(
            self,
            count: int = 30,
            page: int = 1) -> dict:
        return self._get(
            f"{self.api}/users/notifications/?count={count}&page={page}&status=0&type=1")

    def get_important_notifications(
            self,
            count: int = 30,
            page: int = 1) -> dict:
        return self._get(
            f"{self.api}/users/notifications/?count={count}&page={page}&status=0&type=2")

    def reset_password(self, email: str) -> dict:
        data = {
            "email": email,
            "g-recaptcha-response": "WITHOUT_TOKEN"
        }
        return self._post(
            f"{self.api}/users/password-reset/", data)

    def get_billing_premium(self) -> dict:
        return self._get(f"{self.api}/billing/premium")

    def get_billing_charge(self) -> dict:
        return self._get(
            f"{self.api}/v2/billing/charge/")

    def create_billing(
            self,
            service: str,
            amount: int,
            currency: str = "RUB") -> dict:
        data = {
            "service": service,
            "sum": amount,
            "currency": currency
        }
        return self._post(
            f"{self.api}/v2/billing/charge/", data)

    def get_title_collections(self) -> dict:
        return self._get(
            f"{self.api}/v2/titles/collections/")

    def get_lightning_balance(self) -> dict:
        return self._get(
            f"{self.api}/v2/billing/lightning-balance/")

    def get_eventpoint_balance(self) -> dict:
        return self._get(
            f"{self.api}/v2/events/eventpoint-balance/")

    def get_current_battlepass(self) -> dict:
        return self._get(
            f"{self.api}/battlepass/current/preview/")

    def get_bans(
            self,
            count: int = 20,
            page: int = 20,
            ordering: str = "-date") -> dict:
        params = {
            "count": count,
            "page": page,
            "ordering": ordering
        }
        return self._get(
            f"{self.api}/v2/users/bans", params)

    def get_shop(
            self,
            count: int = 20,
            page: int = 1,
            is_event: bool = False,
            ordering: str = "cost",
            type: str = "avatar") -> dict:
        """
         TYPES:
            AVATAR,
            FRAME,
            WALLPAPER,
            THEME,
            PACK,
            DECKS
        """
        params = {
            "count": count,
            "page": page,
            "is_event": is_event,
            "ordering": ordering,
            "type": type
        }
        return self._get(
            f"{self.api}/v2/shop", params)

    def get_payments(self, ordering: str = "-date", page: int = 1) -> dict:
        params = {
            "ordering": ordering,
            "page": page
        }
        return self._get(
            f"{self.api}/v2/billing/users/payments",
            params=params).json()

    def comment_profile(self, user_id: int, text: str) -> dict:
        data = {
            "text": text,
            "profile": user_id
        }
        return self._post(
            f"{self.api}/v2/activity/comments/")

    def comment_post(self, post_id: int, text: str) -> dict:
        data = {
            "text": text,
            "post": post_id
        }
        return self._post(
            f"{self.api}/v2/activity/comments/")

    def get_forum_tags(self, count: int = 200, page: int = 1) -> None:
        params = {
            "count": count,
            "page": page
        }
        return self._get(
            f"{self.api}/v2/forum/tags", params)

    def get_forum_feed(
            self,
            count: int = 20,
            page: int = 1,
            week: bool = False,
            ordering: str = "-id") -> dict:
        params = {
            "count": count,
            "page": page,
            "week": week,
            "ordering": ordering
        }
        return self._get(
            f"{self.api}/v2/forum/search", params)

    def get_post_comments(self, post_id: int, page: int = 1) -> dict:
        params = {
            "post_id": post_id,
            "page": page
        }
        return self._get(
            f"{self.api}/v2/activity/comments", params)

    def create_post(
            self,
            header: str,
            text: str,
            tags: list[str],
            attachments: list[str] = None) -> dict:
        data = {
            "header": header,
            "text": text,
            "tags": tags,
            "author_user_id": 282600
        }
        if attachments:
            data["attachments"] = attachments
        return self._post(
            f"{self.api}/v2/forum/", data)

    def get_titles_top(
            self,
            count: int = 20,
            page: int = 1,
            period: str = "new",
            tag: str = "all") -> dict:
        params = {
            "count": count,
            "page": page,
            "period": period,
            "section": period,
            "tag": tag
        }
        return self._get(
            f"{self.api}/v2/titles/top/?=all", params)

    def get_users_top(
            self, ordering: str, page: int = 1) -> dict:
        params = {
            "ordering": ordering,
            "page": page
        }
        return self._get(
            f"{self.api}/v2/users/top", params)
