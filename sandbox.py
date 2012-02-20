import sys

import hpfeed.hpf_sink as hpf_sink


def main():
    sink = hpf_sink.HPFeedsSink()
    sink.run()

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
