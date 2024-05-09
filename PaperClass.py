
class Paper:
   def __init__(self, title, url, year, authors, isOpenAccess,paperId):
      self.paperId = paperId
      self.title = title
      self.url = url 
      self.year = year 
      self.authors = [name['name'] for name in authors]
      self.isOpenAcess = isOpenAccess
    
   def __str__(self) -> str:
       return f'''
       title: {self.title}
       nurl: {self.url}
       year: {self.year}
       authors: {', '.join(self.authors)}
       OpenAcess: {'Yes' if self.isOpenAcess else 'No'}\n'''