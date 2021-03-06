#!/usr/bin/python
# coding: utf-8

"""
FeedList class  
"""


__version__ =  '1.2' 



from PyQt4.QtGui import *
from Feed import Feed;
from DB import DB;

class FeedList():
  def __init__(self, feedListWidget, dbHandle):
    self.feedListWidget = feedListWidget;
    self.dbHandle = dbHandle;
    self.refresh();
    
  def refresh(self):
    self.feedListWidget.clear();
    self.feedListItems = [];
    
    itemlist = self.dbHandle.getFeedList();
    for item in itemlist:
      self.feedListWidget.addItem(item['name']);
      self.feedListItems.append(item['id']);
   
  def add(self, feed, name, address):
    
    self.dbHandle.send('insert into feedList(name, addr, FeedTitle) values (\''+str(name)+'\',\''+str(address)+'\', \''+feed.feedTitle+'\')');
    
    size = (len(feed.title));

    for i in range(0, size):
      self.dbHandle.send('insert into items(feed_id, title, pubDate, description) values ('+str(self.dbHandle.lastID())+',\''+feed.title[i].replace("'","&#39;")+'\', \''+feed.pubDate[i].replace("'","&#39;")+'\', \''+feed.description[i].replace("'","&#39;")+'\')');
    self.refresh();
    
  def remove(self, feed_id):
    self.dbHandle.send('delete from feedList where id='+str(self.feedListItems[feed_id]));
    self.dbHandle.send('delete from items where feed_id='+str(self.feedListItems[feed_id]));

    self.refresh();

  def getSingleSubscription(self, feed_id):
    feed = self.dbHandle.getSingleSubscription(self.feedListItems[feed_id]);
    return feed;

  def getSingleSubscriptionToHTML(self, feed_id):
    
    feed = self.dbHandle.getSingleSubscription(self.feedListItems[feed_id]);
    size = (len(feed['content']));
    result = "";
    for i in range(0, size):
      result += """<article><h2>"""+feed['content'][i]['title']+"""</h2>
      <div class=\"pubDate\">"""+feed['content'][i]['pubDate']+"""</div>
      <div class=\"description\">"""+feed['content'][i]['description']+"""</div></article>
      """;
    return result;
    
  def updateAll(self, Feed, Source):
    for feed_id in self.feedListItems:
      
      #deleting old feeds
      try:
	source = Source();

	feed_from_db = self.dbHandle.getSingleSubscription(feed_id);
	source = source.fromURL(str(feed_from_db['addr']));
	feed = Feed(source);
	self.dbHandle.send('delete from items where feed_id='+str(feed_id));

	size = len(feed.title);
      
	for i in range(0, size):
	  self.dbHandle.send('insert into items(feed_id, title, pubDate, description) values ('+str(feed_id)+',\''+feed.title[i]+'\', \''+feed.pubDate[i]+'\', \''+feed.description[i]+'\')');
      except:
	raise Exception('downloadError', 'downloadError');	
	
  def updateSelectedFeed(self, selected_id, Feed, Source):
    feed_id = self.feedListItems[selected_id];
    source = Source();

    feed_from_db = self.dbHandle.getSingleSubscription(feed_id);
    try:
      source = source.fromURL(str(feed_from_db['addr']));
    
      feed = Feed(source);
      size = (len(feed.title));
      
      self.dbHandle.send('delete from items where feed_id='+str(feed_id));

      for i in range(0, size):
	self.dbHandle.send('insert into items(feed_id, title, pubDate, description) values ('+str(feed_id)+',\''+feed.title[i]+'\', \''+feed.pubDate[i]+'\', \''+feed.description[i]+'\')');
    except:
      raise Exception('downloadError', 'downloadError');
  
  def editSelectedFeed(self,selected, name, address, Feed, Source):
    feed_id = self.feedListItems[selected];
    source = Source();
    source = source.fromURL(address);
    feed = Feed(source);
    size = len(feed.title);
      
    self.dbHandle.send('delete from items where feed_id='+str(feed_id));

    for i in range(0, size):
      self.dbHandle.send('insert into items(feed_id, title, pubDate, description) values ('+str(feed_id)+',\''+feed.title[i]+'\', \''+feed.pubDate[i]+'\', \''+feed.description[i]+'\')');
      
    self.dbHandle.send("update feedList set name=\'"+name+"\', addr=\'"+address+"\', feedTitle=\'"+feed.feedTitle+"\' where id="+str(self.feedListItems[selected]))
    
    
    
    
    self.refresh();