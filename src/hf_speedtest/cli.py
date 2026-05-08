"""
Minimal re-interpretation of LibreSpeed's dlTest to Python + httpx.

Runs N parallel HTTP streams against a large file, counts bytes received,
applies a grace period, and reports speed in Mbit/s. Auto-shortens on
fast links via the same "bonusT" trick as the original.
"""

import asyncio
import sys
import time

import httpx

from .location import get_server_location

URL = "https://aws.cdn.hf.co/fast/5gb"

NUM_STREAMS = 8           # xhr_dlMultistream
STREAM_STAGGER_MS = 300   # xhr_multistreamDelay
GRACE_SECONDS = 1.5       # time_dlGraceTime
MAX_SECONDS = 20.0        # time_dl_max
OVERHEAD = 1.06           # overheadCompensationFactor
TIME_AUTO = True          # auto-shorten on fast connections
CHUNK_BYTES = 64 * 1024   # how many bytes to read per iteration


class State:
    def __init__(self) -> None:
        self.tot_loaded = 0          # cumulative bytes across all streams
        self.start_t = time.monotonic()
        self.bonus_t = 0.0           # virtual seconds shaved off
        self.grace_done = False
        self.stop = False            # set True to tell streams to bail


async def stream_loop(client: httpx.AsyncClient, state: State, idx: int, delay: float) -> None:
    """One download stream: keep refetching the URL until state.stop."""
    await asyncio.sleep(delay)
    while not state.stop:
        try:
            params = {"r": f"{idx}-{time.time_ns()}"}  # cache-buster
            async with client.stream("GET", URL, params=params, timeout=None) as r:
                r.raise_for_status()
                async for chunk in r.aiter_bytes(CHUNK_BYTES):
                    if state.stop:
                        return
                    state.tot_loaded += len(chunk)
        except (httpx.HTTPError, asyncio.CancelledError):
            if state.stop:
                return
            # restart this stream (mirrors xhr_ignoreErrors == 1)
            await asyncio.sleep(0.1)


async def ticker(state: State) -> None:
    """200 ms loop: handles grace, computes speed, ends the test."""
    while not state.stop:
        await asyncio.sleep(0.2)
        t = time.monotonic() - state.start_t

        if not state.grace_done:
            if t > GRACE_SECONDS:
                if state.tot_loaded > 0:
                    # restart measurement once the pipe is warm
                    state.start_t = time.monotonic()
                    state.bonus_t = 0.0
                    state.tot_loaded = 0
                state.grace_done = True
            continue

        speed_bps = state.tot_loaded / t                    # bytes/sec
        mbps = speed_bps * 8 * OVERHEAD / 1_000_000         # Mbit/s

        if TIME_AUTO:
            bonus = (5.0 * speed_bps) / 100_000 / 1000.0    # → seconds
            state.bonus_t += min(bonus, 0.4)

        progress = (t + state.bonus_t) / MAX_SECONDS
        bar_w = 30
        filled = int(min(progress, 1.0) * bar_w)
        bar = "#" * filled + "-" * (bar_w - filled)
        sys.stdout.write(f"\r[{bar}] {mbps:7.2f} Mbit/s  ({state.tot_loaded / 1_000_000:7.1f} MB in {t:4.1f}s)")
        sys.stdout.flush()

        if t + state.bonus_t > MAX_SECONDS:
            state.stop = True
            print(f"\nfinal: {mbps:.2f} Mbit/s")
            return


async def main() -> None:
    server_location = await get_server_location(URL)
    print(f"server location: {server_location}")

    state = State()
    limits = httpx.Limits(max_connections=NUM_STREAMS * 2, max_keepalive_connections=NUM_STREAMS)
    async with httpx.AsyncClient(limits=limits, http2=False, follow_redirects=True) as client:
        streams = [
            asyncio.create_task(stream_loop(client, state, i, (STREAM_STAGGER_MS / 1000) * i))
            for i in range(NUM_STREAMS)
        ]
        tick = asyncio.create_task(ticker(state))
        await tick
        for s in streams:
            s.cancel()
        await asyncio.gather(*streams, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
