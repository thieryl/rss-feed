#!/usr/bin/python3
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import feedparser

db_connection = sqlite3.connect('rss_feed.db')
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS magazine(title TEXT, date TEXT)')


def article_not_in_db(article_title, article_date):
    """ Checks is a givenn pair or article title and
        date is in the database
    Args:
        article_title (str) : the title of the article
        article_date  (str) : the publication date of an article
    Returns:
        True if the article is not in the database
        False if the article is in the database
    """

    db.execute("SELECT * FROM magazine WHERE title=? and date=?",
               (article_title, article_date))

    if not db.fetchall():
        return True
    else:
        return False


def add_article_to_database(article_title, article_date):
    """ Add a new article title and date to the database
        Args:
            article_title (str) : the title of the article
            article_date  (str) : the publication date of an article
    """

    db.execute("INSERT INTO magazine VALUES(?,?)",
               (article_title, article_date))
    db_connection.commit()


def send_mail_notification(article_title, article_url):
    """ Send a mail notification after addinf new article to the database

        Args:
        article_title (str) : the title of the article
        article_date  (str) : the publication date of an article
    """
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login('thiery.louison@gmail.com', 'ierzpncwbquegafe')
    msg = MIMEText(
        f'\nHi there is a new Fedora Magazine article available : {article_title}. \n You can read it here : {article_url}'
    )
    msg['Subject'] = 'New Fedora Magazine Article available'
    msg['From'] = 'thiery.louison@gmail.com'
    msg['To'] = 'thiery.louison@gmail.com'
    msg['To'] = 'maracheea.m@gmail.com'
    smtp_server.send_message(msg)
    smtp_server.quit()


def read_article_feed():
    """ Get article from RSS Feed """
    feed = feedparser.parse('https://fedoramagazine.org/feed/')
    for article in feed['entries']:
        if article_not_in_db(article['title'], article['published']):
            send_mail_notification(article['title'], article['link'])
            add_article_to_database(article['title'], article['published'])


if __name__ == '__main__':
    read_article_feed()
    db_connection.close()
