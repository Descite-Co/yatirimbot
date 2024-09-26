"""
This module contains utility functions for handling date and time conversions, as well as for generating textual and graphical representations of stock performance.

Functions included:
- Convert English month names to their Turkish equivalents.
- Retrieve stock movement emojis and descriptive text based on percentage changes.
- Get the current date and time in the Istanbul timezone.
"""

from datetime import datetime
import pytz


def get_turkish_month(month):
    """Convert English month name to Turkish.

    Args:
        month (str): The English name of the month.

    Returns:
        str: The corresponding Turkish name of the month.

    Raises:
        KeyError: If the provided month name is not valid.
    """
    return {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık",
    }[month]


def get_stock_emoji_and_text(change, single="false"):
    """Get the emoji and text for stocks depending on their change rate.

    Args:
        change (float): The percentage change of the stock.
        single (str): Optional; if "emoji" returns only the emoji,
                      if "text" returns only the text; defaults to "false".

    Returns:
        tuple: A tuple containing the emoji and text indicating stock movement
               if `single` is not "emoji" or "text".
        str: The emoji if `single` is "emoji".
        str: The text if `single` is "text".
    """
    emo = "📈" if change > 0 else "📉"
    text = "yükseldi" if change > 0 else "düştü"
    if single == "emoji":
        return emo
    if single == "text":
        return text
    return emo, text


def get_date():
    """Get the current date and time in Istanbul timezone.

    Returns:
        datetime: The current date and time in the Istanbul timezone.
    """
    timezone = pytz.timezone("Europe/Istanbul")
    today_date = datetime.now(timezone)
    return today_date
