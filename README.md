<h1>
  <img src="https://github.com/user-attachments/assets/e8f4d866-2d21-47ae-a3a9-eefecdf7a04e" width="28" style="vertical-align:middle;" />
  remanga.py
</h1>
<p align="center">
  <a href="https://t.me/forevayounger">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white" />
  </a>
</p>

> Web-API for [remanga.org](https://remanga.org) russian manga reading platform.

## Quick Start
```python
from remanga import Remanga

remanga = Remanga()
remanga.login(username="", password="")
```

---

## Authentication
| Method | Description |
|--------|-------------|
| `login(username, password)` | Login and store access token |
| `reset_password(email)` | Send a password reset email |
| `change_password(old_password, new_password)` | Change password |

---

## Titles
| Method | Description |
|--------|-------------|
| `search_title(title, count=5)` | Search manga by name |
| `get_title_info(title)` | Get full info by URL slug |
| `get_title_chapters(branch_id)` | Get all chapters for a branch |
| `get_title_comments(title_id, page=1, ordering="-id")` | Get paginated comments |
| `similar_titles(title)` | Get similar title recommendations |
| `get_daily_top_titles(count=5)` | Today's trending titles |
| `get_titles_last_chapters(page=1, count=5)` | Titles with recent chapter releases |
| `get_title_collections()` | Get curated title collections |
| `rate_title(title_id, rating=10)` | Rate a title (1–10) |
| `get_titles_top(count=20, page=1, period="new", tag="all")` | Get top titles by period and tag |

---

## Bookmarks
| Type | Meaning |
|------|---------|
| `0` | Reading |
| `1` | Will Read |
| `2` | Has Read |
| `3` | Abandoned |
| `4` | Postponed |
| `5` | Not Interesting |

| Method | Description |
|--------|-------------|
| `add_to_bookmarks(title_id, type)` | Add title to reading list |
| `get_user_bookmarks(type, user_id, page=1)` | Get user's bookmarks by type |

```python
remanga.add_to_bookmarks(title_id=123, type=0)  # Mark as "Reading"
```

---

## Comments & Votes
| Method | Description |
|--------|-------------|
| `send_comment(text, title_id, is_pinned=False, is_spoiler=False)` | Post a comment on a title |
| `like_comment(comment_id, type=0)` | Like/dislike a comment |
| `like_chapter(chapter_id, type=0)` | Like/dislike a chapter |
| `comment_profile(user_id, text)` | Post a comment on a user profile |
| `comment_post(post_id, text)` | Post a comment on a forum post |
| `get_post_comments(post_id, page=1)` | Get comments on a forum post |

---

## Forum
| Method | Description |
|--------|-------------|
| `get_forum_feed(count=20, page=1, week=False, ordering="-id")` | Get paginated forum posts |
| `get_forum_tags(count=200, page=1)` | Get all forum tags |
| `create_post(header, text, tags, attachments=None)` | Create a new forum post |

---

## User
| Method | Description |
|--------|-------------|
| `get_account_info()` | Get current user's account info |
| `get_user_info(user_id)` | Get public profile of any user |
| `get_user_history(user_id, page=1)` | Get reading history |
| `get_users_top(ordering, page=1)` | Get top users by ordering |
| `edit_profile(username, adult, sex, yaoi, ...)` | Update profile settings |
| `get_bans(count=20, page=20, ordering="-date")` | Get ban history |

---

## Notifications
| Method | Description |
|--------|-------------|
| `get_notifications(count=30, page=1, status=0, type=0)` | Get all notifications |
| `get_notifications_count()` | Get unread notifications count |
| `get_social_notifications(count=30, page=1)` | Social notifications only |
| `get_important_notifications(count=30, page=1)` | Important notifications only |

---

## Search & Filters
| Method | Description |
|--------|-------------|
| `search_publishers(username, page=1, count=10)` | Search publisher accounts |
| `get_genres()` | All available genres |
| `get_categories()` | All available categories |
| `get_types()` | All title types (manga, manhwa, etc.) |
| `get_statuses()` | All title statuses |
| `get_age_limits()` | All age limit options |

---

## Reports & Publishers
| Method | Description |
|--------|-------------|
| `get_report_reasons()` | Fetch available report reason IDs |
| `send_report(message, reason, title_id, type="title")` | Submit a report |
| `create_publishers(name, vk_url)` | Register a publisher profile |

---

## Billing & Shop
| Method | Description |
|--------|-------------|
| `bill_promo_code(promo_code)` | Apply a promo code |
| `get_billing_premium()` | Get premium billing info |
| `get_billing_charge()` | Get current billing charge options |
| `create_billing(service, amount, currency="RUB")` | Create a billing transaction |
| `get_payments(ordering="-date", page=1)` | Get billing payment history |
| `get_lightning_balance()` | Get lightning coin balance |
| `get_eventpoint_balance()` | Get event point balance |
| `get_current_battlepass()` | Get current battlepass info |
| `get_shop(count=20, page=1, is_event=False, ordering="cost", type="avatar")` | Browse the shop |

**Shop types:** `avatar`, `frame`, `wallpaper`, `theme`, `pack`, `decks`

---

> **Note:** Authentication is required for all write operations. All methods return a Python `dict`.
