from requests import session

class Recomics:
	def __init__(self) -> None:
		self.api = "https://api.recomics.org"
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
		}
		self.user_id = None
		self.access_token = None

	def _post(self, endpoint: str, data: dict) -> dict:
		return self.session.post(f"{self.api}{endpoint}", json=data).json()

	def _get(self, endpoint: str, params: dict = None) -> dict:
		return self.session.get(f"{self.api}{endpoint}", params=params).json()

	def _put(self, endpoint: str, data: dict) -> dict:
		return self.session.put(f"{self.api}{endpoint}", data=data).json()

	def login(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"user": username,
			"password": password,
			"g-recaptcha-response": self.generate_captcha()
		}
		response = self._post("/api/users/login/", data)
		if "content" in response:
			self.user_id = response["content"]["id"]
			self.access_token = response["content"]["access_token"]
			self.headers["authorization"] = f"bearer {self.access_token}"
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
			f"/api/activity/comments/?title_id={title_id}", data)

	def similar_titles(self, title: str) -> dict:
		return self._get(
			f"/api/titles/{title}/similar/")

	def search_title(
			self,
			query: str,
			count: int = 5) -> dict:
		params = {
			"query": query,
			"count": count
		}
		return self._get("/api/search", params)

	def search_publishers(
			self,
			query: str,
			page: int = 1,
			count: int = 10) -> dict:
		params = {
			"count": count,
			"field": "publishers",
			"page": page,
			"query": query
		}
		return self._get("/api/search", params)

	def edit_profile(
			self,
			username: str = None,
			adult: bool = False,
			sex: int = 0,
			yaoi: int = 0) -> dict:
		data = {
			"adult": adult,
			"sex": sex,
			"yaoi": yaoi
		}
		if username:
			data["username"] = username
		return self._put("/api/users/current/", data)

	def get_report_reasons(self) -> dict:
		params = {
			"get": "reasons",
			"type": "title"
		}
		return self._get("/api/reports/", params)

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
		return self._post("/panel/api/reports/", data)

	def like_comment(
			self,
			comment_id: int,
			type: int = 0) -> dict:
		data = {
			"comment": comment_id,
			"type": type
		}
		return self._post("/api/activity/votes/", data)

	def get_genres(self) -> dict:
		params = {
			"get": "genres"
		}
		return self._get("/api/forms/titles/", params)

	def get_title_info(self, title: str) -> dict:
		return self._get(f"/api/titles/{title}/")

	def get_title_chapters(self, branch_id: int) -> dict:
		params = {
			"branch_id": branch_id
		}
		return self._get("/api/titles/chapters/", params)

	def get_title_comments(
			self,
			title_id: int,
			page: int = 1,
			ordering: str = "-id") -> dict:
		data = {
			"title_id": title_id,
			"page": page,
			"ordering": ordering
		}
		return self._get("/api/activity/comments/", params)

	def get_user_info(self, user_id: str) -> dict:
		return self._get(f"/api/users/{user_id}")

	def get_notifications(
			self,
			count: int = 30,
			page: int = 1,
			status: int = 0,
			type: int = 0) -> dict:
		params = {
			"count": count,
			"page": page,
			"status": status,
			"type": type
		}
		return self._get("/api/users/notifications/", params)

	def get_notifications_count(self) -> dict:
		return self._get("/api/users/notifications/count/")

	def get_account_info(self) -> dict:
		return self._get("/api/users/current/")

	def get_daily_top_titles(self, count: int = 5) -> dict:
		params = {
			"count": count
		}
		return self._get(
			"/api/titles/daily-top/", params)

	def get_titles_last_chapters(
			self,
			page: int = 1,
			count: int = 5) -> dict:
		params = {
			"page": page,
			"count": count
		}
		return self._get(
			"/api/titles/last-chapters/", params)

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
		return self._post("/api/users/bookmarks/", data)

	def change_password(
			self,
			old_password: str,
			new_password: str) -> dict:
		data = {
			"old_password": old_password,
			"confirm_password": new_password,
			"password": new_password
		}
		return self._put("/api/users/current/", data)

	def bill_promo_code(self, promo_code: str) -> dict:
		data = {
			"promo_code": promo_code
		}
		return self._post("/api/billing/promo-codes/", data)

	def create_publishers(
			self,
			name: str,
			vk_url: str) -> dict:
		data = {
			"name": name,
			"vk": vk_url
		}
		return self._post("/api/publishers/", data)

	def rate_title(
			self,
			title_id: int,
			rating: int = 10) -> dict:
		data = {
			"rating": rating,
			"title": title_id
		}
		return self._post("/api/activity/ratings/", data)

	def like_chapter(
			self,
			chapter_id: int,
			type: int = 0) -> dict:
		data = {
			"chapter": chapter_id,
			"type": type
		}
		return self._post(
			"/api/activity/votes/", data)

	def get_categories(self) -> dict:
		params = {
			"get": "categories"
		}
		return self._get(
			"/api/forms/titles/", params)

	def get_age_limits(self) -> dict:
		params = {
			"get": "age_limit"
		}
		return self._get(
			"/api/forms/titles/", params)

	def get_types(self) -> dict:
		params = {
			"get": "types"
		}
		return self._get(
			"/api/forms/titles/", params)

	def get_statuses(self) -> dict:
		params = {
			"get": "statys"
		}
		return self._get(
			"/api/forms/titles/", params)

	def get_user_bookmarks(
			self,
			type: int,
			user_id: int,
			page: int = 1) -> dict:
		params = {
			"ordering": "chapter-date",
			"page": page,
			"type": type
		}
		return self._get(
			f"/api/users/{user_id}/bookmarks/", params)

	def get_user_history(
			self,
			user_id: int,
			page: int = 1) -> dict:
		params = {
			"page": page
		}
		return self._get(
			f"/api/users/{user_id}/history", params)

	def get_social_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		params = {
			"count": count,
			"page": page,
			"status": 0,
			"type": 1
		}
		return self._get(
			"/api/users/notifications/", params)

	def get_important_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		params = {
			"count": count,
			"page": page,
			"status": 0,
			"type": 2
		}
		return self._get(
			f"/api/users/notifications/", params)
