import ftplib
import io
import logging
import threading
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import win32clipboard
from PIL import Image
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter, AutoDateLocator
from matplotlib.figure import Figure
from tkcalendar import DateEntry

from pi.temp import read_temp_df

LOGGER = logging.getLogger(__name__)


class App:
    def __init__(self, ip = None, user = None, password = None, db = None):
        self.root = tk.Tk()
        self.controls = Controls(master=self.root,
                                 db=db or Path(r'temp\temps.db'))

        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
        ax = self.fig.add_subplot(111)
        pad = .05
        self.fig.subplots_adjust(
            left=pad,
            right=1-pad,
            bottom=pad,
            top=1-pad
        )
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()

        self.controls.grid(row=0, column=0,
                           sticky=(tk.E, tk.W))
        self.canvas.get_tk_widget().grid(row=1, column=0,
                                         columnspan=2,
                                         sticky=(tk.E, tk.W, tk.N, tk.S))

        button = self.controls.winfo_children()[-1]
        LOGGER.info(button.config()['text'][-1])
        button.config({'command': self.plot})

        cols, rows = self.root.grid_size()
        self.root.columnconfigure(cols - 1, weight=1)
        self.root.rowconfigure(rows - 1, weight=1)

        if ip is not None:
            self.controls.ip = ip
        if user is not None:
            self.controls.user = user
        if password is not None:
            self.controls.password = password

    @property
    def df(self):
        df = read_temp_df(self.controls.db).applymap(lambda v: (v*9/5)+32)
        df = df.groupby(pd.Grouper(freq='10min', origin='start_day')).mean()

        rolling = self.controls.rolling
        if rolling is not None:
            df = df.rolling(rolling).mean()

        return df.loc[self.controls.date_start.strftime('%Y-%m-%d'):self.controls.date_end.strftime('%Y-%m-%d')]

    def plot(self):
        LOGGER.info('Plotting')
        ax: Axes = self.fig.axes[0]
        ax.clear()
        ax.plot(self.df, '.')
        lmajor = AutoDateLocator(maxticks=6)
        ax.xaxis.set_major_locator(lmajor)
        ax.xaxis.set_major_formatter(DateFormatter('%b-%d %H'))
        ax.grid(True)
        self.canvas.draw()
        self.fig_to_clipboard()

    def fig_to_clipboard(self):
        with io.BytesIO() as buf:
            self.fig.savefig(buf)
            im = Image.open(buf)

            with io.BytesIO() as output:
                im.convert("RGB").save(output, "BMP")
                data = output.getvalue()[14:]  # The file header off-set of BMP is 14 bytes

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # DIB = device independent bitmap
        win32clipboard.CloseClipboard()


class Controls(tk.Frame):
    def __init__(self, master, db = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        ttk.Button(master=self, text='Get Data')
        pi_settings = [
            (ttk.Label(master=self, text='IP'), ttk.Entry(master=self)),
            (ttk.Label(master=self, text='User'), ttk.Entry(master=self)),
            (ttk.Label(master=self, text='Password'), ttk.Entry(master=self)),
        ]

        for i, (label, entry) in enumerate(pi_settings):
            label.grid(row=i, column=0,
                      sticky=tk.E)
            entry.grid(row=i, column=1,
                       pady=5, padx=5,
                       sticky=tk.W)
        get_data_button = ttk.Button(master=self,
                                     text='Get Data',
                                     command=lambda *args: threading.Thread(target=self.get_data).start())
        get_data_button.grid(row=self.grid_size()[1], column=0,
                             columnspan=2,
                             sticky=(tk.W, tk.E))

        date = datetime.today() - timedelta(days=3)
        plot_settings = [
            (ttk.Label(master=self, text='Start'), DateEntry(master=self,
                                                             width=8,
                                                             year=date.year,
                                                             day=date.day,
                                                             month=date.month)),
            (ttk.Label(master=self, text='End'), DateEntry(master=self,
                                                           width=8,
                                                           year=date.year)),
            (ttk.Label(master=self, text='Avg'), ttk.Entry(master=self,
                                                           width=8))
        ]

        for i, (label, entry) in enumerate(plot_settings):
            label.grid(row=i, column=2,
                       sticky=tk.E)
            entry.grid(row=i, column=3,
                       sticky=tk.W)

        plot_button = ttk.Button(master=self,
                                 text='Plot Data')
        plot_button.grid(row=3, column=2,
                         columnspan=2,
                         sticky=(tk.W, tk.E))

        self.pi_settings = pi_settings
        self.plot_settings = plot_settings

        if db is not None:
            self.db = db if isinstance(db, Path) else Path(db)

    def get_data(self, dest = None):
        dest = dest or self.db
        try:
            with ftplib.FTP(self.ip, self.user, self.password) as conn:
                LOGGER.info(f'{self.ip}, {self.user}, {self.password}')
                with dest.open('wb') as file:
                    conn.retrbinary(f'RETR /home/pi/Documents/plants/temps.db', file.write)
        except Exception as e:
            LOGGER.exception(e)
        else:
            LOGGER.info(f'Success {dest}')

    @property
    def ip(self):
        return self.pi_settings[0][1].get()

    @ip.setter
    def ip(self, ip):
        widget = self.pi_settings[0][1]
        widget.delete(0, len(widget.get()))
        widget.insert(0, ip)

    @property
    def user(self):
        return self.pi_settings[1][1].get()

    @user.setter
    def user(self, user):
        widget = self.pi_settings[1][1]
        widget.delete(0, len(widget.get()))
        widget.insert(0, user)

    @property
    def password(self):
        return self.pi_settings[2][1].get()

    @password.setter
    def password(self, password):
        widget = self.pi_settings[2][1]
        widget.delete(0, len(widget.get()))
        widget.insert(0, password)

    @property
    def date_start(self):
        return datetime.strptime(self.plot_settings[0][1].get(), '%m/%d/%y')

    @property
    def date_end(self):
        return datetime.strptime(self.plot_settings[1][1].get(), '%m/%d/%y')

    @property
    def rolling(self):
        try:
            return int(self.plot_settings[2][1].get())
        except:
            return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = App(ip='192.168.1.126', user='pi', password='raspberry')
    # app.controls.get_data()
    app.plot()
    app.root.mainloop()
