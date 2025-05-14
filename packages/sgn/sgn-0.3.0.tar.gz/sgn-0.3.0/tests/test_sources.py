"""Tests for sources module."""

from collections import deque
from collections.abc import Iterator
import signal
import pytest

from sgn.base import Frame
from sgn.sources import DequeSource, IterSource, NullSource, SignalEOS


class TestSignalEOS:
    """Tests for SignalEOS class."""

    def test_context_manager(self):
        SignalEOS.handled_signals.add(signal.SIGUSR2)
        with SignalEOS() as f:
            signal.raise_signal(signal.SIGUSR2)
        signal.signal(signal.SIGUSR2, lambda x, y: None)
        f.raise_signal(signal.SIGUSR2)

    def test_raise_signal(self):
        """Test the raise_signal method specifically."""
        # Set up a test signal
        test_signal = signal.SIGUSR1

        # First test with a signal that hasn't been received (should not raise)
        SignalEOS.rcvd_signals = set()
        signal_eos = SignalEOS()
        signal_eos.raise_signal(test_signal)

        # Now test with a signal that has been received (should reach line 59)
        SignalEOS.rcvd_signals.add(test_signal)

        # Set up a flag to verify the signal was raised
        signal_raised = False

        def test_handler(signum, frame):
            nonlocal signal_raised
            signal_raised = True

        # Set our test handler
        original_handler = signal.getsignal(test_signal)
        signal.signal(test_signal, test_handler)

        try:
            signal_eos.raise_signal(test_signal)
            assert signal_raised, "Signal was not raised"
        finally:
            # Restore original handler
            signal.signal(test_signal, original_handler)
            SignalEOS.rcvd_signals = set()


class TestNullSource:
    """Tests for Null Source class."""

    def test_init(self):
        """Test the NullSource class constructor."""
        src = NullSource(name="src1", source_pad_names=("O1", "O2"))
        assert src.name == "src1"
        assert [p.name for p in src.source_pads] == ["src1:src:O1", "src1:src:O2"]

    def test_new(self):
        """Test the new method."""
        src = NullSource(
            name="src1", source_pad_names=("O1", "O2"), num_frames=0, wait=1e-10
        )
        frame = src.new(src.source_pads[0])
        assert isinstance(frame, Frame)
        assert frame.data is None
        assert frame.EOS


class TestIterSource:
    """Test group for IterSource class."""

    def test_init(self):
        """Test the DeqSource class constructor."""
        src = IterSource(name="src1", source_pad_names=("O1", "O2"))
        assert isinstance(src, IterSource)
        assert [p.name for p in src.source_pads] == ["src1:src:O1", "src1:src:O2"]
        assert src.eos_on_empty == {"src1:src:O1": True, "src1:src:O2": True}
        assert isinstance(src.iters["src1:src:O1"], Iterator)
        assert isinstance(src.iters["src1:src:O2"], Iterator)

    def test_init_with_iter(self):
        """Test the DeqSource class constructor."""
        src = IterSource(
            name="src1",
            source_pad_names=("O1", "O2"),
            iters={
                "src1:src:O1": iter(deque([1, 2, 3])),
                "src1:src:O2": iter(deque([4, 5, 6])),
            },
        )
        assert isinstance(src, IterSource)
        assert isinstance(src.iters["src1:src:O1"], Iterator)

    def test_init_err_deques_wrong_number(self):
        """Test init with wrong number of deques."""
        with pytest.raises(ValueError):
            IterSource(
                name="src1",
                source_pad_names=("O1", "O2"),
                iters={
                    "src1:src:O1": deque(),
                    "src1:src:O2": deque(),
                    "src1:src:O3": deque(),
                },
            )

    def test_init_err_deques_wrong_name(self):
        """Test init with wrong pad name."""
        with pytest.raises(ValueError):
            IterSource(
                name="src1",
                source_pad_names=("O1", "O2"),
                iters={"src1:src:O1": deque(), "src1:src:O3": deque()},
            )

    def test_init_err_eosoe_wrong_number(self):
        """Test init with wrong number of limits."""
        with pytest.raises(ValueError):
            IterSource(
                name="src1",
                source_pad_names=("O1", "O2"),
                eos_on_empty={
                    "src1:src:O1": True,
                    "src1:src:O2": True,
                    "src1:src:O3": False,
                },
            )

    def test_init_err_eosoe_wrong_name(self):
        """Test init with wrong pad name."""
        with pytest.raises(ValueError):
            IterSource(
                name="src1",
                source_pad_names=("O1", "O2"),
                eos_on_empty={"src1:src:O1": True, "src1:src:O3": True},
            )

    def test_new_empty(self):
        """Test new data method with empty queue."""
        src = IterSource(name="src1", source_pad_names=("O1", "O2"), eos_on_empty=True)

        # First frame
        frame = src.new(src.source_pads[0])
        assert isinstance(frame, Frame)
        assert frame.EOS
        assert frame.data is None


class TestDeqSource:
    """Test group for DeqSource class."""

    def test_init(self):
        """Test the DeqSource class constructor."""
        src = DequeSource(name="src1", source_pad_names=("O1", "O2"))
        assert isinstance(src, DequeSource)
        assert [p.name for p in src.source_pads] == ["src1:src:O1", "src1:src:O2"]
        assert src.eos_on_empty == {"src1:src:O1": True, "src1:src:O2": True}
        assert src.deques == {"src1:src:O1": deque(), "src1:src:O2": deque()}

    def test_new_simple(self):
        """Test new with single item in queue."""
        src = DequeSource(name="src1", source_pad_names=("O1", "O2"))

        # Add item to queue as data payload
        src.deques["src1:src:O1"].append("test")

        frame = src.new(src.source_pads[0])
        assert frame.data == "test"

        # Second frame should be empty
        frame = src.new(src.source_pads[0])
        assert frame.data is None

    def test_dynamic_queue(self):
        """Test new with the contents of queue changing between successive iterations of
        the stream loop."""
        src = DequeSource(
            name="src1", source_pad_names=("O1", "O2"), eos_on_empty=False
        )

        frame = src.new(src.source_pads[0])
        assert frame.data is None

        # Add item to queue as data payload
        src.deques["src1:src:O1"].append("test2")

        # Second frame should be empty
        frame = src.new(src.source_pads[0])
        assert frame.data == "test2"
