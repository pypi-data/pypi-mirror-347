from fitburst.backend.generic import DataReader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class NpzReader(DataReader):
    def __init__(self, fname, factor):
        self.__fname = fname

        temp = np.load(fname, allow_pickle=True)
        self.metadata = temp["metadata"].tolist()
        temp.close()

        super().__init__(fname)
        self.downsampling_factor = factor

    def __repr__(self):
        return f"{self.__class__.__name__}(fname='{self.__fname}', file_downsampling={self.downsampling_factor})"

    def __str__(self):
        return f"(fname='{self.__fname}', file_downsampling={self.downsampling_factor})"


class NpzWriter:
    dm_index = -2
    scattering_index = -4
    spectral_index = 0
    ref_freq = 400

    def __init__(self, original_data: NpzReader):
        self.reader = original_data
        if self.reader.data_full is None:
            self.reader.load_data()

        self.burst_parameters = self.reader.burst_parameters

    def update_burst_parameters(self, **kwargs):
        if "amplitude" in kwargs:
            self.burst_parameters["amplitude"] = kwargs["amplitude"]
        if "dm" in kwargs:
            self.burst_parameters["dm"] = kwargs["dm"]
        if "scattering_timescale" in kwargs:
            self.burst_parameters["scattering_timescale"] = kwargs[
                "scattering_timescale"
            ]
        if "arrival_time" in kwargs:
            self.burst_parameters["arrival_time"] = kwargs["arrival_time"]
        if "burst_width" in kwargs:
            self.burst_parameters["burst_width"] = kwargs["burst_width"]
        if "spectral_running" in kwargs:
            self.burst_parameters["spectral_running"] = kwargs["spectral_running"]

        number_of_components = len(self.burst_parameters["arrival_time"])
        for param in self.burst_parameters:
            if type(self.burst_parameters[param]) != list:
                self.burst_parameters[param] = [
                    self.burst_parameters[param]
                ] * number_of_components

            if len(self.burst_parameters[param]) != number_of_components:
                if param in ["arrival_time", "burst_width", "scattering_timescale"]:
                    raise ValueError(
                        f"Unexpected length of {len(self.burst_parameters[param])} for parameter {param} when {number_of_components} expected."
                    )
                else:
                    self.burst_parameters[param] = [
                        self.burst_parameters[param][0]
                    ] * number_of_components

    def save(self, new_filepath: str):
        with open(new_filepath, "wb") as f:
            np.savez(
                f,
                data_full=self.reader.data_full,
                burst_parameters=self.burst_parameters,
                metadata=self.reader.metadata,
            )
        print(f"Saved file at {new_filepath} successfully.")


class Peaks:
    def __init__(self, oscfar_result):
        self.peaks = np.array(oscfar_result[0])
        self.threshold = np.array(oscfar_result[1])


