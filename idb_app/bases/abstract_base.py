from abc import ABC, abstractmethod


class AbstractBase(ABC):
    @property
    @abstractmethod
    def title(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def filter_buttons(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def filter_text(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def sort_buttons(self):
        raise NotImplementedError

    @abstractmethod
    def build_instances(self, query_set):
        raise NotImplementedError

    def create_base(self, query_set):
        base = {
            "title": self.title,
            "type": self.type,
            "instances": self.build_instances(query_set),
            "filter_buttons": self.filter_buttons,
            "filter_text": self.filter_text,
            "sort_buttons": self.sort_buttons,
        }
        return base
