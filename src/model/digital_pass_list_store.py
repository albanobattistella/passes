# digital_pass_list_store.py
#
# Copyright 2022-2023 Pablo Sánchez Rodríguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from gi.repository import Gio, GObject

from .digital_pass import Date, DigitalPass


class DigitalPassListStore(GObject.GObject):

    __gtype_name__ = 'DigitalPassListStore'

    def __init__(self):
        super().__init__()
        self.__list_store = Gio.ListStore.new(DigitalPass)

    def find(self, digital_pass):
        return self.__list_store.find(digital_pass)

    def get_model(self):
        return self.__list_store

    def insert(self, digital_pass):
        self.__list_store.insert_sorted(digital_pass,
                                        SortPassesBy.expiration_date)

    def is_empty(self):
        return self.length() == 0

    def length(self):
        return len(self.__list_store)

    def remove(self, index):
        self.__list_store.remove(index)


class SortPassesBy:

    @classmethod
    def expiration_date(cls, d1, d2):
        """
        Sort passes by expiration date. In the event that two passes have the
        same expiration date then they will be sorted by description.
        """
        dates_comparison = Date.compare_dates(d1.expiration_date(),
                                              d2.expiration_date())

        d1_is_later_than_d2 = dates_comparison > 0
        dates_are_equal = dates_comparison == 0

        return  d1_is_later_than_d2 or \
                (dates_are_equal and d1.description() > d2.description())
