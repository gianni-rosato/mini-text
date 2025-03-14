# window.py
#
# Copyright 2023 Nokse
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio, Gdk

@Gtk.Template(resource_path='/io/github/nokse22/minitext/window.ui')
class MiniTextWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MiniTextWindow'

    text_view = Gtk.Template.Child("text_view")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('io.github.nokse22.minitext')

        self.settings.bind(
            "window-width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        self.settings.bind(
            "window-height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )

    @Gtk.Template.Callback("on_copy_action")
    def on_copy_action(self, *args):
        print("copy")
        text_buffer = self.text_view.get_buffer()
        start = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        text = text_buffer.get_text(start, end, False)
        if text.strip() != "":
            self.copy_to_clipboard(text)

    @Gtk.Template.Callback("on_paste_action")
    def on_paste_action(self, *args):
        clipboard = Gdk.Display().get_default().get_clipboard()
        def callback(clipboard, res, data):
            text = clipboard.read_text_finish(res)
            text_buffer = self.text_view.get_buffer()
            text_buffer.set_text(text)
        data = {}
        res = clipboard.read_text_async(None, callback, data)

    @Gtk.Template.Callback("on_delete_action")
    def on_delete_action(self, *args):
        print("delete")
        text_buffer = self.text_view.get_buffer()
        text_buffer.set_text("")

    def copy_to_clipboard(self, text):
        clipboard = Gdk.Display().get_default().get_clipboard()
        clipboard.set(text)
        #clipboard.store()