class WaterFallAxes:
    def __init__(
        self,
        data: DataReader,
        width: float,
        height: float,
        bottom: float,
        left: float = None,
        hratio: float = 1,
        vratio: float = 1,
        show_ts=True,
        show_spec=True,
        labels_on=[True, True],
        title="",
        readjust_title=0,
    ):
        self._data = data
        self.show_ts = show_ts
        self.show_spec = show_spec

        if labels_on[0] or labels_on[1]:
            width = 0.6
            height = 0.6

        bot = bottom
        if left is None:
            left = bot

        im_w = width / hratio
        im_h = height / vratio

        self.im = plt.axes((left, bot, im_w, im_h))
        if self.show_ts:
            self.ts = plt.axes((left, im_h + bot, im_w, 0.2 / vratio), sharex=self.im)
            plt.text(
                1,  # - len(title) * 0.025,
                0.85 - readjust_title,
                title,
                transform=self.ts.transAxes,
                ha="right",
                va="bottom",
            )
        if self.show_spec:
            self.spec = plt.axes((im_w + left, bot, 0.2 / hratio, im_h), sharey=self.im)

        if labels_on[0] or labels_on[1]:
            if labels_on[0]:
                self.im.set_xlabel("Time (s)")
            if labels_on[1]:
                self.im.set_ylabel("Observing frequency (MHz)")
        else:
            plt.setp(self.im.get_xticklabels(), visible=False)
            plt.setp(self.im.get_xticklines(), visible=False)
            plt.setp(self.im.get_yticklabels(), visible=False)
            plt.setp(self.im.get_yticklines(), visible=False)

        if self.show_ts:
            plt.setp(self.ts.get_xticklabels(), visible=False)
            plt.setp(self.ts.get_xticklines(), visible=False)
            plt.setp(self.ts.get_yticklabels(), visible=False)
            plt.setp(self.ts.get_yticklines(), visible=False)
        if self.show_spec:
            plt.setp(self.spec.get_xticklabels(), visible=False)
            plt.setp(self.spec.get_xticklines(), visible=False)
            plt.setp(self.spec.get_yticklabels(), visible=False)
            plt.setp(self.spec.get_yticklines(), visible=False)

        self.time_series = np.sum(self._data.data_full, 0)
        self.freq_series = np.sum(self._data.data_full, 1)

    def plot(self):
        self.im.imshow(
            self._data.data_full,
            cmap="gist_yarg",
            aspect="auto",
            origin="lower",
            extent=[
                self._data.times[0],
                self._data.times[-1],
                self._data.freqs[0],
                self._data.freqs[-1],
            ],
        )
        if self.show_ts:
            self.ts.plot(self._data.times, self.time_series)
        if self.show_spec:
            self.spec.plot(self.freq_series, self._data.freqs)

    def plot_time_peaks(self, peaks: Peaks, color, show_thres=False):
        for x in peaks.peaks:
            self.im.axvline(self._data.times[x], color=color, linestyle="--", alpha=0.5)

        if self.show_ts:
            self.ts.scatter(
                self._data.times[peaks.peaks],
                self.time_series[peaks.peaks],
                marker="x",
                color=color,
            )

        if show_thres:
            self.ts.plot(self._data.times, peaks.threshold, c="grey", linestyle="--")


class WaterFallGrid:
    def __init__(self, nrows: int, ncols: int, vspacing=0.1, hspacing=0.1):
        # Spacing is actually an offset oops
        self.nrows = nrows
        self.ncols = ncols
        self.axes = np.zeros((nrows, ncols), dtype=object)
        self.vs = vspacing
        self.hs = hspacing

    def plot(
        self,
        data: list,
        peaks: list,
        titles: list,
        color,
        labels=[True, False],
        adjust_t=0,
        show_thres=False,
    ):
        if type(data) == list or type(peaks) == list or type(titles) == list:
            data = np.array(data).reshape((self.nrows, self.ncols))
            peaks = np.array(peaks).reshape((self.nrows, self.ncols))
            titles = np.array(titles).reshape((self.nrows, self.ncols))

        lefts = np.arange(0, 1, 1 / (self.ncols)) + self.hs
        bottoms = np.arange(0, 1, 1 / (self.nrows)) + self.vs
        for i in range(self.nrows):
            for j in range(self.ncols):
                ax = WaterFallAxes(
                    data[i, j],
                    0.75,
                    0.75,
                    bottoms[i],
                    left=lefts[j],
                    hratio=self.ncols,
                    vratio=self.nrows,
                    show_ts=True,
                    show_spec=True,
                    labels_on=labels,
                    title=titles[i, j],
                    readjust_title=adjust_t,
                )
                ax.plot()
                ax.plot_time_peaks(peaks[i, j], color, show_thres)
                self.axes[i, j] = ax

    def add_info(self, info: pd.DataFrame):
        ax = plt.axes((0, 0, 1, self.vs - 0.1))
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plt.setp(ax.get_xticklines(), visible=False)
        plt.setp(ax.get_yticklines(), visible=False)

        table = ax.table(
            info.values,
            colLabels=info.columns,
            rowLabels=info.index,
            loc="bottom",
            cellLoc="center",
            rowLoc="center",
            bbox=[0, 0, 1, 1],
        )
