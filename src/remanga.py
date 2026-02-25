from requests import Session

class Remanga:
	def __init__(self) -> None:
		self.api = "https://api.remanga.org"
		self.recaptcha_api = "https://www.google.com/recaptcha/api2"
		self.user_id = None
		self.access_token = None
		self.session = Session()
		self.session.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
		}

	def generate_captcha(
			self,
			hl: str = "en",
			vh: int = 171805507,
			cb: str = "x8tfd89z6xpn",
			size: str = "invisible",
			chr: str = "[88,91,94]",
			v: str = "PRMRaAwB3KlylGQR57Dyk-pF",
			key: str = "6LdGNc8UAAAAAOi7mZdoujfQ0s-zHexDM8AWyB1J",
			co: str = "aHR0cHM6Ly9uZXh0LnJlbWFuZ2Eub3JnOjQ0Mw..",
			bg: str = "!u72gvbgKAAQeG9ujbQEHDwNQThjPgVnP7bQGfGtLFTSQ9q7PRWq4Mo6wTK1hF6mTmob321ueoFddZBgl3CNxklbmAd_8x8YxYDs5QrjL7dUsYncpMGmkgC7zGhUD0BwVc3v8cz2Bpap3IHwTDlUSNRYp9EyzZ3WTmkn72WjZixVOb5MJrD7nfwq2T8c8XaIINt60LWpEgRbduOLUxBAynNNCbWdx4R_dhxK7wkXMFMv34aAr9Q8Kj7BGQqoXIU4Ipj_fUd_cuXF4AdbcCERBSRyELilo5WyMkx3yZA_SdwkCg1Dq9JvAHKlhw5nSl49hjcLvBdppQxiX40G_7-wW8f1yOHrBCCut2YB7fGS6TzqRroQhmwufQeuleX1aWRIX-gmXhVdv2-NscuqGbMCugcxXC6GIJK_E3I4fkr5TT6_J4KnmjJLIB23LVrax3N2Da7QXpEq6PhA1WGLrCKxdzONe46StOcc-tKK_zlbg2UCLm0GPV_Ai1qmKKipyCErtZIE4nuqUxbHddY6DUQ_a7tWEA_yDT5Y9txb5XdsdtpLPOULrzElUGyHDKD51acbNfw6sUk5c33LZl20XMJc9sTFSitCX_B1lTMyR63g6FMeZGcFshiVb8-kFdwSlphiiJRTc4hruXo-PtQKM1ZnU0mL2HfQ8D20qDrQIkRI2mMs8QV6vX0zhbCFQ4r6HMdKQQgvlPdox3JjwmXMdVX1jV_wx3JWObthRfEXocF39Km-hQYC-TP06Biej705zlTtXVQ5v5sMgDzBAfYP0sDUr9cjYplzKZ6rkxpCc3BOF1K2Tkfy4JN1mm5l9RpcayJHQyOlCBH_DsTbxqdTESD8uwSGZeTn7uEytRv3-AHA98Qr-gexjL1kEu4ZJBwFHfNIZTP2HSz8Wadvvtc-8pzkn74xljxgvhlbzl9tgshMv5mqicfwSv6rxKy0VWKLk66PwSRsNQM1y77SLQ3c3b73tpv7-c9MgyinRnc-SuxKOdPJLVUiXxd4hhcz7g1fyLSh_LaskcEMTWPKm_uAKHUPy1d7UerHiUc31CdFQaEi6X-knv_d2wVeQtYQhb0WKwfVPNLtbRhbZeMSFtzJWVpwvLq3pyWBvBcVxfvhmCLFAyRcalZLhcRoqXeLorrrwq6mBqBKcAEaCJSJCY7wmqzJbvhTimQGmw1GsPo5rfTeXVfEyJ8TBFTVcAETA_Cl6ea0QWEErqn22tv5EXs7tLRdbYr0jIX3ObDYfJoEq*") -> str:
		parameters = (
			f"v={v}&reason=q&c=<token>&k={key}&co={co}"
			f"&hl={hl}&size={size}&chr={chr}&vh={vh}&bg={bg}"
		)
		params = {
			"ar": 1,
			"k": key,
			"co": co,
			"hl": hl,
			"v": v,
			"size": size,
			"cb": cb
		}
		anchor = self.session.get(
			f"{self.recaptcha_api}/anchor", params=params).text
		recaptcha_token = anchor.split('recaptcha-token" value="')[1].split('">')[0]
		data = parameters.replace("<token>", recaptcha_token)
		self.session.headers["Content-Type"] = "application/x-www-form-urlencoded"
		response = self.session.post(
			f"{self.recaptcha_api}/reload?k={key}", data=data).text
		return response.split(
			'"rresp","')[1].split('"')[0] if "rresp" in response else response

	def login(
			self,
			username: str,
			password: str) -> dict:
		data = {
			"user": username,
			"password": password,
			"g-recaptcha-response": self.generate_captcha()
		}
		response = self.session.post(
			f"{self.api}/api/users/login/", data=data).json()			
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
		return self.session.post(
			f"{self.api}/api/activity/comments/?title_id={title_id}",
			data=data).json()

	def logging(self, path_name: str = "/") -> dict:
		data = {
			"user": self.user_id,
			"access_token": self.access_token,
			"msg": "CONSOLE",
			"location": {
				"pathname": path_name,
				"search": "",
				"hash": "",
				"key": ""
			},
			"deviceType": "desktop",
			"appVersion": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
			"userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
		}
		return self.session.post(
			f"{self.api}/api/logging/",
			data=data).json()

	def similar_titles(self, title: str) -> dict:
		return self.session.get(
			f"{self.api}/api/titles/{title}/similar/").json()

	def search_title(
			self,
			title: str,
			count: int = 5) -> dict:
		return self.session.get(
			f"{self.api}/api/search/?query={title}&count={count}").json()

	def search_publishers(
			self,
			username: str,
			page: int = 1,
			count: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/api/search/?count={count}&field=publishers&page={page}&query={username}").json()

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
		return self.session.put(
			f"{self.api}/api/users/current/", data=data).json()

	def get_report_reasons(self) -> dict:
		return self.session.get(
			f"{self.api}/api/reports/?get=reasons&type=title").json()

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
		return self.session.post(
			f"{self.api}/panel/api/reports/", data=data).json()

	def like_comment(
			self,
			comment_id: int,
			type: int = 0) -> dict:
		data = {
			"comment": comment_id,
			"type": type
		}
		return self.session.post(
			f"{self.api}/api/activity/votes/", data=data).json()

	def get_genres(self) -> dict:
		return self.session.get(
			f"{self.api}/api/forms/titles/?get=genres").json()

	def get_title_info(self, title: str) -> dict:
		return self.session.get(f"{self.api}/api/titles/{title}/").json()

	def get_title_chapters(self, branch_id: int) -> dict:
		return self.session.get(
			f"{self.api}/api/titles/chapters/?branch_id={branch_id}").json()

	def get_title_comments(
			self,
			title_id: int,
			page: int = 1,
			ordering: str = "-id") -> dict:
		return self.session.get(
			f"{self.api}/api/activity/comments/?title_id={title_id}&page={page}&ordering={ordering}").json()

	def get_user_info(self, user_id: str) -> dict:
		return self.session.get(f"{self.api}/api/users/{user_id}").json()

	def get_notifications(
			self,
			count: int = 30,
			page: int = 1,
			status: int = 0,
			type: int = 0) -> dict:
		return self.session.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status={status}&type={type}").json()

	def get_notifications_count(self) -> dict:
		return self.session.get(
			f"{self.api}/api/users/notifications/count/").json()

	def get_account_info(self) -> dict:
		return self.session.get(f"{self.api}/api/users/current/").json()

	def get_daily_top_titles(self, count: int = 5) -> dict:
		return self.session.get(
			f"{self.api}/api/titles/daily-top/?count={count}").json()

	def get_titles_last_chapters(
			self,
			page: int = 1,
			count: int = 5) -> dict:
		return self.session.get(
			f"{self.api}/api/titles/last-chapters/?page={page}&count={count}").json()

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
		return self.session.post(
			f"{self.api}/api/users/bookmarks/",data=data).json()

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
			f"{self.api}/api/users/current/", data=data).json()

	def bill_promo_code(self, promo_code: str) -> dict:
		data = {
			"promo_code": promo_code
		}
		return self.session.post(
			f"{self.api}/api/billing/promo-codes/", data=data).json()

	def create_publishers(
			self,
			name: str,
			vk_url: str) -> dict:
		data = {
			"name": name,
			"vk": vk_url
		}
		return self.session.post(
			f"{self.api}/api/publishers/", data=data).json()

	def rate_title(
			self,
			title_id: int,
			rating: int = 10) -> dict:
		data = {
			"rating": rating,
			"title": title_id
		}
		return self.session.post(
			f"{self.api}/api/activity/ratings/", data=data).json()

	def like_chapter(
			self,
			chapter_id: int,
			type: int = 0) -> dict:
		data = {
			"chapter": chapter_id,
			"type": type
		}
		return self.session.post(
			f"{self.api}/api/activity/votes/", data=data).json()

	def get_categories(self) -> dict:
		return self.session.get(f"{self.api}/api/forms/titles/?get=categories").json()

	def get_age_limits(self) -> dict:
		return self.session.get(f"{self.api}/api/forms/titles/?get=age_limit").json()

	def get_types(self) -> dict:
		return self.session.get(f"{self.api}/api/forms/titles/?get=types").json()

	def get_statuses(self) -> dict:
		return self.session.get(f"{self.api}/api/forms/titles/?get=status").json()

	def get_user_bookmarks(
			self,
			type: int,
			user_id: int,
			page: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/api/users/{user_id}/bookmarks/?ordering=-chapter_date&page={page}&type={type}").json()

	def get_user_history(
			self,
			user_id: int,
			page: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/api/users/{user_id}/history/?page={page}").json()

	def get_social_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=1").json()

	def get_important_notifications(
			self,
			count: int = 30,
			page: int = 1) -> dict:
		return self.session.get(
			f"{self.api}/api/users/notifications/?count={count}&page={page}&status=0&type=2").json()
