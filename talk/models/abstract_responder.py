#!/usr/bin/env python

from abc import ABCMeta, abstractmethod


class AbstractResponder(metaclass=ABCMeta):
    @abstractmethod
    def talk(self):
        pass

