from abc import ABC, abstractmethod

class DbAccess:
  @abstractmethod
  def get(self):
    pass

  @abstractmethod
  def save(self, file):
    pass

  @abstractmethod
  def ensureExists(self):
    pass

  @abstractmethod
  def read_blob(self, blob, file):
    pass