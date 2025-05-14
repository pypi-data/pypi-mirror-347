from collections.abc import Generator
from dataclasses import dataclass

import arrakis
from sgnts.base import Offset, SeriesBuffer, TSResourceSource


@dataclass
class ArrakisSource(TSResourceSource):
    """Source element that streams channel data from Arrakis.

    Source pads should be named after the channel they will stream
    from Arrakis.

    start_time: Optional[int] = None
        start time of stream, or "now" if None.
    duration: Optional[int] = None
        duration of stream, or endless stream if None.
    in_queue_timeout: int = 60
        How long to wait for a block from the Arrakis server before
        timing out with an error.

    """

    def get_data(self) -> Generator:
        for block in arrakis.stream(
            self.source_pad_names, self.start_time, self.end_time
        ):
            for name, series in block.items():
                channel = series.channel

                # FIXME: should we do this for every block?
                assert channel.sample_rate in Offset.ALLOWED_RATES, (
                    f"channel {name} has an invalid sample rate: {channel.sample_rate}"
                )
                # FIXME: should we do other checks?

                buf = SeriesBuffer(
                    offset=Offset.fromns(series.time_ns),
                    data=series.data,
                    sample_rate=int(series.sample_rate),
                )
                pad = self.srcs[name]

                yield pad, buf
